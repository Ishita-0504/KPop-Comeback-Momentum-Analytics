import streamlit as st
import pandas as pd
from textwrap import dedent

from src.styles import load_css
from src.data_loader import load_data
from src.charts import (
    popularity_trend_chart,
    album_type_donut,
    explicit_content_donut,
    popularity_distribution_chart,
    top_artists_chart,
    top_reentry_songs_chart,
    reentry_gap_distribution_chart,
    reentry_timeline_chart,
    reentry_scatter_chart,
    top_momentum_chart,
    momentum_distribution_chart,
    retention_vs_momentum_chart,
    rank_recovery_chart,
    momentum_timeline_chart,
    top_fandom_songs_chart,
    fandom_distribution_chart,
    fandom_bubble_chart,
    top_fandom_artists_chart,
    momentum_by_album_type_chart,
    momentum_by_explicit_chart,
    duration_vs_momentum_chart,
    album_size_vs_momentum_chart,
    retention_by_album_type_chart,
    rank_recovery_by_content_chart,
    fandom_tier_chart
)
from src.reentry import (
    prepare_reentry_data,
    get_reentry_summary,
    get_reentry_events
)
from src.momentum import (
    get_comeback_events,
    get_song_momentum_summary
)
from src.fandom import (
    get_fandom_summary,
    get_artist_fandom_summary
)
from src.recommendation import (
    generate_recommendations,
    generate_executive_summary
)



def render_html(html: str) -> None:
    """Render raw HTML without Markdown interpreting indentation as code blocks."""
    st.html(dedent(html).strip())


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="K-Pop Intelligence Dashboard",
    page_icon="🎵",
    layout="wide"
)

load_css()

df = load_data()

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    render_html("""
    <div style="
        background:linear-gradient(135deg,#F26B5B,#C94E44);
        padding:35px;
        border-radius:18px;
        text-align:center;
        margin-bottom:20px;
        color:white;
    ">
    <h1 style="margin-bottom:5px;">
    K-Pop Analytics
    </h1>

    <p style="
        color:#FFE9E3;
        margin:0;
        font-size:18px;
    ">
    South Korea Top 50 Intelligence
    </p>

    </div>
    """)

    st.markdown("### 🎛 Dashboard Filters")

    # ----------------------------
    # Date Filter
    # ----------------------------
    date_range = st.date_input(
        "Select Date Range",
        value=(
            df["date"].min().date(),
            df["date"].max().date()
        )
    )

    # ----------------------------
    # Artist Filter
    # ----------------------------
    artists = st.multiselect(
        "Artist",
        sorted(df["artist"].unique())
    )

    # ----------------------------
    # Song Filter
    # ----------------------------
    songs = st.multiselect(
        "Song",
        sorted(df["song"].unique())
    )

    # ----------------------------
    # Album Type
    # ----------------------------
    album = st.multiselect(
        "Album Type",
        sorted(df["album_type"].unique())
    )

    # ----------------------------
    # Explicit
    # ----------------------------
    explicit = st.selectbox(
        "Explicit Content",
        ["All", "Explicit", "Clean"]
    )

    st.markdown("---")

    st.caption("Dashboard developed for Atlantic Recording Corporation")


# ============================================
# FILTER DATA
# ============================================
filtered_df = df.copy()

if len(date_range) == 2:
    start, end = date_range
    filtered_df = filtered_df[
        (filtered_df["date"] >= pd.to_datetime(start))
        & (filtered_df["date"] <= pd.to_datetime(end))
    ]

if artists:
    filtered_df = filtered_df[filtered_df["artist"].isin(artists)]

if songs:
    filtered_df = filtered_df[filtered_df["song"].isin(songs)]

if album:
    filtered_df = filtered_df[filtered_df["album_type"].isin(album)]

if explicit == "Explicit":
    filtered_df = filtered_df[filtered_df["is_explicit"] == True]
elif explicit == "Clean":
    filtered_df = filtered_df[filtered_df["is_explicit"] == False]

if filtered_df.empty:
    st.warning(
        "No records match the selected filters. Please modify the sidebar selections."
    )
    st.stop()


# ============================================
# PREPARE ANALYTICAL DATA
# ============================================
reentry_data = prepare_reentry_data(filtered_df)
reentry_summary = get_reentry_summary(filtered_df)
reentry_events = get_reentry_events(filtered_df)

comeback_events = get_comeback_events(filtered_df)
song_momentum = get_song_momentum_summary(filtered_df)

fandom_summary = get_fandom_summary(filtered_df)
artist_fandom = get_artist_fandom_summary(filtered_df)


# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
<div class="hero">
<div class="hero-badge">South Korea • Top 50 • Momentum Intelligence</div>
<h1>Comeback Momentum and Fandom Intelligence</h1>
<p>
An analytical view of chart re-entry cycles, promotional surges,
post-comeback sustainability, and fandom-driven listening behaviour
across South Korea’s Top 50 playlist.
</p>
</div>
""",
    unsafe_allow_html=True
)

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_songs = filtered_df["song"].nunique()
total_artists = filtered_df["artist"].nunique()
total_records = len(filtered_df)
avg_popularity = round(filtered_df["popularity"].mean(), 1)
explicit_entries = int(filtered_df["is_explicit"].sum())
album_types = filtered_df["album_type"].nunique()

# -----------------------------
# KPI CARDS
# -----------------------------
cards = [
    ("🎵", "Unique Songs", total_songs),
    ("🎤", "Artists", total_artists),
    ("📚", "Chart Records", f"{total_records:,}"),
    ("🔥", "Avg Popularity", avg_popularity),
    ("🔞", "Explicit Entries", f"{explicit_entries:,}"),
    ("💿", "Release Types", album_types),
]

columns = st.columns(6)

for col, (icon, title, value) in zip(columns, cards):
    with col:
        render_html(
            f"""
            <div class="metric-card">
                <div class="metric-icon">{icon}</div>
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """
)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

render_html(
    f"""
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:22px;">
        <div class="filter-chip">
            📅 {filtered_df["date"].min().strftime("%d %b %Y")} –
            {filtered_df["date"].max().strftime("%d %b %Y")}
        </div>
        <div class="filter-chip">🎵 {filtered_df["song"].nunique():,} Songs</div>
        <div class="filter-chip">🎤 {filtered_df["artist"].nunique():,} Artists</div>
        <div class="filter-chip">📊 {len(filtered_df):,} Records</div>
    </div>
    """
)


# ============================================
# DASHBOARD TABS
# ============================================
(
    overview_tab,
    reentry_tab,
    momentum_tab,
    fandom_tab,
    content_tab,
    recommendation_tab,
) = st.tabs(
    [
        "Overview",
        "Re-Entry Analysis",
        "Comeback Momentum",
        "Fandom Intelligence",
        "Content Insights",
        "Recommendations",
    ]
)


with overview_tab:

    render_html(
        """
        <div class="section-heading">
            <div>
                <h2>Market Overview</h2>
                <p>
                    Explore playlist activity, popularity movement,
                    release composition and leading artists.
                </p>
            </div>
        </div>
        """
)

    # Popularity trend
    st.plotly_chart(
        popularity_trend_chart(filtered_df),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # Donut charts
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            album_type_donut(filtered_df),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:
        st.plotly_chart(
            explicit_content_donut(filtered_df),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # Distribution and top artists
    col3, col4 = st.columns([1, 1.25])

    with col3:
        st.plotly_chart(
            popularity_distribution_chart(filtered_df),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col4:
        st.plotly_chart(
            top_artists_chart(filtered_df),
            use_container_width=True,
            config={"displayModeBar": False}
        )

with reentry_tab:

    render_html(
        """
        <div class="section-heading">
            <div>
                <h2>Chart Re-Entry Intelligence</h2>
                <p>
                    Identify songs that repeatedly return to the Top 50,
                    measure absence periods and evaluate recurring chart activity.
                </p>
            </div>
        </div>
        """
)

    total_reentry_events = int(
        reentry_summary["reentry_count"].sum()
    )

    songs_with_reentry = int(
        (reentry_summary["reentry_count"] > 0).sum()
    )

    avg_reentry_gap = (
        reentry_events["day_gap"].mean()
        if not reentry_events.empty
        else 0
    )

    highest_reentry = (
        reentry_summary["reentry_count"].max()
        if not reentry_summary.empty
        else 0
    )

    k1, k2, k3, k4 = st.columns(4)

    reentry_cards = [
        ("🔁", "Re-Entry Events", f"{total_reentry_events:,}"),
        ("🎵", "Songs Re-Entering", f"{songs_with_reentry:,}"),
        ("⏳", "Average Gap", f"{avg_reentry_gap:.1f} days"),
        ("🏆", "Highest Re-Entries", int(highest_reentry))
    ]

    for col, (icon, title, value) in zip(
        [k1, k2, k3, k4],
        reentry_cards
    ):
        with col:
            render_html(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """
)

    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.plotly_chart(
            top_reentry_songs_chart(reentry_summary),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:
        st.plotly_chart(
            reentry_gap_distribution_chart(reentry_events),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    st.plotly_chart(
        reentry_scatter_chart(reentry_summary),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown("### Song Re-Entry Timeline")

    timeline_options = (
        reentry_summary[
            reentry_summary["reentry_count"] > 0
        ]
        .sort_values(
            "reentry_count",
            ascending=False
        )
    )

    selected_song_id = st.selectbox(
        "Select a song",
        timeline_options["song_id"],
        format_func=lambda song_id: (
            timeline_options.loc[
                timeline_options["song_id"] == song_id,
                "song"
            ].iloc[0]
            + " — "
            + timeline_options.loc[
                timeline_options["song_id"] == song_id,
                "artist"
            ].iloc[0]
        )
    )

    selected_song_name = timeline_options.loc[
        timeline_options["song_id"] == selected_song_id,
        "song"
    ].iloc[0]

    song_timeline = reentry_data[
        reentry_data["song_id"] == selected_song_id
    ].copy()

    st.plotly_chart(
        reentry_timeline_chart(
            song_timeline,
            selected_song_name
        ),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    leaderboard = (
        reentry_summary[
            reentry_summary["reentry_count"] > 0
        ]
        .sort_values(
            "reentry_count",
            ascending=False
        )
        .head(25)
        [
            [
                "song",
                "artist",
                "reentry_count",
                "average_reentry_gap",
                "maximum_reentry_gap",
                "total_chart_days"
            ]
        ]
    )

    leaderboard.columns = [
        "Song",
        "Artist",
        "Re-Entries",
        "Average Gap",
        "Maximum Gap",
        "Chart Days"
    ]

    st.markdown("### Re-Entry Leaderboard")

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )


comeback_events = get_comeback_events(filtered_df)

song_momentum = get_song_momentum_summary(filtered_df)
with momentum_tab:

    render_html(
        """
        <div class="section-heading">
            <div>
                <h2>Comeback Momentum Intelligence</h2>
                <p>
                    Measure comeback strength using rank recovery,
                    popularity growth, retention, recovery speed and
                    post-peak stability.
                </p>
            </div>
        </div>
        """
)

    if comeback_events.empty:
        st.info(
            "No comeback episodes are available for the selected filters."
        )

    else:
        average_momentum = comeback_events["momentum_score"].mean()
        strongest_momentum = comeback_events["momentum_score"].max()
        average_retention = comeback_events["retention_days"].mean()
        average_recovery = comeback_events["days_to_peak"].mean()

        strongest_event = comeback_events.loc[
            comeback_events["momentum_score"].idxmax()
        ]

        m1, m2, m3, m4 = st.columns(4)

        momentum_cards = [
            (
                "⚡",
                "Average Momentum",
                f"{average_momentum:.1f}"
            ),
            (
                "🔥",
                "Strongest Momentum",
                f"{strongest_momentum:.1f}"
            ),
            (
                "📆",
                "Average Retention",
                f"{average_retention:.1f} days"
            ),
            (
                "🚀",
                "Average Recovery",
                f"{average_recovery:.1f} days"
            )
        ]

        for col, (icon, title, value) in zip(
            [m1, m2, m3, m4],
            momentum_cards
        ):
            with col:
                render_html(
                    f"""
                    <div class="metric-card">
                        <div class="metric-icon">{icon}</div>
                        <div class="metric-title">{title}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """
)

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        render_html(
            f"""
            <div class="highlight-card">
                <div class="highlight-label">
                    Strongest Comeback Episode
                </div>

                <div class="highlight-title">
                    {strongest_event["song"]}
                </div>

                <div class="highlight-subtitle">
                    {strongest_event["artist"]}
                </div>

                <div class="highlight-stats">
                    <span>
                        ⚡ Momentum:
                        <b>{strongest_event["momentum_score"]:.1f}</b>
                    </span>

                    <span>
                        🏆 Peak Rank:
                        <b>#{int(strongest_event["peak_rank"])}</b>
                    </span>

                    <span>
                        📆 Retention:
                        <b>{int(strongest_event["retention_days"])} days</b>
                    </span>

                    <span>
                        📈 Rank Recovery:
                        <b>{int(strongest_event["rank_improvement"])}</b>
                    </span>
                </div>
            </div>
            """
)

        chart1, chart2 = st.columns([1.2, 1])

        with chart1:
            st.plotly_chart(
                top_momentum_chart(song_momentum),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with chart2:
            st.plotly_chart(
                momentum_distribution_chart(comeback_events),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.plotly_chart(
            retention_vs_momentum_chart(comeback_events),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.plotly_chart(
            rank_recovery_chart(comeback_events),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.markdown("### Individual Song Comeback Timeline")

        momentum_song_options = (
            song_momentum
            .sort_values(
                "maximum_momentum",
                ascending=False
            )
        )

        selected_momentum_song = st.selectbox(
            "Select a song for momentum history",
            momentum_song_options["song_id"],
            key="momentum_song_selector",
            format_func=lambda song_id: (
                momentum_song_options.loc[
                    momentum_song_options["song_id"] == song_id,
                    "song"
                ].iloc[0]
                + " — "
                + momentum_song_options.loc[
                    momentum_song_options["song_id"] == song_id,
                    "artist"
                ].iloc[0]
            )
        )

        selected_momentum_name = (
            momentum_song_options.loc[
                momentum_song_options["song_id"]
                == selected_momentum_song,
                "song"
            ].iloc[0]
        )

        selected_momentum_events = comeback_events[
            comeback_events["song_id"]
            == selected_momentum_song
        ]

        st.plotly_chart(
            momentum_timeline_chart(
                selected_momentum_events,
                selected_momentum_name
            ),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        momentum_table = (
            comeback_events
            .sort_values(
                "momentum_score",
                ascending=False
            )
            .head(30)
            [
                [
                    "song",
                    "artist",
                    "comeback_date",
                    "momentum_score",
                    "start_rank",
                    "peak_rank",
                    "rank_improvement",
                    "popularity_gain",
                    "retention_days",
                    "days_to_peak",
                    "rank_decay_speed"
                ]
            ]
        )

        momentum_table.columns = [
            "Song",
            "Artist",
            "Comeback Date",
            "Momentum Score",
            "Starting Rank",
            "Peak Rank",
            "Rank Improvement",
            "Popularity Gain",
            "Retention Days",
            "Days to Peak",
            "Rank Decay per Day"
        ]

        st.markdown("### Comeback Episode Leaderboard")

        st.dataframe(
            momentum_table,
            use_container_width=True,
            hide_index=True
        )

fandom_summary = get_fandom_summary(
    filtered_df
)

artist_fandom = get_artist_fandom_summary(
    filtered_df
)
with fandom_tab:

    render_html(
        """
        <div class="section-heading">
            <div>
                <h2>Fandom Intelligence</h2>
                <p>
                    Estimate fandom-driven engagement using repeated
                    chart returns, comeback strength, chart persistence
                    and recovery efficiency.
                </p>
            </div>
        </div>
        """
)

    fandom_with_activity = fandom_summary[
        fandom_summary["reentry_count"] > 0
    ].copy()

    if fandom_with_activity.empty:

        st.info(
            "No fandom-intensity results are available "
            "for the selected filters."
        )

    else:

        average_fandom = (
            fandom_with_activity["fandom_score"].mean()
        )

        maximum_fandom = (
            fandom_with_activity["fandom_score"].max()
        )

        intense_songs = int(
            (
                fandom_with_activity["fandom_tier"]
                == "Intense"
            ).sum()
        )

        active_artists = int(
            fandom_with_activity["artist"].nunique()
        )

        strongest_fandom_song = fandom_with_activity.loc[
            fandom_with_activity[
                "fandom_score"
            ].idxmax()
        ]

        f1, f2, f3, f4 = st.columns(4)

        fandom_cards = [
            (
                "💗",
                "Average Fandom Score",
                f"{average_fandom:.1f}"
            ),
            (
                "🔥",
                "Highest Fandom Score",
                f"{maximum_fandom:.1f}"
            ),
            (
                "🌟",
                "Intense-Tier Songs",
                f"{intense_songs:,}"
            ),
            (
                "🎤",
                "Artists with Re-Entries",
                f"{active_artists:,}"
            )
        ]

        for col, (
            icon,
            title,
            value
        ) in zip(
            [f1, f2, f3, f4],
            fandom_cards
        ):

            with col:

                render_html(
                    f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            {icon}
                        </div>

                        <div class="metric-title">
                            {title}
                        </div>

                        <div class="metric-value">
                            {value}
                        </div>

                    </div>
                    """
)

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        render_html(
            f"""
            <div class="highlight-card">

                <div class="highlight-label">
                    Strongest Fandom Signal
                </div>

                <div class="highlight-title">
                    {strongest_fandom_song["song"]}
                </div>

                <div class="highlight-subtitle">
                    {strongest_fandom_song["artist"]}
                </div>

                <div class="highlight-stats">

                    <span>
                        💗 Fandom Score:
                        <b>
                            {strongest_fandom_song["fandom_score"]:.1f}
                        </b>
                    </span>

                    <span>
                        🔁 Re-Entries:
                        <b>
                            {int(strongest_fandom_song["reentry_count"])}
                        </b>
                    </span>

                    <span>
                        ⚡ Average Momentum:
                        <b>
                            {strongest_fandom_song["average_momentum"]:.1f}
                        </b>
                    </span>

                    <span>
                        📆 Chart Days:
                        <b>
                            {int(strongest_fandom_song["total_chart_days"])}
                        </b>
                    </span>

                    <span>
                        🏷 Tier:
                        <b>
                            {strongest_fandom_song["fandom_tier"]}
                        </b>
                    </span>

                </div>

            </div>
            """
)

        chart1, chart2 = st.columns(
            [1.25, 1]
        )

        with chart1:

            st.plotly_chart(
                top_fandom_songs_chart(
                    fandom_with_activity
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with chart2:

            st.plotly_chart(
                fandom_tier_chart(
                    fandom_with_activity
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        st.plotly_chart(
            fandom_bubble_chart(
                fandom_with_activity
            ),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

        artist_col, distribution_col = st.columns(
            [1.25, 1]
        )

        with artist_col:

            st.plotly_chart(
                top_fandom_artists_chart(
                    artist_fandom
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with distribution_col:

            st.plotly_chart(
                fandom_distribution_chart(
                    fandom_with_activity
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        fandom_table = (
            fandom_with_activity
            .sort_values(
                "fandom_score",
                ascending=False
            )
            .head(30)
            [
                [
                    "song",
                    "artist",
                    "fandom_score",
                    "fandom_tier",
                    "reentry_count",
                    "average_momentum",
                    "maximum_momentum",
                    "average_retention",
                    "total_chart_days",
                    "average_recovery_days"
                ]
            ]
        )

        fandom_table.columns = [
            "Song",
            "Artist",
            "Fandom Score",
            "Fandom Tier",
            "Re-Entries",
            "Average Momentum",
            "Maximum Momentum",
            "Average Retention",
            "Chart Days",
            "Average Recovery Days"
        ]

        st.markdown(
            "### Fandom Intensity Leaderboard"
        )

        st.dataframe(
            fandom_table,
            use_container_width=True,
            hide_index=True
        )

with content_tab:

    render_html(
        """
        <div class="section-heading">
            <div>
                <h2>Content and Release Strategy Insights</h2>
                <p>
                    Examine how release type, album size, duration and
                    explicit-content classification influence comeback
                    intensity, recovery and post-comeback retention.
                </p>
            </div>
        </div>
        """
)

    if comeback_events.empty:

        st.info(
            "No comeback episodes are available for "
            "content-attribute analysis."
        )

    else:

        content_data = comeback_events.copy()

        release_summary = (
            content_data.groupby("album_type")
            .agg(
                average_momentum=(
                    "momentum_score",
                    "mean"
                ),
                average_retention=(
                    "retention_days",
                    "mean"
                ),
                average_rank_recovery=(
                    "rank_improvement",
                    "mean"
                ),
                comeback_events=(
                    "episode",
                    "count"
                )
            )
            .reset_index()
        )

        album_momentum = release_summary.loc[
            release_summary["album_type"]
            .str.lower()
            .eq("album"),
            "average_momentum"
        ]

        single_momentum = release_summary.loc[
            release_summary["album_type"]
            .str.lower()
            .eq("single"),
            "average_momentum"
        ]

        if (
            not album_momentum.empty
            and not single_momentum.empty
            and single_momentum.iloc[0] != 0
        ):
            album_advantage_index = (
                album_momentum.iloc[0]
                / single_momentum.iloc[0]
            )
        else:
            album_advantage_index = 0

        explicit_average = content_data.loc[
            content_data["is_explicit"] == True,
            "momentum_score"
        ].mean()

        clean_average = content_data.loc[
            content_data["is_explicit"] == False,
            "momentum_score"
        ].mean()

        explicit_average = (
            0
            if pd.isna(explicit_average)
            else explicit_average
        )

        clean_average = (
            0
            if pd.isna(clean_average)
            else clean_average
        )

        dominant_release = (
            release_summary.sort_values(
                "average_momentum",
                ascending=False
            )
            .iloc[0]
        )

        average_duration = (
            content_data["duration_min"].mean()
        )

        c1, c2, c3, c4 = st.columns(4)

        content_cards = [
            (
                "💿",
                "Album Advantage Index",
                f"{album_advantage_index:.2f}"
            ),
            (
                "🏆",
                "Leading Release Type",
                dominant_release[
                    "album_type"
                ].title()
            ),
            (
                "🔞",
                "Explicit Momentum",
                f"{explicit_average:.1f}"
            ),
            (
                "⏱",
                "Average Duration",
                f"{average_duration:.2f} min"
            )
        ]

        for col, (
            icon,
            title,
            value
        ) in zip(
            [c1, c2, c3, c4],
            content_cards
        ):

            with col:

                render_html(
                    f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            {icon}
                        </div>

                        <div class="metric-title">
                            {title}
                        </div>

                        <div class="metric-value">
                            {value}
                        </div>

                    </div>
                    """
)

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True
        )

        if album_advantage_index > 1:

            advantage_message = (
                "Album tracks currently show a stronger "
                "average comeback score than singles."
            )

        elif album_advantage_index > 0:

            advantage_message = (
                "Singles currently show a stronger average "
                "comeback score than album tracks."
            )

        else:

            advantage_message = (
                "The selected data does not contain enough "
                "album and single comeback episodes for a "
                "reliable advantage comparison."
            )

        render_html(
            f"""
            <div class="insight-banner">

                <div class="insight-banner-icon">
                    💡
                </div>

                <div>
                    <div class="insight-banner-title">
                        Release Strategy Signal
                    </div>

                    <div class="insight-banner-text">
                        {advantage_message}
                        The current Album Comeback Advantage
                        Index is
                        <b>{album_advantage_index:.2f}</b>.
                    </div>
                </div>

            </div>
            """
)

        chart1, chart2 = st.columns(2)

        with chart1:

            st.plotly_chart(
                momentum_by_album_type_chart(
                    content_data
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with chart2:

            st.plotly_chart(
                momentum_by_explicit_chart(
                    content_data
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        st.plotly_chart(
            duration_vs_momentum_chart(
                content_data
            ),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

        st.plotly_chart(
            album_size_vs_momentum_chart(
                content_data
            ),
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

        comparison1, comparison2 = st.columns(2)

        with comparison1:

            st.plotly_chart(
                retention_by_album_type_chart(
                    content_data
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with comparison2:

            st.plotly_chart(
                rank_recovery_by_content_chart(
                    content_data
                ),
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        release_table = release_summary.copy()

        release_table[
            "average_momentum"
        ] = release_table[
            "average_momentum"
        ].round(2)

        release_table[
            "average_retention"
        ] = release_table[
            "average_retention"
        ].round(2)

        release_table[
            "average_rank_recovery"
        ] = release_table[
            "average_rank_recovery"
        ].round(2)

        release_table.columns = [
            "Release Type",
            "Average Momentum",
            "Average Retention",
            "Average Rank Recovery",
            "Comeback Episodes"
        ]

        st.markdown(
            "### Release-Type Performance Summary"
        )

        st.dataframe(
            release_table,
            use_container_width=True,
            hide_index=True
        )

with recommendation_tab:

    render_html(
        """
        <div class="section-heading">
            <div>
                <h2>Strategic Recommendations</h2>
                <p>
                    Translate chart re-entry, comeback momentum and
                    fandom-intensity signals into release, promotion
                    and artist-development actions.
                </p>
            </div>
        </div>
        """
)

    executive_summary = generate_executive_summary(
        comeback_events,
        fandom_summary,
        artist_fandom
    )

    recommendations = generate_recommendations(
        comeback_events,
        fandom_summary,
        artist_fandom
    )

    render_html(
        f"""
        <div class="executive-summary-card">

            <div class="executive-summary-label">
                Executive Brief
            </div>

            <div class="executive-summary-title">
                South Korea Top 50 Momentum Outlook
            </div>

            <div class="executive-summary-text">
                {executive_summary}
            </div>

        </div>
        """
)

    recommendation_html = '<div class="recommendation-grid">'

    for recommendation in recommendations:

        recommendation_html += f"""
        <div class="recommendation-card">

            <div class="recommendation-top">

                <div class="recommendation-icon">
                    {recommendation["icon"]}
                </div>

                <div class="recommendation-priority">
                    {recommendation["priority"]} Priority
                </div>

            </div>

            <div class="recommendation-category">
                {recommendation["category"]}
            </div>

            <div class="recommendation-title">
                {recommendation["title"]}
            </div>

            <div class="recommendation-message">
                {recommendation["message"]}
            </div>

        </div>
        """

    recommendation_html += "</div>"

    render_html(recommendation_html)

    st.markdown(
        "<div style='height:25px'></div>",
        unsafe_allow_html=True
    )

    render_html(
    """
    <div style="
    position:relative;
    overflow:hidden;
    margin-top:28px;
    padding:30px 32px;
    border-radius:22px;
    background:
        linear-gradient(
            125deg,
            rgba(242,184,75,0.16),
            rgba(242,107,91,0.10),
            rgba(42,35,31,0.98)
        );
    border:1px solid rgba(242,184,75,0.32);
    border-left:6px solid #F2B84B;
    box-shadow:0 16px 36px rgba(0,0,0,0.28);
">

    <div style="
        display:flex;
        align-items:center;
        gap:14px;
        margin-bottom:18px;
    ">

        <div style="
            width:48px;
            height:48px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:14px;
            background:rgba(242,184,75,0.14);
            border:1px solid rgba(242,184,75,0.30);
            font-size:25px;
        ">
            📘
        </div>

        <div style="
            color:#FFF4E8;
            font-size:27px;
            font-weight:900;
        ">
            Methodology Note
        </div>

    </div>

    <div style="
        color:#C7B8AA;
        font-size:17px;
        line-height:1.85;
        margin-bottom:20px;
    ">
        Recommendations are generated from chart behaviour within the
        selected date range and active dashboard filters. The
        <b style="color:#FFF4E8;">
            Fandom Intensity Proxy Score
        </b>
        estimates behavioural engagement using the following analytical
        signals:
    </div>

    <div style="
        display:grid;
        grid-template-columns:repeat(2,minmax(0,1fr));
        gap:13px 16px;
    ">

        <div style="
            padding:14px 17px;
            border-radius:14px;
            background:rgba(255,244,232,0.055);
            border:1px solid rgba(255,244,232,0.10);
            color:#FFF4E8;
            font-size:16px;
            font-weight:750;
        ">
            🔁 Re-entry frequency
        </div>

        <div style="
            padding:14px 17px;
            border-radius:14px;
            background:rgba(255,244,232,0.055);
            border:1px solid rgba(255,244,232,0.10);
            color:#FFF4E8;
            font-size:16px;
            font-weight:750;
        ">
            ⚡ Comeback momentum
        </div>

        <div style="
            padding:14px 17px;
            border-radius:14px;
            background:rgba(255,244,232,0.055);
            border:1px solid rgba(255,244,232,0.10);
            color:#FFF4E8;
            font-size:16px;
            font-weight:750;
        ">
            📆 Chart persistence
        </div>

        <div style="
            padding:14px 17px;
            border-radius:14px;
            background:rgba(255,244,232,0.055);
            border:1px solid rgba(255,244,232,0.10);
            color:#FFF4E8;
            font-size:16px;
            font-weight:750;
        ">
            🚀 Recovery efficiency
        </div>

    </div>

    <div style="
        margin-top:21px;
        padding-top:18px;
        border-top:1px solid rgba(255,244,232,0.11);
        color:#AFA095;
        font-size:15px;
        line-height:1.75;
    ">
        <b style="color:#F2B84B;">Important:</b>
        This proxy does not directly measure fan population, individual
        streaming behaviour, sales, social-media activity or audience
        demographics. It should be interpreted as a chart-behaviour signal,
        rather than an exact measurement of fandom size.
    </div>

</div>
"""
)  