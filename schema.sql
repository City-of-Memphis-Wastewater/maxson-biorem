-- nodes table
CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,       -- 'component', 'sensor', 'tank', etc.
    name TEXT NOT NULL UNIQUE,
    metadata JSON DEFAULT '{}' -- additional properties in JSON
);

-- edges table (graph relationships)
CREATE TABLE IF NOT EXISTS edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id INTEGER NOT NULL,
    to_id INTEGER NOT NULL,
    type TEXT NOT NULL,        -- 'HAS_SENSOR', 'CONNECTED_TO', 'MEASURES', etc.
    properties JSON DEFAULT '{}',
    FOREIGN KEY(from_id) REFERENCES nodes(id),
    FOREIGN KEY(to_id) REFERENCES nodes(id)
    UNIQUE(from_id, to_id, type)  -- ensures no duplicates
);


-- readings table for sensors
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    value REAL NOT NULL,
    FOREIGN KEY(node_id) REFERENCES nodes(id)
    UNIQUE(node_id, timestamp)  -- prevents multiple readings at the same timestamp
);

-- events table for issues or alerts
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL,       -- 'failure', 'alert', 'maintenance'
    description TEXT,
    FOREIGN KEY(node_id) REFERENCES nodes(id)
    UNIQUE(node_id, timestamp, type)  -- prevents duplicate events  at the same timestamp
);
