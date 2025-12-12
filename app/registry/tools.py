from typing import Dict, List, Any
import statistics

TOOLS: Dict[str, Any] = {}

def register_tool(name: str, fn):
    TOOLS[name] = fn

def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)

def safe_mean(values):
    return statistics.mean(values) if values else None

def safe_median(values):
    return statistics.median(values) if values else None

def safe_mode(values):
    if not values:
        return None
    modes = statistics.multimode(values)
    return modes[0] if modes else None

def safe_std(values):
    if not values or len(values) < 2:
        return 0.0
    return statistics.stdev(values)

def compute_quartiles(values):
    if not values:
        return None, None
    sorted_vals = sorted(values)
    try:
        qs = statistics.quantiles(sorted_vals, n=4)
        return qs[0], qs[2]
    except:
        mid = len(sorted_vals) // 2
        lower = sorted_vals[:mid]
        upper = sorted_vals[mid+1:]
        return statistics.median(lower), statistics.median(upper)

def compute_bounds(values):
    q1, q3 = compute_quartiles(values)
    iqr = q3 - q1
    lower_iqr = q1 - 1.5 * iqr
    upper_iqr = q3 + 1.5 * iqr
    mean = safe_mean(values)
    std = safe_std(values)
    lower_z = mean - 3 * std if std > 0 else None
    upper_z = mean + 3 * std if std > 0 else None
    return {
        "q1": q1, "q3": q3, "iqr": iqr,
        "lower_iqr": lower_iqr, "upper_iqr": upper_iqr,
        "mean": mean, "std": std,
        "lower_z": lower_z, "upper_z": upper_z
    }

def compute_clean_replacement(col_values, lower, upper):
    clean = [v for v in col_values if is_number(v) and not (v < lower or v > upper)]
    if not clean:
        clean = [v for v in col_values if is_number(v)]
    if not clean:
        return None
    clean_sorted = sorted(clean)
    n = len(clean_sorted)
    if n % 2 == 1:
        return clean_sorted[n // 2]
    return (clean_sorted[n // 2 - 1] + clean_sorted[n // 2]) / 2


def profile_data(state: Dict[str, Any]):
    data = state.get("data", [])
    if not isinstance(data, list) or not data:
        state["profile"] = {}
        return state

    all_columns = set()
    for row in data:
        if isinstance(row, dict):
            all_columns.update(row.keys())

    numeric_stats = {}
    missing_counts = {}
    negative_counts = {}

    for col in all_columns:
        col_values = []
        missing = 0
        negative = 0

        for row in data:
            val = row.get(col)
            if val is None:
                missing += 1
            else:
                if is_number(val):
                    col_values.append(float(val))
                    if val < 0:
                        negative += 1

        missing_counts[col] = missing
        negative_counts[col] = negative

        if col_values:
            stats = compute_bounds(col_values)
            stats["median"] = safe_median(col_values)
            stats["mode"] = safe_mode(col_values)
            numeric_stats[col] = stats
        else:
            numeric_stats[col] = None

    state["profile"] = {
        "missing_counts": missing_counts,
        "negative_counts": negative_counts,
        "numeric_stats": numeric_stats
    }

    return state


def identify_anomalies(state):
    data = state.get("data", [])
    profile = state.get("profile", {})
    options = state.get("options", {})

    use_z = options.get("use_zscore", False)
    z_thresh = options.get("z_thresh", 3.0)

    anomalies = []
    stats = profile.get("numeric_stats", {})

    for i, row in enumerate(data):
        for col, val in row.items():

            if val is None:
                anomalies.append({"row": i, "column": col, "issue": "missing"})
                continue

            if is_number(val):
                num = float(val)

                if num < 0:
                    anomalies.append({"row": i, "column": col, "issue": "negative_value"})

                col_stats = stats.get(col)
                if col_stats:
                    if num < col_stats["lower_iqr"] or num > col_stats["upper_iqr"]:
                        anomalies.append({"row": i, "column": col, "issue": "outlier_iqr"})

                    if use_z and col_stats["std"] > 0:
                        z = abs((num - col_stats["mean"]) / col_stats["std"])
                        if z > z_thresh:
                            anomalies.append({
                                "row": i,
                                "column": col,
                                "issue": "outlier_z",
                                "z": z
                            })

    state["anomalies"] = anomalies
    state["anomaly_count"] = len(anomalies)
    return state


def generate_rules(state):
    anomalies = state.get("anomalies", [])
    profile = state.get("profile", {})
    numeric_stats = profile.get("numeric_stats", {})
    data = state.get("data", [])
    stats = numeric_stats

    rules = {}

    for a in anomalies:
        col = a["column"]
        issue = a["issue"]

        col_values = [row.get(col) for row in data if is_number(row.get(col))]
        if not stats.get(col):
            continue

        lower = stats[col]["lower_iqr"]
        upper = stats[col]["upper_iqr"]
        replacement = compute_clean_replacement(col_values, lower, upper)

        if issue == "missing":
            rules.setdefault(col + "-missing", {
                "column": col,
                "action": "fill_missing",
                "value": replacement,
                "explain": f"Fill missing in '{col}' with {replacement}"
            })

        if issue == "negative_value":
            rules.setdefault(col + "-neg", {
                "column": col,
                "action": "fix_negative",
                "value": replacement,
                "explain": f"Replace negative '{col}' with {replacement}"
            })

        if issue.startswith("outlier"):
            rules.setdefault(col + "-outlier", {
                "column": col,
                "action": "fix_outlier",
                "value": replacement,
                "explain": f"Replace outliers in '{col}' with median={replacement}"
            })

    state["rules"] = list(rules.values())
    return state


# APPLY RULES

def apply_rules(state):
    data = state.get("data", [])
    rules = state.get("rules", [])
    profile = state.get("profile", {})
    stats = profile.get("numeric_stats", {})

    for rule in rules:
        col = rule["column"]
        action = rule["action"]
        value = rule["value"]

        bounds = stats.get(col)

        for row in data:
            current = row.get(col)

            # missing
            if action == "fill_missing" and current is None:
                row[col] = value

            # negative
            if action == "fix_negative" and is_number(current) and current < 0:
                row[col] = value

            # OUTLIER → Winsorization
            if action == "fix_outlier" and is_number(current):
                lb = bounds["lower_iqr"]
                ub = bounds["upper_iqr"]

                if current < lb:
                    row[col] = lb     # replace with lower bound
                elif current > ub:
                    row[col] = ub     # replace with upper bound

    state["data"] = data
    state["anomalies"] = []
    state["anomaly_count"] = 0
    return state



register_tool("profile_data", profile_data)
register_tool("identify_anomalies", identify_anomalies)
register_tool("generate_rules", generate_rules)
register_tool("apply_rules", apply_rules)
