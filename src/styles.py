import streamlit as st


def load_css():
    st.markdown(
        """
<style>

/* =========================================================
   ROOT THEME
========================================================= */

:root {
    --bg-dark: #171412;
    --bg-soft: #211C19;
    --card: #2A231F;
    --card-light: #332A25;

    --coral: #F26B5B;
    --coral-dark: #C94E44;
    --amber: #F2B84B;

    --cream: #FFF4E8;
    --cream-soft: #F7E8DA;
    --muted: #C7B8AA;
    --muted-dark: #AFA095;

    --border: rgba(255, 244, 232, 0.10);
    --border-strong: rgba(255, 244, 232, 0.16);
}


/* =========================================================
   APPLICATION BACKGROUND
========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(242, 107, 91, 0.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 15%,
            rgba(242, 184, 75, 0.12),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #171412 0%,
            #1D1815 48%,
            #151210 100%
        );

    color: var(--cream);
    font-size: 17px;
}


/* =========================================================
   MAIN CONTAINER
========================================================= */

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
}


/* =========================================================
   STREAMLIT HEADER
========================================================= */

header[data-testid="stHeader"] {
    background: rgba(23, 20, 18, 0.82);
    backdrop-filter: blur(15px);
    border-bottom: 1px solid var(--border);
}


/* =========================================================
   GLOBAL TYPOGRAPHY
========================================================= */

h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--cream) !important;
    font-weight: 850 !important;
    letter-spacing: -0.01em;
}

h1 {
    font-size: 44px !important;
}

h2 {
    font-size: 32px !important;
}

h3 {
    font-size: 25px !important;
}

h4 {
    font-size: 21px !important;
}

p {
    color: var(--muted);
    font-size: 17px;
    line-height: 1.75;
}

label {
    color: var(--muted) !important;
    font-size: 16px !important;
    font-weight: 750 !important;
}

div[data-testid="stMarkdownContainer"] {
    font-size: 17px;
}

div[data-testid="stMarkdownContainer"] strong {
    color: var(--cream);
    font-weight: 850;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #211C19 0%,
            #171412 100%
        );

    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--cream);
}

section[data-testid="stSidebar"] label {
    font-size: 16px !important;
    font-weight: 750 !important;
}

section[data-testid="stSidebar"] p {
    font-size: 15px;
    line-height: 1.6;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-weight: 850 !important;
}

/* =========================================================
   SIDEBAR LOGO CARD
========================================================= */

.sidebar-logo{

    height:220px;

    display:flex;
    flex-direction:column;

    justify-content:space-between;

    align-items:center;

    padding:24px 20px;

    border-radius:22px;

    background:linear-gradient(
        145deg,
        #F26B5B,
        #D85648
    );

    box-shadow:0 12px 28px rgba(0,0,0,.25);

}

.sidebar-logo h1{

    margin:0;

    color:#FFF8F0;

    font-size:34px;

    font-weight:900;

    line-height:1.35;

    text-align:center;

}

.sidebar-logo p{

    margin:0;

    color:rgba(255,255,255,.92);

    font-size:16px;

    font-weight:600;

    text-align:center;

}


/* =========================================================
   HERO SECTION
========================================================= */

.hero {
    position: relative;
    overflow: hidden;

    padding: 48px 46px;
    margin-bottom: 30px;

    border-radius: 28px;

    background:
        linear-gradient(
            120deg,
            rgba(242, 107, 91, 0.97),
            rgba(201, 78, 68, 0.94) 52%,
            rgba(119, 48, 42, 0.95)
        );

    border: 1px solid rgba(255, 244, 232, 0.20);

    box-shadow:
        0 24px 55px rgba(0, 0, 0, 0.34),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.hero::after {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    right: -75px;
    top: -95px;

    border-radius: 50%;

    background: rgba(242, 184, 75, 0.28);

    filter: blur(4px);
}

.hero-badge {
    display: inline-block;
    position: relative;
    z-index: 2;

    padding: 9px 16px;

    border-radius: 999px;

    background: rgba(23, 20, 18, 0.25);
    border: 1px solid rgba(255, 244, 232, 0.24);

    color: #FFF8F0;

    font-size: 15px;
    font-weight: 800;

    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.hero h1 {
    position: relative;
    z-index: 2;

    max-width: 1020px;

    margin: 21px 0 14px;

    color: #FFF8F0 !important;

    font-size: 54px !important;
    line-height: 1.12;

    font-weight: 900 !important;
    letter-spacing: -0.025em;
}

.hero p {
    position: relative;
    z-index: 2;

    max-width: 920px;

    margin: 0;

    color: rgba(255, 248, 240, 0.92);

    font-size: 21px;
    line-height: 1.75;
}


/* =========================================================
   SECTION HEADINGS
========================================================= */

.section-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding:34px 36px;
    margin: 20px 0 16px;

    background:
        linear-gradient(
            135deg,
            rgba(51, 42, 37, 0.94),
            rgba(37, 31, 28, 0.92)
        );

    border: 1px solid var(--border);
    border-left: 6px solid var(--coral);

    border-radius:22px;

    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
}

.section-heading h2{

    margin:0;

    color:#FFF4E8;

    font-size:36px;

    line-height:1.2;

    font-weight:900;

}

.section-heading p{

    margin:14px 0 0;

    color:#D6C9BE;

    font-size:19px;

    line-height:1.8;

    font-weight:500;

}

/* =========================================================
   KPI CARDS
========================================================= */

.metric-card {
    min-height: 170px;

    padding: 24px 17px;

    background:
        linear-gradient(
            145deg,
            rgba(51, 42, 37, 0.97),
            rgba(37, 31, 28, 0.99)
        );

    border: 1px solid var(--border);
    border-top: 4px solid var(--amber);

    border-radius: 20px;

    text-align: center;

    box-shadow:
        0 14px 32px rgba(0, 0, 0, 0.24),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-5px);

    border-color: rgba(242, 184, 75, 0.48);

    box-shadow:
        0 20px 42px rgba(0, 0, 0, 0.32);
}

.metric-icon {
    margin-bottom: 11px;

    font-size: 32px;
}

.metric-title {
    color: var(--muted);

    font-size: 15px;
    line-height: 1.4;

    font-weight: 800;

    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.metric-value {
    margin-top: 11px;

    color: var(--cream);

    font-size: 40px;
    line-height: 1.1;

    font-weight: 900;
}


/* =========================================================
   FILTER CHIPS
========================================================= */

.filter-chip {
    display: inline-flex;
    align-items: center;

    padding: 11px 17px;

    border-radius: 999px;

    background: rgba(242, 184, 75, 0.10);
    border: 1px solid rgba(242, 184, 75, 0.28);

    color: var(--cream);

    font-size: 15px;
    font-weight: 750;
}


/* =========================================================
   HIGHLIGHT CARDS
========================================================= */

.highlight-card {
    padding: 27px 30px;
    margin-bottom: 24px;

    background:
        linear-gradient(
            115deg,
            rgba(242, 107, 91, 0.20),
            rgba(242, 184, 75, 0.10),
            rgba(42, 35, 31, 0.95)
        );

    border: 1px solid rgba(242, 184, 75, 0.30);
    border-left: 6px solid var(--amber);

    border-radius: 20px;

    box-shadow:
        0 14px 32px rgba(0, 0, 0, 0.22);
}

.highlight-label {
    color: var(--amber);

    font-size: 15px;
    font-weight: 850;

    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.highlight-title {
    margin-top: 10px;

    color: var(--cream);

    font-size: 34px;
    line-height: 1.25;

    font-weight: 900;
}

.highlight-subtitle {
    margin-top: 6px;

    color: var(--muted);

    font-size: 19px;
    font-weight: 650;
}

.highlight-stats {
    display: flex;
    flex-wrap: wrap;

    gap: 13px 26px;

    margin-top: 20px;
}

.highlight-stats span {
    color: var(--muted);

    font-size: 17px;
    line-height: 1.6;
}

.highlight-stats b {
    color: var(--cream);

    font-weight: 850;
}


/* =========================================================
   INSIGHT BANNERS
========================================================= */

.insight-banner {
    display: flex;
    align-items: flex-start;

    gap: 17px;

    padding: 23px 26px;
    margin-bottom: 24px;

    background:
        linear-gradient(
            110deg,
            rgba(242, 184, 75, 0.15),
            rgba(242, 107, 91, 0.08),
            rgba(42, 35, 31, 0.93)
        );

    border: 1px solid rgba(242, 184, 75, 0.28);

    border-radius: 18px;
}

.insight-banner-icon {
    font-size: 32px;
    line-height: 1;
}

.insight-banner-title {
    color: var(--amber);

    font-size: 16px;
    font-weight: 850;

    letter-spacing: 0.07em;
    text-transform: uppercase;
}

.insight-banner-text {
    margin-top: 8px;

    color: var(--muted);

    font-size: 17px;
    line-height: 1.8;
}

.insight-banner-text b {
    color: var(--cream);
}


/* =========================================================
   RECOMMENDATION GRID
========================================================= */

.recommendation-grid {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 20px;

    margin-top: 20px;
}

.recommendation-card {
    position: relative;
    overflow: hidden;

    min-height: 285px;

    padding: 27px;

    background:
        linear-gradient(
            145deg,
            rgba(51, 42, 37, 0.97),
            rgba(37, 31, 28, 0.99)
        );

    border: 1px solid var(--border);

    border-radius: 20px;

    box-shadow:
        0 15px 35px rgba(0, 0, 0, 0.22);

    transition:
        transform 0.25s ease,
        border-color 0.25s ease;
}

.recommendation-card:hover {
    transform: translateY(-4px);

    border-color: rgba(242, 184, 75, 0.40);
}

.recommendation-card::after {
    content: "";

    position: absolute;

    width: 120px;
    height: 120px;

    right: -48px;
    bottom: -55px;

    border-radius: 50%;

    background: rgba(242, 107, 91, 0.10);
}

.recommendation-top {
    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 12px;
}

.recommendation-icon {
    font-size: 34px;
}

.recommendation-priority {
    padding: 7px 13px;

    border-radius: 999px;

    background: rgba(242, 184, 75, 0.12);
    border: 1px solid rgba(242, 184, 75, 0.28);

    color: var(--amber);

    font-size: 13px;
    font-weight: 850;

    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.recommendation-category {
    margin-top: 19px;

    color: var(--coral);

    font-size: 15px;
    font-weight: 850;

    letter-spacing: 0.10em;
    text-transform: uppercase;
}

.recommendation-title {
    margin-top: 9px;

    color: var(--cream);

    font-size: 25px;
    line-height: 1.35;

    font-weight: 900;
}

.recommendation-message {
    position: relative;
    z-index: 2;

    margin-top: 14px;

    color: var(--muted);

    font-size: 17px;
    line-height: 1.8;
}


/* =========================================================
   EXECUTIVE SUMMARY CARD
========================================================= */

.executive-summary-card {
    padding: 31px;
    margin-bottom: 26px;

    background:
        linear-gradient(
            115deg,
            rgba(242, 107, 91, 0.18),
            rgba(242, 184, 75, 0.09),
            rgba(42, 35, 31, 0.97)
        );

    border: 1px solid rgba(242, 184, 75, 0.28);
    border-left: 6px solid var(--coral);

    border-radius: 21px;
}

.executive-summary-label {
    color: var(--amber);

    font-size: 15px;
    font-weight: 850;

    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.executive-summary-title {
    margin-top: 10px;

    color: var(--cream);

    font-size: 31px;
    line-height: 1.25;

    font-weight: 900;
}

.executive-summary-text {
    margin-top: 15px;

    color: var(--muted);

    font-size: 18px;
    line-height: 1.9;
}


/* =========================================================
   METHODOLOGY CARD
========================================================= */

.methodology-card {
    position: relative;
    overflow: hidden;

    margin-top: 28px;
    padding: 30px 32px;

    background:
        linear-gradient(
            125deg,
            rgba(242, 184, 75, 0.16),
            rgba(242, 107, 91, 0.09),
            rgba(42, 35, 31, 0.98)
        );

    border: 1px solid rgba(242, 184, 75, 0.32);
    border-left: 6px solid var(--amber);

    border-radius: 21px;

    box-shadow:
        0 16px 36px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.methodology-card::after {
    content: "";

    position: absolute;

    width: 190px;
    height: 190px;

    right: -75px;
    top: -95px;

    border-radius: 50%;

    background: rgba(242, 184, 75, 0.10);
}

.methodology-header {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;

    gap: 13px;
}

.methodology-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 48px;
    height: 48px;

    border-radius: 14px;

    background: rgba(242, 184, 75, 0.14);
    border: 1px solid rgba(242, 184, 75, 0.30);

    font-size: 25px;
}

.methodology-title {
    color: var(--cream);

    font-size: 27px;
    font-weight: 900;
}

.methodology-description {
    position: relative;
    z-index: 2;

    margin-top: 18px;

    color: var(--muted);

    font-size: 17px;
    line-height: 1.9;
}

.methodology-description b {
    color: var(--cream);

    font-weight: 850;
}

.methodology-points {
    position: relative;
    z-index: 2;

    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 12px 18px;

    margin-top: 21px;
}

.methodology-point {
    padding: 13px 16px;

    border-radius: 13px;

    background: rgba(255, 244, 232, 0.045);
    border: 1px solid rgba(255, 244, 232, 0.09);

    color: #D9CCC1;

    font-size: 16px;
    font-weight: 700;
}

.methodology-disclaimer {
    position: relative;
    z-index: 2;

    margin-top: 20px;
    padding-top: 18px;

    border-top:
        1px solid rgba(255, 244, 232, 0.11);

    color: var(--muted-dark);

    font-size: 15px;
    line-height: 1.75;
}


/* =========================================================
   TABS
========================================================= */

div[data-testid="stTabs"] {
    margin-top: 6px;
}

div[data-testid="stTabs"] button {
    min-height: 56px;

    padding: 14px 18px !important;

    color: var(--muted);

    font-size: 16px !important;
    font-weight: 800 !important;
}

div[data-testid="stTabs"] button:hover {
    color: var(--cream);
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--cream);
}

div[data-testid="stTabs"]
div[data-baseweb="tab-highlight"] {
    height: 4px;

    background-color: var(--coral);

    border-radius: 6px;
}


/* =========================================================
   INPUT CONTROLS
========================================================= */

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div,
div[data-testid="stDateInput"] > div > div {
    background: var(--card);

    border-color: var(--border);
}

div[data-testid="stSelectbox"] *,
div[data-testid="stMultiSelect"] *,
div[data-testid="stDateInput"] * {
    font-size: 15px !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {
    min-height: 46px;

    padding: 10px 18px;

    border: 1px solid rgba(242, 184, 75, 0.32);
    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            rgba(242, 107, 91, 0.92),
            rgba(201, 78, 68, 0.95)
        );

    color: white;

    font-size: 16px;
    font-weight: 800;

    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    border-color: rgba(242, 184, 75, 0.55);

    box-shadow:
        0 10px 22px rgba(0, 0, 0, 0.24);
}


/* =========================================================
   DATAFRAME
========================================================= */

div[data-testid="stDataFrame"] {
    overflow: hidden;

    border: 1px solid var(--border);
    border-radius: 16px;

    font-size: 15px;
}


/* =========================================================
   ALERTS
========================================================= */

div[data-testid="stAlert"] {
    border-radius: 16px;

    font-size: 16px;
    line-height: 1.7;
}


/* =========================================================
   PLOTLY CONTAINERS
========================================================= */

div[data-testid="stPlotlyChart"] {
    overflow: hidden;

    padding: 4px;

    border: 1px solid rgba(255, 244, 232, 0.06);
    border-radius: 17px;

    background: rgba(42, 35, 31, 0.22);
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {
    border-color: rgba(255, 244, 232, 0.10);
}


/* =========================================================
   RESPONSIVE DESIGN
========================================================= */

@media (max-width: 1100px) {

    .hero h1 {
        font-size: 46px !important;
    }

    .metric-value {
        font-size: 35px;
    }

    .recommendation-grid {
        grid-template-columns: 1fr;
    }
}


@media (max-width: 800px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 34px 28px;
    }

    .hero h1 {
        font-size: 38px !important;
    }

    .hero p {
        font-size: 18px;
    }

    .section-heading h2 {
        font-size: 27px !important;
    }

    .metric-value {
        font-size: 32px;
    }

    .methodology-points {
        grid-template-columns: 1fr;
    }

    .highlight-stats {
        flex-direction: column;
    }
}

</style>
        """,
        unsafe_allow_html=True
    )
