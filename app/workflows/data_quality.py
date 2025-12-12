from app.engine.graph import Node, Graph, save_graph
import uuid


def create_data_quality_workflow():
    graph_id = str(uuid.uuid4())

    graph = Graph(
        nodes={
            "profile_data": Node(type="tool", tool="profile_data"),
            "identify_anomalies": Node(type="tool", tool="identify_anomalies"),
            "generate_rules": Node(type="tool", tool="generate_rules"),
            "apply_rules": Node(type="tool", tool="apply_rules"),
            "check_loop": Node(
                type="condition",
                expr="state['anomaly_count'] > state.get('threshold', 0)"
            )
        },
        edges={
            "profile_data": "identify_anomalies",
            "identify_anomalies": "generate_rules",
            "generate_rules": "apply_rules",
            "apply_rules": "check_loop",
            "check_loop": {
                "true": "identify_anomalies",
                "false": "end"
            }
        },
        start_node="profile_data",
        metadata={
            "max_iterations": 10
        }
    )

    save_graph(graph_id, graph)

    return graph_id
