def main():
    print("Hello from maxson-biorem!")
    import sqlite3
    import networkx as nx
    from prettytable import PrettyTable
    from datetime import datetime

    # -----------------------------
    # 1. Setup DB
    # -----------------------------
    conn = sqlite3.connect("biorem.db")
    cur = conn.cursor()

    # Create tables if not exist
    with open("schema.sql", "r") as f:
        cur.executescript(f.read())

    conn.commit()

    # -----------------------------
    # 2. Insert nodes
    # -----------------------------
    nodes = [
        ('component', 'Pump1', '{"capacity":100}'),
        ('sensor', 'FlowMeter1', '{"unit":"L/min"}'),
        ('tank', 'Tank1', '{"volume":500}')
    ]

    cur.executemany("INSERT OR IGNORE INTO nodes (type, name, metadata) VALUES (?, ?, ?)", nodes)
    conn.commit()

    # Fetch node IDs
    cur.execute("SELECT id, name FROM nodes")
    node_ids = {name: nid for nid, name in cur.fetchall()}

    # -----------------------------
    # 3. Insert edges
    # -----------------------------
    edges = [
        (node_ids['Pump1'], node_ids['FlowMeter1'], 'HAS_SENSOR', '{"status":"active"}'),
        (node_ids['FlowMeter1'], node_ids['Tank1'], 'MEASURES', '{"flow_rate":50}')
    ]
    cur.executemany("INSERT INTO edges (from_id, to_id, type, properties) VALUES (?, ?, ?, ?)", edges)
    conn.commit()

    # -----------------------------
    # 4. Insert sensor readings
    # -----------------------------
    readings = [
        (node_ids['FlowMeter1'], 48.5),
        (node_ids['FlowMeter1'], 49.2)
    ]
    cur.executemany("INSERT INTO readings (node_id, value) VALUES (?, ?)", readings)
    conn.commit()

    # -----------------------------
    # 5. Graph Traversal using NetworkX
    # -----------------------------
    G = nx.DiGraph()

    # Add nodes
    cur.execute("SELECT id, name FROM nodes")
    for nid, name in cur.fetchall():
        G.add_node(nid, label=name)

    # Add edges
    cur.execute("SELECT from_id, to_id, type FROM edges")
    for f, t, etype in cur.fetchall():
        G.add_edge(f, t, type=etype)

    # Example: Find all downstream nodes from Pump1
    pump_id = node_ids['Pump1']
    downstream = nx.descendants(G, pump_id)

    table = PrettyTable(['Node', 'Type'])
    for nid in downstream:
        cur.execute("SELECT name, type FROM nodes WHERE id=?", (nid,))
        name, ntype = cur.fetchone()
        table.add_row([name, ntype])

    print("Downstream nodes from Pump1:")
    print(table)

    # -----------------------------
    # 6. Example: Sensor readings
    # -----------------------------
    cur.execute("SELECT timestamp, value FROM readings WHERE node_id=?", (node_ids['FlowMeter1'],))
    print("\nFlowMeter1 readings:")
    for ts, val in cur.fetchall():
        print(f"{ts}: {val} L/min")

    conn.close()

if __name__ == "__main__":
    main()
