from typing import Dict, Any
from .graph import Graph, load_graph
from app.registry.tools import TOOLS


RUN_STORE: Dict[str, Dict[str, Any]] = {}


def run_graph(graph_id: str, initial_state: Dict[str, Any]):
    graph: Graph = load_graph(graph_id)

    state = initial_state.copy()
    logs = []

    current = graph.start_node
    iteration = 0
    max_iterations = graph.metadata.get("max_iterations", 20)

    while current != "end":

        node = graph.nodes[current]
        before_state = state.copy()

        if node.type == "tool":
            tool_fn = TOOLS[node.tool]
            state = tool_fn(state)

        elif node.type == "condition":
            condition_result = eval(node.expr, {}, {"state": state})
            next_node = graph.edges[current]["true" if condition_result else "false"]
            logs.append({
                "node": current,
                "type": "condition",
                "condition": node.expr,
                "result": condition_result
            })
            current = next_node
            continue

        
        logs.append({
            "node": current,
            "before": before_state,
            "after": state
        })

        
        next_node = graph.edges.get(current, "end")
        if isinstance(next_node, str):
            current = next_node
        else:
            current = next_node

        
        iteration += 1
        if iteration > max_iterations:
            logs.append({"error": "Max iterations exceeded"})
            break

    return {"final_state": state, "logs": logs}
