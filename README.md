# ✈️ AERONET — Airline Route Network & Airport Connectivity Analytics

**A Big Data & Graph Analytics pipeline that turns the global airline route network into an explorable, interactive intelligence dashboard.**

Built on the OpenFlights dataset, AERONET processes millions of airline routes through Hadoop HDFS and Apache Spark, models the network as a graph in Neo4j, and surfaces the results through a Streamlit dashboard — from the busiest hub airports to the shortest path between any two airports on Earth.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Dashboard](#dashboard)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dataset](#dataset)
- [Results & Insights](#results--insights)
- [Future Scope](#future-scope)
- [Author](#author)

---

## Overview

Airline networks aren't really tables of routes — they're graphs. An airport's importance isn't just how many flights it handles, but *where it sits* in the web of connections that link the rest of the world together. Spotting that kind of structure in a spreadsheet is nearly impossible; spotting it in a graph is what graph theory is built for.

**AERONET** analyzes airline routes, airports, and airlines from the OpenFlights dataset using a combination of:

- **Big Data processing** (Hadoop HDFS + Apache Spark/PySpark) for scalable ingestion and cleaning
- **Feature engineering** to derive route counts, connectivity scores, and route characteristics
- **Graph analytics** (Neo4j + Neo4j Graph Data Science) to compute PageRank, Degree Centrality, Betweenness Centrality, and shortest paths
- **Interactive visualization** (Streamlit + Plotly) to explore the results through a live dashboard

The result is a system that can answer questions a plain CSV never could — *which airports quietly hold the whole network together?*

## Problem Statement

Airline networks contain a large number of airports, airlines, and connections between them. Analyzing a network this size with only traditional tabular methods makes it difficult to see how airports relate to one another or which ones matter most structurally.

This project builds a Big Data pipeline that processes airline network data end-to-end and surfaces patterns such as:

- Highly connected airports
- Airlines with the largest route networks
- Frequently used airport-to-airport connections
- Geographic distribution of airports worldwide
- Structurally important airports in the network
- Airports acting as connecting "bridges" between regions
- Shortest paths between any two airports

The project combines traditional data analytics with graph-based analytics to study the network from both angles.

## Objectives

1. Store airline network data using Hadoop HDFS
2. Process large airline datasets using PySpark
3. Clean and transform airline, airport, and route data
4. Perform exploratory data analysis on the datasets
5. Identify highly connected airports
6. Analyze airline route activity
7. Analyze frequently occurring airport-to-airport routes
8. Perform geographic analysis using airport coordinates
9. Engineer meaningful features from the processed data
10. Represent the airline route network as a graph in Neo4j
11. Perform graph analytics using Neo4j Graph Data Science
12. Calculate Degree Centrality, PageRank, and Betweenness Centrality
13. Find shortest paths between airports
14. Present all results through an interactive Streamlit dashboard

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Storage | **Hadoop HDFS** | Distributed storage for raw and processed data |
| Processing | **Apache Spark / PySpark** | Large-scale data cleaning, transformation, and analytics |
| Data handling | **Pandas / NumPy** | In-memory data handling and numerical operations |
| Data Science | **Scikit-learn** | Supporting feature engineering and analysis |
| Graph Database | **Neo4j** | Storing the route network as a graph |
| Graph Analytics | **Neo4j Graph Data Science** | PageRank, Centrality, and Shortest Path algorithms |
| Dashboard | **Streamlit** | Interactive web application layer |
| Visualization | **Plotly / Matplotlib** | Charts, maps, and graph visualizations |
| Config | **python-dotenv** | Environment variable management |
| Language | **Python** | End-to-end pipeline implementation |

## Architecture

```text
                    OpenFlights Dataset
                           |
                           v
                    Raw CSV Files
                           |
                           v
                       HDFS
                           |
                           v
                  PySpark Processing
                           |
             +-------------+-------------+
             |                           |
             v                           v
      Data Preprocessing          Data Transformation
             |                           |
             +-------------+-------------+
                           |
                           v
                    Processed Data
                           |
             +-------------+-------------+
             |                           |
             v                           v
      PySpark Analysis          Feature Engineering
             |                           |
             +-------------+-------------+
                           |
                           v
                     Neo4j Graph
                           |
                           v
                  Graph Data Science
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          PageRank     Betweenness    Degree
                       Centrality     Centrality
                           |
                           v
                    Shortest Path
                           |
                           v
                Analytical Results
                           |
                           v
                 Streamlit Dashboard
```

**Pipeline stages, in short:**

1. **Ingest** — raw OpenFlights CSVs land in HDFS
2. **Clean** — PySpark handles missing values, duplicates, and type conversion
3. **Analyze & Engineer** — PySpark computes route/airport/airline-level statistics and features
4. **Graph** — the cleaned network is imported into Neo4j
5. **Score** — Neo4j Graph Data Science runs PageRank, Degree Centrality, Betweenness Centrality, and Shortest Path
6. **Visualize** — every result is served through the Streamlit dashboard

## Dashboard

The dashboard is organized into five focused views:

| Page | What it shows |
|---|---|
| 🛰️ **Command Deck** | Network-wide overview — total routes, airports, airlines, and countries, plus top carriers, top hubs, and busiest destinations |
| 🛫 **Flight Paths** | Route-level analysis — top airlines by route volume, top airports by connectivity, and the underlying route feature table |
| 🗺️ **Terminal Map** | Airport & geographic analysis — connectivity rankings and a global map of every airport in the network |
| ✈️ **Carrier Fleet** | Airline-level analysis — route activity and distribution across carriers |
| 🕸️ **Network Core** | Graph analytics — PageRank, Degree Centrality, Betweenness Centrality, and shortest-path lookups |

Run it with:

```bash
streamlit run dashboard/app.py
```

## Project Structure

```text
airline-route-bda/
│
├── data/
│   │
│   ├── raw/
│   │   ├── airlines.csv
│   │   ├── airports.csv
│   │   └── routes.csv
│   │
│   ├── processed/
│   │   ├── airlines_clean/
│   │   ├── airports_clean/
│   │   └── routes_clean/
│   │
│   └── output/
│       │
│       ├── route_analysis/
│       ├── airport_analysis/
│       ├── airline_analysis/
│       ├── geographic_analysis/
│       └── graph_analysis/
│
├── hdfs/
│
├── src/
│   │
│   ├── preprocessing/
│   │   ├── load_airlines.py
│   │   ├── load_airports.py
│   │   └── load_routes.py
│   │
│   ├── analysis/
│   │   ├── route_analysis.py
│   │   ├── airport_analysis.py
│   │   ├── airline_analysis.py
│   │   └── geographic_analysis.py
│   │
│   ├── features/
│   │   ├── airport_features.py
│   │   ├── airline_features.py
│   │   └── route_features.py
│   │
│   ├── spark/
│   │
│   └── neo4j/
│       ├── connection.py
│       └── import_graph.py
│
├── dashboard/
│   └── app.py
│
├── config/
│   └── .env
│
├── requirements.txt
├── .gitignore
└── README.md
```

**What lives where:**

- **`data/raw/`** — untouched OpenFlights source files
- **`data/processed/`** — cleaned, typed data written by the `preprocessing/` scripts
- **`data/output/`** — final analytical results, one folder per analysis type, consumed directly by the dashboard
- **`hdfs/`** — local HDFS working directory (data node storage, checkpoints, etc.)
- **`src/preprocessing/`** — loads and cleans each raw dataset (airlines, airports, routes)
- **`src/analysis/`** — PySpark scripts for route, airport, airline, and geographic analysis
- **`src/features/`** — feature engineering scripts that produce the tables the dashboard reads
- **`src/spark/`** — shared Spark session setup and utilities
- **`src/neo4j/`** — Neo4j connection handling and graph import logic
- **`dashboard/app.py`** — the Streamlit dashboard
- **`config/.env`** — environment variables (Neo4j credentials, Spark config, file paths — not committed to version control)

## Getting Started

### Prerequisites

- Python 3.9+
- Hadoop (with HDFS running locally or on a cluster)
- Apache Spark
- **Neo4j Desktop 2**, with the **Graph Data Science** plugin installed (see [step 6](#6-set-up-neo4j-desktop-2) below)
- pip / virtualenv

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/airline-route-bda.git
cd airline-route-bda
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `config/.env` with your local settings:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
HDFS_NAMENODE=hdfs://localhost:9000
```

### 5. Place the raw data

Download the OpenFlights `airlines.csv`, `airports.csv`, and `routes.csv` into `data/raw/`.

### 6. Set up Neo4j Desktop 2

This project's graph analytics stage (PageRank, Degree/Betweenness Centrality, Shortest Path) runs through **Neo4j Graph Data Science**, which needs a running Neo4j instance. The easiest way to get one locally is Neo4j Desktop 2:

1. **Install Neo4j Desktop 2** from [neo4j.com/download](https://neo4j.com/download/) and sign in (a free Neo4j account is required to activate it).
2. **Create a new Project** — click **New Project** in the left sidebar and give it a name (e.g. `airline-route-bda`).
3. **Add a local DBMS** — inside the project, click **Add** → **Local DBMS**. Give it a name, set a password (you'll need this for `.env`), and choose a Neo4j version (5.x is recommended for GDS compatibility).
4. **Install the Graph Data Science plugin** — select your new DBMS, go to the **Plugins** tab in the right-hand panel, find **Graph Data Science Library**, and click **Install**. This adds the `gds.*` procedures used by `src/neo4j/import_graph.py` and the centrality/PageRank calculations.
5. **Start the DBMS** — click **Start** on the DBMS card. Once it shows **Active**, you can open **Neo4j Browser** from the same card to confirm it's running (try `RETURN 1;`).
6. **Get your connection details** — with the DBMS active, click the three-dot menu → **Terminal**, or check the DBMS details panel, for the Bolt connection URI. By default this is:

   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=<the password you set in step 3>
   ```

   Update `config/.env` with these values.
7. **Verify the GDS plugin loaded correctly** — in Neo4j Browser, run:

   ```cypher
   RETURN gds.version();
   ```

   If this returns a version string, the plugin is active and `src/neo4j/import_graph.py` (and the PageRank/Centrality scripts) will be able to call it.
8. **Import the graph** — once the DBMS is active and reachable, run the import script from [Usage](#usage) below to load the cleaned route network into Neo4j as nodes (airports) and relationships (routes).

> 💡 **Tip:** Keep the DBMS running in Neo4j Desktop while you run any script under `src/neo4j/` or while the **Network Core** page of the dashboard is open — the dashboard reads Neo4j's graph algorithm outputs (PageRank, Centrality, Shortest Path) live via the Bolt connection.

## Usage

Run the pipeline stages in order:

```bash
# 1. Load and clean raw data
python src/preprocessing/load_airlines.py
python src/preprocessing/load_airports.py
python src/preprocessing/load_routes.py

# 2. Run analysis
python src/analysis/route_analysis.py
python src/analysis/airport_analysis.py
python src/analysis/airline_analysis.py
python src/analysis/geographic_analysis.py

# 3. Engineer features
python src/features/airport_features.py
python src/features/airline_features.py
python src/features/route_features.py

# 4. Import the network into Neo4j
python src/neo4j/import_graph.py

# 5. Launch the dashboard
streamlit run dashboard/app.py
```

## Dataset

This project uses the **[OpenFlights](https://openflights.org/data.php)** dataset:

- **`airlines.csv`** — airline names, codes, and countries
- **`airports.csv`** — airport names, IATA/ICAO codes, cities, countries, and coordinates
- **`routes.csv`** — source and destination airports for each route, by airline

## Results & Insights

Once the pipeline has run, the dashboard surfaces insights such as:

- The airports with the highest **PageRank** — the ones the network structurally depends on most
- **Betweenness Centrality** leaders — airports that act as bridges between otherwise distant regions
- The most connected airports and airlines by raw route count
- The shortest path between any two airports in the network
- The global geographic spread of airports across countries and continents

## Future Scope

- Incorporate real-time flight data for live network monitoring
- Add delay and cancellation data to weight routes by reliability
- Extend graph analytics with community detection (e.g., Louvain) to identify regional clusters
- Deploy the dashboard for public access
- Add predictive modeling for route demand forecasting

## Author

**Karan**
Final-year Computer Engineering student, University of Mumbai
Project area: Big Data Analytics, Graph Analytics, and Machine Learning

---

*Built with Python, PySpark, Neo4j, and Streamlit.*