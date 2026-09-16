import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


# ============================================================
# GLOBAL PLOTLY THEME (AERONET / blended aviation palette)
# ============================================================

pio.templates["aeronet"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#DCE3F2", size=13),
        title=dict(font=dict(size=17, color="#F1F4FA", family="Sora, sans-serif")),
        colorway=[
            "#22D3EE", "#818CF8", "#A78BFA", "#2DD4BF",
            "#67E8F9", "#C4B5FD", "#5EEAD4", "#93C5FD"
        ],
        xaxis=dict(
            gridcolor="rgba(129,140,248,0.10)",
            linecolor="#243252",
            zerolinecolor="#243252",
            tickfont=dict(color="#8993AB")
        ),
        yaxis=dict(
            gridcolor="rgba(129,140,248,0.10)",
            linecolor="#243252",
            zerolinecolor="#243252",
            tickfont=dict(color="#8993AB")
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=55, l=10, r=10, b=10),
        hoverlabel=dict(bgcolor="#0F1523", font_color="#F1F4FA", bordercolor="#243252")
    )
)

px.defaults.template = "aeronet"

ACCENT_SCALE = ["#12203A", "#22D3EE", "#818CF8", "#A78BFA"]


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AERONET | Global Flight Network Intelligence",
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

    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* ============================================================
       BASE CANVAS — deep space, blended ambient orbs, faint grid
       ============================================================ */

    .stApp {
        background:
            radial-gradient(circle at 8% 8%,  rgba(34, 211, 238, 0.10), transparent 40%),
            radial-gradient(circle at 92% 4%, rgba(129, 140, 248, 0.10), transparent 42%),
            radial-gradient(circle at 50% 100%, rgba(167, 139, 250, 0.08), transparent 48%),
            radial-gradient(circle at 100% 60%, rgba(45, 212, 191, 0.06), transparent 40%),
            repeating-linear-gradient(0deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 1px, transparent 1px, transparent 48px),
            repeating-linear-gradient(90deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 1px, transparent 1px, transparent 48px),
            #05070D;
        background-attachment: fixed;
        color: #E8ECF5;
    }

    h1, h2, h3, .main-title, .sidebar-brand-text, .section-title, .nav-heading {
        font-family: 'Sora', sans-serif !important;
    }

    h3 {
        color: #F1F4FA !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        position: relative;
        padding-left: 16px;
        margin-top: 38px !important;
        margin-bottom: 16px !important;
        letter-spacing: 0.2px;
    }

    h3::before {
        content: "";
        position: absolute;
        left: 0; top: 4px; bottom: 4px;
        width: 3px;
        border-radius: 3px;
        background: linear-gradient(180deg, #22D3EE, #818CF8, #A78BFA);
    }

    /* ============================================================
       SIDEBAR — glass panel
       ============================================================ */

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(11,13,22,0.97), rgba(7,9,16,0.99));
        border-right: 1px solid rgba(129,140,248,0.14);
    }

    [data-testid="stSidebar"] * {
        color: #C9D2E3;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 0 2px 0;
    }

    .sidebar-brand-badge {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
        background: linear-gradient(140deg, rgba(34,211,238,0.18), rgba(167,139,250,0.18));
        border: 1px solid rgba(129,140,248,0.35);
        box-shadow: 0 0 18px rgba(34,211,238,0.18);
    }

    .sidebar-brand-text {
        font-size: 21px;
        font-weight: 800;
        letter-spacing: 2.5px;
        background: linear-gradient(90deg, #F1F4FA, #A9D9FF 45%, #C4B5FD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .sidebar-subtitle {
        color: #6B7A99;
        font-size: 9.5px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 2px;
        margin-bottom: 26px;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(129,140,248,0.14);
    }

    .nav-heading {
        color: #57648A;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
        font-weight: 700;
    }

    div[role="radiogroup"] {
        gap: 6px;
    }

    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.025);
        border-radius: 10px;
        padding: 9px 12px;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all .18s ease;
    }

    div[role="radiogroup"] label:hover {
        border: 1px solid rgba(34,211,238,0.35);
        background: rgba(34,211,238,0.05);
    }

    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(90deg, rgba(34,211,238,0.14), rgba(167,139,250,0.10));
        border: 1px solid rgba(34,211,238,0.5) !important;
        box-shadow: 0 0 16px rgba(34,211,238,0.12);
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 7px 13px;
        border-radius: 20px;
        background: rgba(45,212,191,0.08);
        border: 1px solid rgba(45,212,191,0.28);
        color: #5EEAD4;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.6px;
    }

    .status .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #2DD4BF;
        box-shadow: 0 0 8px #2DD4BF;
        animation: pulse 1.6s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: .3; }
    }

    /* ============================================================
       HERO HEADER
       ============================================================ */

    .hero-wrap {
        position: relative;
        padding: 30px 34px;
        margin-bottom: 8px;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(34,211,238,0.06), rgba(167,139,250,0.05) 60%, rgba(255,255,255,0.02));
        backdrop-filter: blur(18px);
        border: 1px solid rgba(129,140,248,0.16);
        overflow: hidden;
    }

    .hero-wrap::before {
        content: "";
        position: absolute;
        top: 68%;
        left: -6%;
        width: 112%;
        border-top: 1px dashed rgba(129,140,248,0.22);
    }

    .hero-wrap::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        top: -130px;
        right: -80px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(34,211,238,0.16), transparent 70%);
    }

    .plane-icon {
        display: inline-block;
        margin-right: 12px;
        animation: fly 3.4s ease-in-out infinite;
        filter: drop-shadow(0 0 10px rgba(34,211,238,0.5));
    }

    @keyframes fly {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(-4deg); }
    }

    .main-title {
        font-family: 'Sora', sans-serif !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        letter-spacing: 6px !important;
        background: linear-gradient(90deg, #F1F4FA 10%, #67E8F9 40%, #A5B4FC 70%, #C4B5FD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
        margin-bottom: 2px;
    }

    .subtitle {
        color: #8993AB;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 2.2px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }

    /* ============================================================
       KPI CARDS — glass, gradient edge, icon badge
       ============================================================ */

    .kpi-card {
        position: relative;
        overflow: hidden;
        background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
        backdrop-filter: blur(14px);
        border: 1px solid rgba(129,140,248,0.16);
        border-radius: 18px;
        padding: 20px 20px 18px 20px;
        min-height: 118px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.3);
        transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
    }

    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #22D3EE, #818CF8, #A78BFA);
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 36px rgba(0,0,0,0.4);
        border-color: rgba(34,211,238,0.4);
    }

    .kpi-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 9px;
        font-size: 15px;
        background: rgba(34,211,238,0.10);
        border: 1px solid rgba(34,211,238,0.22);
        margin-bottom: 10px;
    }

    .kpi-label {
        color: #8993AB;
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        font-weight: 600;
    }

    .kpi-value {
        color: #F1F4FA;
        font-size: 29px;
        font-weight: 800;
        margin-top: 6px;
        font-family: 'Sora', sans-serif;
    }

    .kpi-accent {
        color: #67E8F9;
        font-size: 11px;
        margin-top: 5px;
    }

    /* ============================================================
       SECTION HEADERS
       ============================================================ */

    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 23px;
        font-weight: 700;
        color: #F1F4FA;
        margin-top: 22px;
    }

    .section-title::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(34,211,238,0.5), transparent);
        margin-left: 10px;
    }

    .section-caption {
        color: #7C87A3;
        font-size: 13px;
        margin-bottom: 16px;
    }

    /* ============================================================
       METRICS, CHARTS, TABLES, ALERTS — unified glass surfaces
       ============================================================ */

    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(129,140,248,0.16);
        border-radius: 16px;
        padding: 16px;
        transition: border-color .18s ease;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(34,211,238,0.4);
    }

    div[data-testid="stMetricLabel"] {
        color: #8993AB;
    }

    div[data-testid="stMetricValue"] {
        color: #F1F4FA;
        font-family: 'Sora', sans-serif;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(129,140,248,0.16);
        border-radius: 14px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        background: rgba(34,211,238,0.06);
        border: 1px solid rgba(34,211,238,0.22);
        border-radius: 14px;
    }

    hr {
        border-color: rgba(129,140,248,0.14);
    }

    div[data-testid="stPlotlyChart"] {
        background: linear-gradient(160deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(129,140,248,0.14);
        border-radius: 16px;
        padding: 8px;
        transition: border-color .18s ease;
    }

    div[data-testid="stPlotlyChart"]:hover {
        border-color: rgba(34,211,238,0.35);
    }

    /* Sliders / selects / tabs picking up the accent family */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #22D3EE !important;
        box-shadow: 0 0 10px rgba(34,211,238,0.6) !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 4px;
    }

    button[data-baseweb="tab"] {
        border-radius: 10px 10px 0 0 !important;
    }

    button[aria-selected="true"] {
        color: #67E8F9 !important;
    }

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #05070D;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #22D3EE, #818CF8);
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
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-badge">✈️</div>
            <div class="sidebar-brand-text">AERONET</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">GLOBAL FLIGHT NETWORK INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="nav-heading">Navigate</div>', unsafe_allow_html=True)

    nav_icons = {
        "Command Deck": "🛰️",
        "Flight Paths": "🛫",
        "Terminal Map": "🗺️",
        "Carrier Fleet": "✈️",
        "Network Core": "🕸️"
    }

    page = st.radio(
        "Navigation",
        [
            "Command Deck",
            "Flight Paths",
            "Terminal Map",
            "Carrier Fleet",
            "Network Core"
        ],
        format_func=lambda option: f"{nav_icons.get(option, '')}  {option}",
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        '<div class="status"><span class="dot"></span>DATA SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )

    st.caption("Big Data Analytics")
    st.caption("PySpark + HDFS + Neo4j")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="main-title"><span class="plane-icon">✈️</span>AERONET</div>
        <div class="subtitle">Mapping the World's Airline Route Network, Hub by Hub</div>
    </div>
    """,
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
            <div class="kpi-icon">🛫</div>
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
            <div class="kpi-icon">🏢</div>
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
            <div class="kpi-icon">✈️</div>
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
            <div class="kpi-icon">🔗</div>
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

if page == "Command Deck":

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

            overview_airlines = overview_airlines.sort_values(
                "total_routes",
                ascending=True
            )

            fig = px.bar(
                overview_airlines,
                x="total_routes",
                y="airline",
                orientation="h",
                title="Top 10 Airlines by Total Routes",
                text="total_routes",
                color="total_routes",
                color_continuous_scale=ACCENT_SCALE
            )

            fig.update_traces(
                textposition="outside",
                marker_line_width=0
            )

            fig.update_layout(
                xaxis_title="Total Routes",
                yaxis_title="",
                height=450,
                coloraxis_showscale=False
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

            fig = px.treemap(
                overview_airports,
                path=[px.Constant("All Hubs"), "airport"],
                values="total_connectivity",
                title="Top 10 Airport Hubs by Connectivity",
                color="total_connectivity",
                color_continuous_scale=ACCENT_SCALE
            )

            fig.update_traces(
                textinfo="label+value",
                marker_line_width=0.5,
                marker_line_color="#05070D"
            )

            fig.update_layout(
                height=450,
                coloraxis_showscale=False,
                margin=dict(t=55, l=6, r=6, b=6)
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

            destination_counts = destination_counts.sort_values(
                "Incoming Routes",
                ascending=False
            )

            fig = px.funnel(
                destination_counts,
                x="Incoming Routes",
                y="Destination Airport",
                title="Top 10 Airports by Incoming Routes"
            )

            fig.update_traces(
                marker_color=[
                    "#22D3EE", "#3BD4EA", "#54D5E5", "#6DA9EE",
                    "#818CF8", "#968FF3", "#A78BFA", "#B49CF9",
                    "#C4B5FD", "#D4C7FE"
                ][:len(destination_counts)]
            )

            fig.update_layout(
                height=450
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

elif page == "Flight Paths":

    st.markdown(
        '<div class="section-title">Flight Paths</div>',
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

            airline_n = st.slider(
                "Airlines to display",
                min_value=5,
                max_value=30,
                value=15,
                step=1,
                key="flight_paths_airline_n"
            )

            chart_df = (
                chart_df
                .sort_values(
                    "total_routes",
                    ascending=False
                )
                .head(airline_n)
                .sort_values("total_routes", ascending=True)
            )

            fig = go.Figure()

            for _, row in chart_df.iterrows():
                fig.add_shape(
                    type="line",
                    x0=0, x1=row["total_routes"],
                    y0=row["airline"], y1=row["airline"],
                    line=dict(color="rgba(129,140,248,0.35)", width=2)
                )

            fig.add_trace(
                go.Scatter(
                    x=chart_df["total_routes"],
                    y=chart_df["airline"],
                    mode="markers+text",
                    text=chart_df["total_routes"],
                    textposition="middle right",
                    textfont=dict(size=11, color="#8993AB"),
                    marker=dict(
                        size=12,
                        color=chart_df["total_routes"],
                        colorscale=[[0, "#22D3EE"], [1, "#A78BFA"]],
                        line=dict(width=1, color="#05070D")
                    ),
                    showlegend=False
                )
            )

            fig.update_layout(
                title="Carrier Route Volume",
                xaxis_title="Total Routes",
                yaxis_title="",
                height=max(420, airline_n * 26)
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

            fig = px.bar_polar(
                chart_df,
                r="total_connectivity",
                theta="airport",
                title="Connectivity Radar",
                color="total_connectivity",
                color_continuous_scale=ACCENT_SCALE
            )

            fig.update_layout(
                height=520,
                coloraxis_showscale=False,
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(gridcolor="rgba(129,140,248,0.14)", color="#8993AB"),
                    angularaxis=dict(gridcolor="rgba(129,140,248,0.14)", color="#C9D2E3")
                )
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

elif page == "Terminal Map":

    st.markdown(
        '<div class="section-title">Terminal Map</div>',
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

            chart_df = chart_df.reset_index(drop=True)
            chart_df["rank"] = chart_df.index + 1

            fig = px.scatter(
                chart_df,
                x="rank",
                y="total_connectivity",
                size="total_connectivity",
                color="total_connectivity",
                hover_name="airport",
                title="Top 15 Airports by Connectivity",
                color_continuous_scale=ACCENT_SCALE,
                size_max=48
            )

            fig.update_traces(
                marker=dict(line=dict(width=1, color="#05070D"))
            )

            fig.update_layout(
                xaxis_title="Rank",
                yaxis_title="Total Connectivity",
                coloraxis_showscale=False,
                height=460
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
                title="Global Airport Constellation"
            )

            fig.update_traces(
                marker=dict(
                    size=4,
                    color="#22D3EE",
                    opacity=0.75,
                    line=dict(width=0)
                )
            )

            fig.update_layout(
                height=520,
                geo=dict(
                    projection_type="orthographic",
                    showland=True,
                    landcolor="#0F1523",
                    showocean=True,
                    oceancolor="#05070D",
                    showcountries=True,
                    countrycolor="rgba(129,140,248,0.25)",
                    showcoastlines=True,
                    coastlinecolor="rgba(129,140,248,0.3)",
                    bgcolor="rgba(0,0,0,0)",
                    lakecolor="#05070D"
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

elif page == "Carrier Fleet":

    st.markdown(
        '<div class="section-title">Carrier Fleet</div>',
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

            chart_df = chart_df.sort_values("total_routes", ascending=False)

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=chart_df["airline"],
                    y=chart_df["total_routes"],
                    mode="markers",
                    marker=dict(
                        size=14,
                        color=chart_df["total_routes"],
                        colorscale=[[0, "#22D3EE"], [0.5, "#818CF8"], [1, "#A78BFA"]],
                        line=dict(width=1, color="#05070D")
                    ),
                    showlegend=False
                )
            )

            for _, row in chart_df.iterrows():
                fig.add_shape(
                    type="line",
                    x0=row["airline"], x1=row["airline"],
                    y0=0, y1=row["total_routes"],
                    line=dict(color="rgba(129,140,248,0.25)", width=1.5)
                )

            fig.update_layout(
                title="Top 15 Airlines by Total Routes",
                xaxis_title="Airline",
                yaxis_title="Total Routes",
                height=460
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

elif page == "Network Core":

    st.markdown(
        '<div class="section-title">Network Core</div>',
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

            chart_df = chart_df.sort_values("pagerank", ascending=True)

            fig = px.bar(
                chart_df,
                x="pagerank",
                y=x_column,
                orientation="h",
                title="Hub Influence Ranking (PageRank)",
                color="pagerank",
                color_continuous_scale=ACCENT_SCALE
            )

            fig.update_layout(
                xaxis_title="PageRank Score",
                yaxis_title="",
                coloraxis_showscale=False,
                height=420
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

            chart_df = chart_df.reset_index(drop=True)
            chart_df["rank"] = chart_df.index + 1

            fig = px.scatter(
                chart_df,
                x="rank",
                y=degree_column,
                size=degree_column,
                color=degree_column,
                hover_name=x_column,
                title="Degree Centrality — Connection Density",
                color_continuous_scale=ACCENT_SCALE,
                size_max=44
            )

            fig.update_traces(
                marker=dict(line=dict(width=1, color="#05070D"))
            )

            fig.update_layout(
                xaxis_title="Rank",
                yaxis_title="Degree",
                coloraxis_showscale=False,
                height=420
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

            chart_df = chart_df.sort_values("betweenness", ascending=False)

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=chart_df[x_column],
                    y=chart_df["betweenness"],
                    mode="lines+markers",
                    fill="tozeroy",
                    fillcolor="rgba(167,139,250,0.10)",
                    line=dict(color="#A78BFA", width=2),
                    marker=dict(size=9, color="#22D3EE", line=dict(width=1, color="#05070D")),
                    showlegend=False
                )
            )

            fig.update_layout(
                title="Betweenness — Bridge Airports",
                xaxis_title="Airport",
                yaxis_title="Betweenness Score",
                height=420
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