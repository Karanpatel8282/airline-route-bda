import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ASTRA | Airline Network Intelligence",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

ROUTE_PATH = Path("data/output/route_analysis")
AIRPORT_ANALYSIS_PATH = Path("data/output/airport_analysis")
AIRLINE_ANALYSIS_PATH = Path("data/output/airline_analysis")
GRAPH_PATH = Path("data/output/graph_analysis")

AIRPORT_DATA_PATH = Path("data/processed/airports_clean")
AIRLINE_DATA_PATH = Path("data/processed/airlines_clean")
ROUTES_DATA_PATH = Path("data/processed/routes_clean")


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #071525;
        color: #F4F8FC;
    }

    [data-testid="stSidebar"] {
        background: #091B2D;
        border-right: 1px solid #173653;
    }

    [data-testid="stSidebar"] * {
        color: #DCEAF7;
    }

    .sidebar-brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 3px;
        color: #F4F8FC;
    }

    .sidebar-subtitle {
        color: #55C7F5;
        font-size: 10px;
        letter-spacing: 2px;
        margin-top: 4px;
        margin-bottom: 28px;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 4px;
        color: #F4F8FC;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #55C7F5;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 2px;
        margin-top: 5px;
        margin-bottom: 28px;
    }

    .kpi-card {
        background: linear-gradient(145deg, #102A43, #0B1D32);
        border: 1px solid #1A4564;
        border-radius: 16px;
        padding: 20px;
        min-height: 115px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.22);
    }

    .kpi-label {
        color: #8FA9BF;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .kpi-value {
        color: #F4F8FC;
        font-size: 30px;
        font-weight: 800;
        margin-top: 7px;
    }

    .kpi-accent {
        color: #55C7F5;
        font-size: 11px;
        margin-top: 4px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 700;
        color: #F4F8FC;
        margin-top: 20px;
    }

    .section-caption {
        color: #8FA9BF;
        font-size: 13px;
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
        background: #0D243B;
        border: 1px solid #1A4564;
        border-radius: 14px;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #8FA9BF;
    }

    div[data-testid="stMetricValue"] {
        color: #F4F8FC;
    }

    div[role="radiogroup"] {
        gap: 6px;
    }

    div[role="radiogroup"] label {
        background: #0D243B;
        border-radius: 9px;
        padding: 7px 10px;
        border: 1px solid transparent;
    }

    div[role="radiogroup"] label:hover {
        border: 1px solid #26719A;
    }

    .status {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 20px;
        background: #10364A;
        color: #65D5F7;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .5px;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #173B57;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        background: #0D2942;
        border: 1px solid #1B4E70;
        border-radius: 12px;
    }

    hr {
        border-color: #173653;
    }

    div[data-testid="stPlotlyChart"] {
        background: #0A1B2D;
        border: 1px solid #153850;
        border-radius: 14px;
        padding: 5px;
    }

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #071525;
    }

    ::-webkit-scrollbar-thumb {
        background: #214A66;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

def read_spark_csv(folder):

    folder = Path(folder)

    if not folder.exists():
        return pd.DataFrame()

    if not folder.is_dir():
        return pd.DataFrame()

    files = sorted(folder.glob("part-*.csv"))

    if not files:
        return pd.DataFrame()

    dataframes = []

    for file in files:
        try:
            df = pd.read_csv(file)

            if not df.empty:
                dataframes.append(df)

        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(
        dataframes,
        ignore_index=True
    )


def read_csv_file(file):

    file = Path(file)

    if not file.exists():
        return pd.DataFrame()

    if not file.is_file():
        return pd.DataFrame()

    try:
        return pd.read_csv(file)

    except Exception as e:
        print(f"Error reading {file}: {e}")
        return pd.DataFrame()


def read_data(path):

    path = Path(path)

    if path.is_file():
        return read_csv_file(path)

    if path.is_dir():
        return read_spark_csv(path)

    return pd.DataFrame()


# ============================================================
# LOAD MAIN DATA
# ============================================================

airports_data = read_data(AIRPORT_DATA_PATH)
airlines_data = read_data(AIRLINE_DATA_PATH)
routes_data = read_data(ROUTES_DATA_PATH)


# ============================================================
# LOAD ANALYSIS DATA
# ============================================================

top_airlines = read_data(
    ROUTE_PATH / "top_airlines.csv"
)

top_source_airports = read_data(
    ROUTE_PATH / "top_source_airports.csv"
)

top_destination_airports = read_data(
    ROUTE_PATH / "top_destination_airports.csv"
)

route_features = read_data(
    ROUTE_PATH / "route_features"
)

airline_features = read_data(
    AIRLINE_ANALYSIS_PATH / "airline_features"
)

airport_features = read_data(
    AIRPORT_ANALYSIS_PATH / "airport_features"
)


# ============================================================
# GRAPH DATA
# ============================================================

pagerank = read_data(
    GRAPH_PATH / "pagerank.csv"
)

degree = read_data(
    GRAPH_PATH / "degree_centrality.csv"
)

betweenness = read_data(
    GRAPH_PATH / "betweenness_centrality.csv"
)

shortest_path = read_data(
    GRAPH_PATH / "shortest_path.csv"
)


# ============================================================
# DYNAMIC KPI VALUES
# ============================================================

total_routes = len(routes_data)
total_airports = len(airports_data)
total_airlines = len(airlines_data)

if not route_features.empty:
    connections = len(route_features)
else:
    connections = 0

if "country" in airports_data.columns:

    countries = (
        airports_data["country"]
        .replace(["\\N", "", "NULL", "null"], pd.NA)
        .dropna()
        .nunique()
    )

else:

    countries = 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">ASTRA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">AIRLINE NETWORK INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Route Analysis",
            "Airport & Geography",
            "Airline Analysis",
            "Graph Analytics"
        ]
    )

    st.markdown("---")

    st.markdown(
        '<div class="status">DATA SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )

    st.caption("Big Data Analytics")
    st.caption("PySpark + HDFS + Neo4j")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">ASTRA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AIRLINE ROUTE NETWORK & AIRPORT CONNECTIVITY ANALYTICS</div>',
    unsafe_allow_html=True
)


# ============================================================
# GLOBAL KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Routes</div>
            <div class="kpi-value">{total_routes:,}</div>
            <div class="kpi-accent">Airline route records</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Airports</div>
            <div class="kpi-value">{total_airports:,}</div>
            <div class="kpi-accent">Global airport network</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Airlines</div>
            <div class="kpi-value">{total_airlines:,}</div>
            <div class="kpi-accent">Airline records</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Connections</div>
            <div class="kpi-value">{connections:,}</div>
            <div class="kpi-accent">Unique airport pairs</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">Network Intelligence Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">High-level overview of the airline route network</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # OVERVIEW METRICS
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Total Routes",
            f"{total_routes:,}"
        )

    with m2:
        st.metric(
            "Airports",
            f"{total_airports:,}"
        )

    with m3:
        st.metric(
            "Airlines",
            f"{total_airlines:,}"
        )

    with m4:
        st.metric(
            "Countries",
            f"{countries:,}"
        )


    # ========================================================
    # TOP AIRLINES GRAPH
    # ========================================================

    st.markdown("### Top Airlines")

    if not airline_features.empty:

        overview_airlines = airline_features.copy()

        if (
            "airline" in overview_airlines.columns
            and "total_routes" in overview_airlines.columns
        ):

            overview_airlines["total_routes"] = pd.to_numeric(
                overview_airlines["total_routes"],
                errors="coerce"
            )

            overview_airlines = overview_airlines.dropna(
                subset=["total_routes"]
            )

            overview_airlines = (
                overview_airlines
                .sort_values(
                    "total_routes",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                overview_airlines,
                x="airline",
                y="total_routes",
                title="Top 10 Airlines by Total Routes",
                text="total_routes"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Airline",
                yaxis_title="Total Routes",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Airline feature data does not contain the expected columns."
            )

            st.write(
                "Available columns:",
                list(airline_features.columns)
            )

    else:

        st.error(
            "Airline feature data could not be loaded."
        )


    # ========================================================
    # TOP AIRPORT HUBS GRAPH
    # ========================================================

    st.markdown("### Top Airport Hubs")

    if not airport_features.empty:

        overview_airports = airport_features.copy()

        if (
            "airport" in overview_airports.columns
            and "total_connectivity" in overview_airports.columns
        ):

            overview_airports["total_connectivity"] = pd.to_numeric(
                overview_airports["total_connectivity"],
                errors="coerce"
            )

            overview_airports = overview_airports.dropna(
                subset=["total_connectivity"]
            )

            overview_airports = (
                overview_airports
                .sort_values(
                    "total_connectivity",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                overview_airports,
                x="airport",
                y="total_connectivity",
                title="Top 10 Airports by Connectivity",
                text="total_connectivity"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="Total Connectivity",
                height=450
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Airport feature data does not contain the expected columns."
            )

            st.write(
                "Available columns:",
                list(airport_features.columns)
            )

    else:

        st.error(
            "Airport feature data could not be loaded."
        )
        # ========================================================
    # MOST CONNECTED DESTINATIONS
    # ========================================================

    st.markdown("### Most Connected Destinations")

    if routes_data.empty:

        st.error("Routes data could not be loaded.")

    elif "destination_airport" not in routes_data.columns:

        st.error(
            "The destination_airport column was not found."
        )

        st.write(
            "Available route columns:",
            list(routes_data.columns)
        )

    else:

        destination_df = routes_data[
            ["destination_airport"]
        ].copy()

        destination_df["destination_airport"] = (
            destination_df["destination_airport"]
            .astype(str)
            .str.strip()
        )

        destination_df = destination_df[
            ~destination_df["destination_airport"].isin(
                [
                    "",
                    "\\N",
                    "nan",
                    "None",
                    "NULL",
                    "null"
                ]
            )
        ]

        destination_counts = (
            destination_df["destination_airport"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        destination_counts.columns = [
            "Destination Airport",
            "Incoming Routes"
        ]

        if not destination_counts.empty:

            fig = px.bar(
                destination_counts,
                x="Destination Airport",
                y="Incoming Routes",
                title="Top 10 Airports by Incoming Routes",
                text="Incoming Routes"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                height=450,
                xaxis_title="Destination Airport",
                yaxis_title="Incoming Routes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No destination airport data available."
            )

    # ========================================================
    # PIPELINE
    # ========================================================

    st.info(
        "Pipeline: Raw CSV → HDFS → PySpark → Data Cleaning → "
        "Feature Engineering → Neo4j Graph Analytics → Dashboard"
    )


# ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.markdown(
        '<div class="section-title">Route Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Analysis of airline routes and airport connections</div>',
        unsafe_allow_html=True
    )


    r1, r2, r3 = st.columns(3)

    with r1:

        st.metric(
            "Total Routes",
            f"{total_routes:,}"
        )


    with r2:

        top_airline = "N/A"

        if not airline_features.empty:

            if (
                "airline" in airline_features.columns
                and "total_routes" in airline_features.columns
            ):

                temp = airline_features.copy()

                temp["total_routes"] = pd.to_numeric(
                    temp["total_routes"],
                    errors="coerce"
                )

                temp = temp.dropna(
                    subset=["total_routes"]
                )

                if not temp.empty:

                    top_airline = (
                        temp
                        .sort_values(
                            "total_routes",
                            ascending=False
                        )
                        .iloc[0]["airline"]
                    )

        st.metric(
            "Top Airline",
            top_airline
        )


    with r3:

        top_airport = "N/A"

        if not airport_features.empty:

            if (
                "airport" in airport_features.columns
                and "total_connectivity" in airport_features.columns
            ):

                temp = airport_features.copy()

                temp["total_connectivity"] = pd.to_numeric(
                    temp["total_connectivity"],
                    errors="coerce"
                )

                temp = temp.dropna(
                    subset=["total_connectivity"]
                )

                if not temp.empty:

                    top_airport = (
                        temp
                        .sort_values(
                            "total_connectivity",
                            ascending=False
                        )
                        .iloc[0]["airport"]
                    )

        st.metric(
            "Top Airport",
            top_airport
        )


    # --------------------------------------------------------
    # AIRLINE FEATURE
    # --------------------------------------------------------

    st.markdown("### Airline Route Feature")

    if not airline_features.empty:

        if (
            "airline" in airline_features.columns
            and "total_routes" in airline_features.columns
        ):

            chart_df = airline_features.copy()

            chart_df["total_routes"] = pd.to_numeric(
                chart_df["total_routes"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["total_routes"]
            )

            chart_df = (
                chart_df
                .sort_values(
                    "total_routes",
                    ascending=False
                )
                .head(15)
            )

            fig = px.bar(
                chart_df,
                x="airline",
                y="total_routes",
                title="Top Airlines by Total Routes"
            )

            fig.update_layout(
                xaxis_title="Airline",
                yaxis_title="Total Routes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # --------------------------------------------------------
    # AIRPORT FEATURE
    # --------------------------------------------------------

    st.markdown("### Airport Connectivity Feature")

    if not airport_features.empty:

        if (
            "airport" in airport_features.columns
            and "total_connectivity" in airport_features.columns
        ):

            chart_df = airport_features.copy()

            chart_df["total_connectivity"] = pd.to_numeric(
                chart_df["total_connectivity"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["total_connectivity"]
            )

            chart_df = (
                chart_df
                .sort_values(
                    "total_connectivity",
                    ascending=False
                )
                .head(15)
            )

            fig = px.bar(
                chart_df,
                x="airport",
                y="total_connectivity",
                title="Top Airports by Connectivity"
            )

            fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="Total Connectivity"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # --------------------------------------------------------
    # ROUTE FEATURE TABLE
    # --------------------------------------------------------

    st.markdown("### Route Features")

    if not route_features.empty:

        st.dataframe(
            route_features,
            use_container_width=True
        )


# ============================================================
# AIRPORT & GEOGRAPHY
# ============================================================

elif page == "Airport & Geography":

    st.markdown(
        '<div class="section-title">Airport & Geography</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Airport connectivity and geographical distribution</div>',
        unsafe_allow_html=True
    )


    a1, a2, a3 = st.columns(3)

    with a1:

        st.metric(
            "Total Airports",
            f"{total_airports:,}"
        )


    with a2:

        st.metric(
            "Countries",
            f"{countries:,}"
        )


    with a3:

        most_connected = "N/A"

        if not airport_features.empty:

            if (
                "airport" in airport_features.columns
                and "total_connectivity" in airport_features.columns
            ):

                temp = airport_features.copy()

                temp["total_connectivity"] = pd.to_numeric(
                    temp["total_connectivity"],
                    errors="coerce"
                )

                temp = temp.dropna(
                    subset=["total_connectivity"]
                )

                if not temp.empty:

                    most_connected = (
                        temp
                        .sort_values(
                            "total_connectivity",
                            ascending=False
                        )
                        .iloc[0]["airport"]
                    )

        st.metric(
            "Most Connected Airport",
            most_connected
        )


    # --------------------------------------------------------
    # CONNECTIVITY GRAPH
    # --------------------------------------------------------

    st.markdown("### Airport Connectivity")

    if not airport_features.empty:

        if (
            "airport" in airport_features.columns
            and "total_connectivity" in airport_features.columns
        ):

            chart_df = airport_features.copy()

            chart_df["total_connectivity"] = pd.to_numeric(
                chart_df["total_connectivity"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["total_connectivity"]
            )

            chart_df = (
                chart_df
                .sort_values(
                    "total_connectivity",
                    ascending=False
                )
                .head(15)
            )

            fig = px.bar(
                chart_df,
                x="airport",
                y="total_connectivity",
                title="Top 15 Airports by Connectivity"
            )

            fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="Total Connectivity"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # --------------------------------------------------------
    # GLOBAL MAP
    # --------------------------------------------------------

    st.markdown("### Global Airport Distribution")

    if not airports_data.empty:

        map_df = airports_data.copy()

        if (
            "latitude" in map_df.columns
            and "longitude" in map_df.columns
        ):

            map_df["latitude"] = pd.to_numeric(
                map_df["latitude"],
                errors="coerce"
            )

            map_df["longitude"] = pd.to_numeric(
                map_df["longitude"],
                errors="coerce"
            )

            map_df = map_df.dropna(
                subset=[
                    "latitude",
                    "longitude"
                ]
            )

            fig = px.scatter_geo(
                map_df,
                lat="latitude",
                lon="longitude",
                hover_name="name",
                hover_data=[
                    "city",
                    "country"
                ],
                title="Global Airport Distribution"
            )

            fig.update_layout(
                geo=dict(
                    showland=True
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    st.markdown("### Airport Feature Data")

    if not airport_features.empty:

        st.dataframe(
            airport_features,
            use_container_width=True
        )


# ============================================================
# AIRLINE ANALYSIS
# ============================================================

elif page == "Airline Analysis":

    st.markdown(
        '<div class="section-title">Airline Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Airline distribution and route activity</div>',
        unsafe_allow_html=True
    )


    al1, al2, al3 = st.columns(3)

    with al1:

        st.metric(
            "Total Airlines",
            f"{total_airlines:,}"
        )


    with al2:

        top_airline_name = "N/A"

        if not airline_features.empty:

            if (
                "airline" in airline_features.columns
                and "total_routes" in airline_features.columns
            ):

                temp = airline_features.copy()

                temp["total_routes"] = pd.to_numeric(
                    temp["total_routes"],
                    errors="coerce"
                )

                temp = temp.dropna(
                    subset=["total_routes"]
                )

                if not temp.empty:

                    top_airline_name = (
                        temp
                        .sort_values(
                            "total_routes",
                            ascending=False
                        )
                        .iloc[0]["airline"]
                    )

        st.metric(
            "Top Airline",
            top_airline_name
        )


    with al3:

        top_routes = 0

        if not airline_features.empty:

            if "total_routes" in airline_features.columns:

                temp = airline_features.copy()

                temp["total_routes"] = pd.to_numeric(
                    temp["total_routes"],
                    errors="coerce"
                )

                temp = temp.dropna(
                    subset=["total_routes"]
                )

                if not temp.empty:

                    top_routes = int(
                        temp
                        .sort_values(
                            "total_routes",
                            ascending=False
                        )
                        .iloc[0]["total_routes"]
                    )

        st.metric(
            "Top Airline Routes",
            f"{top_routes:,}"
        )


    # --------------------------------------------------------
    # AIRLINE GRAPH
    # --------------------------------------------------------

    st.markdown("### Airline Route Features")

    if not airline_features.empty:

        if (
            "airline" in airline_features.columns
            and "total_routes" in airline_features.columns
        ):

            chart_df = airline_features.copy()

            chart_df["total_routes"] = pd.to_numeric(
                chart_df["total_routes"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["total_routes"]
            )

            chart_df = (
                chart_df
                .sort_values(
                    "total_routes",
                    ascending=False
                )
                .head(15)
            )

            fig = px.bar(
                chart_df,
                x="airline",
                y="total_routes",
                title="Top 15 Airlines by Total Routes"
            )

            fig.update_layout(
                xaxis_title="Airline",
                yaxis_title="Total Routes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    st.markdown("### Airline Feature Data")

    if not airline_features.empty:

        st.dataframe(
            airline_features,
            use_container_width=True
        )


# ============================================================
# GRAPH ANALYTICS
# ============================================================

elif page == "Graph Analytics":

    st.markdown(
        '<div class="section-title">Graph Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Neo4j graph-based analysis of the airline network</div>',
        unsafe_allow_html=True
    )


    g1, g2, g3, g4 = st.columns(4)

    with g1:

        st.metric(
            "Airport Nodes",
            f"{total_airports:,}"
        )

    with g2:

        st.metric(
            "Route Relationships",
            f"{total_routes:,}"
        )

    with g3:

        st.metric(
            "Airline Nodes",
            f"{total_airlines:,}"
        )

    with g4:

        st.metric(
            "Graph Engine",
            "Neo4j"
        )


    # --------------------------------------------------------
    # PAGERANK
    # --------------------------------------------------------

    st.markdown("### PageRank")

    if not pagerank.empty:

        if "pagerank" in pagerank.columns:

            chart_df = pagerank.copy()

            chart_df["pagerank"] = pd.to_numeric(
                chart_df["pagerank"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["pagerank"]
            )

            chart_df = (
                chart_df
                .sort_values(
                    "pagerank",
                    ascending=False
                )
                .head(10)
            )

            x_column = (
                "iata"
                if "iata" in chart_df.columns
                else "airport_name"
            )

            fig = px.bar(
                chart_df,
                x=x_column,
                y="pagerank",
                title="Top Airports by PageRank"
            )

            fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="PageRank Score"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.dataframe(
            pagerank,
            use_container_width=True
        )


    # --------------------------------------------------------
    # DEGREE CENTRALITY
    # --------------------------------------------------------

    st.markdown("### Degree Centrality")

    if not degree.empty:

        degree_column = None

        for column in [
            "degree",
            "degree_centrality",
            "total_degree"
        ]:

            if column in degree.columns:

                degree_column = column
                break


        if degree_column:

            chart_df = degree.copy()

            chart_df[degree_column] = pd.to_numeric(
                chart_df[degree_column],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=[degree_column]
            )

            chart_df = (
                chart_df
                .sort_values(
                    degree_column,
                    ascending=False
                )
                .head(10)
            )

            x_column = (
                "iata"
                if "iata" in chart_df.columns
                else "airport_name"
            )

            fig = px.bar(
                chart_df,
                x=x_column,
                y=degree_column,
                title="Top Airports by Degree Centrality"
            )

            fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="Degree"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.dataframe(
            degree,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BETWEENNESS CENTRALITY
    # --------------------------------------------------------

    st.markdown("### Betweenness Centrality")

    if not betweenness.empty:

        if "betweenness" in betweenness.columns:

            chart_df = betweenness.copy()

            chart_df["betweenness"] = pd.to_numeric(
                chart_df["betweenness"],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["betweenness"]
            )

            chart_df = (
                chart_df
                .sort_values(
                    "betweenness",
                    ascending=False
                )
                .head(10)
            )

            x_column = (
                "iata"
                if "iata" in chart_df.columns
                else "airport_name"
            )

            fig = px.bar(
                chart_df,
                x=x_column,
                y="betweenness",
                title="Top Airports by Betweenness Centrality"
            )

            fig.update_layout(
                xaxis_title="Airport",
                yaxis_title="Betweenness Score"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.dataframe(
            betweenness,
            use_container_width=True
        )


    # --------------------------------------------------------
    # SHORTEST PATH
    # --------------------------------------------------------

    st.markdown("### Shortest Path")

    if not shortest_path.empty:

        st.dataframe(
            shortest_path,
            use_container_width=True
        )