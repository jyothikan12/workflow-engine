from typing import Dict, Any
from pydantic import BaseModel

class Node(BaseModel):
    type: str                      
    tool: str | None = None       
    expr: str | None = None 
    
class Graph(BaseModel):
    nodes: Dict[str, Node]         
    edges: Dict[str, Any]          
    start_node: str               
    metadata: Dict[str, Any] = {}  
    
GRAPH_STORE: Dict[str, Graph] = {} 

def save_graph(graph_id: str, graph: Graph):
    GRAPH_STORE[graph_id] = graph
        
def load_graph(graph_id: str) -> Graph:
    if graph_id not in GRAPH_STORE:
        raise ValueError("Graph not found")
    return GRAPH_STORE[graph_id]        