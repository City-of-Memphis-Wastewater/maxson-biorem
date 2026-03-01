import sqlite3
from graphviz import Digraph

conn = sqlite3.connect("biorem.db")
cur = conn.cursor()

dot = Digraph(comment='Biorem System')

# Add nodes
cur.execute("SELECT id, name, type FROM nodes")
for nid, name, ntype in cur.fetchall():
    dot.node(str(nid), f"{name}\n({ntype})")

# Add edges
#cur.execute("SELECT from_id, to_id, type FROM edges")
#for f, t, etype in cur.fetchall():
#    dot.edge(str(f), str(t), label=etype)
cur.execute("""
    SELECT from_id, to_id, type, MIN(id)
    FROM edges
    GROUP BY from_id, to_id, type
""")
for f, t, etype, _ in cur.fetchall():
    dot.edge(str(f), str(t), label=etype)

# Save diagram
dot.render('biorem_system', format='png', cleanup=True)
# src/maxson_biorem/graphviz_gen.py
from graphviz import Digraph
from pathlib import Path
import sqlite3

# Set output folder
OUTPUT_DIR = Path("exports")
OUTPUT_DIR.mkdir(exist_ok=True)  # create folder if it doesn't exist

# Connect to DB
conn = sqlite3.connect("biorem.db")
cur = conn.cursor()

# Create a directed graph
dot = Digraph(comment="Biorem System")

# Add nodes from DB
cur.execute("SELECT id, name, type FROM nodes")
for nid, name, ntype in cur.fetchall():
    color = "lightgrey"
    shape = "ellipse"
    if ntype == "component":
        color = "lightblue"
        shape = "box"
    elif ntype == "sensor":
        color = "lightgreen"
        shape = "oval"
    elif ntype == "tank":
        color = "orange"
        shape = "cylinder"
    dot.node(str(nid), name, color=color, style="filled", shape=shape)

# Add edges from DB
cur.execute("SELECT from_id, to_id, type FROM edges")
for f, t, etype in cur.fetchall():
    dot.edge(str(f), str(t), label=etype)

conn.close()

# Render PNG in exports/
output_path = OUTPUT_DIR / "biorem_system"
dot.render(str(output_path), format="png", cleanup=True)

print(f"Graph exported to {output_path}.png")
