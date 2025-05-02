import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from global_variables import *
import streamlit as st
import tempfile
import os
from pyvis.network import Network
import networkx as nx
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle

st.set_page_config(page_title="Visualizer", layout="wide")
st.title("📈 Visualizer")

# Sample Data
def networkx_to_cytoscape_elements(G: nx.Graph):
    elements = {
        "nodes": [],
        "edges": []
    }

    # Ajouter les noeuds
    for node_id, data in G.nodes(data=True):
        node_data = {"id": str(node_id)}
        node_data.update(data)  # ajoute 'label', 'name', 'content', etc.
        elements["nodes"].append({"data": node_data})

    # Ajouter les arêtes
    for edge_id, (source, target, data) in enumerate(G.edges(data=True), start=1):
        edge_data = {
            "id": str(data.get("id", edge_id)),
            "source": str(source),
            "target": str(target)
        }
        edge_data.update({k: v for k, v in data.items() if k != "id"})
        elements["edges"].append({"data": edge_data})

    return elements

# Exemple d'utilisation
G = nx.DiGraph()

# Ajout des noeuds
G.add_node("oui", label="PERSON", name="Streamlit")
G.add_node("2", label="PERSON", name="Hello")
G.add_node("3", label="PERSON", name="World")
G.add_node("4", label="POST", content="x")
G.add_node("5", label="POST", content="y")

# Ajout des arêtes avec des IDs personnalisés
G.add_edge("oui", "2", id="6", label="FOLLOWS")
G.add_edge("2", "3", id="7", label="FOLLOWS")
G.add_edge("3", "4", id="8", label="POSTED")
G.add_edge("oui", "5", id="9", label="POSTED")
G.add_edge("5", "4", id="10", label="QUOTES")

# Conversion
elements = networkx_to_cytoscape_elements(G)

# Style node & edge groups
node_styles = [
    NodeStyle("PERSON", "#FF7F3E", "name", "person"),
    NodeStyle("POST", "#2A629A", "content", "description"),
]

edge_styles = [
    EdgeStyle("FOLLOWS", caption='label', directed=True),
    EdgeStyle("POSTED", caption='label', directed=True),
    EdgeStyle("QUOTES", caption='label', directed=True),
]

# Render the component
st_link_analysis(elements, "cose", node_styles, edge_styles)