import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CHART_BG = "rgba(0,0,0,0)"
CARD_BG = "#2A231F"
TEXT_COLOR = "#FFF4E8"
MUTED_COLOR = "#C7B8AA"

CORAL = "#F26B5B"
AMBER = "#F2B84B"
CREAM = "#FFF4E8"
BROWN = "#9C6255"


def apply_chart_layout(fig, title):
    """Apply the shared visual theme and spacing to every Plotly figure."""
    fig.update_layout(
        title=dict(
            text=title,
            x=0,
            xanchor="left",
            y=0.97,
            yanchor="top",
            font=dict(
                size=25,
                color=TEXT_COLOR
            )
        ),
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=MUTED_COLOR),
        margin=dict(l=35, r=30, t=90, b=45),
        legend=dict(
            font=dict(color=MUTED_COLOR),
            bgcolor="rgba(0,0,0,0)"
        ),
        hoverlabel=dict(
            bgcolor=CARD_BG,
            font_color=CREAM
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(255,244,232,0.08)",
        zerolinecolor="rgba(255,244,232,0.08)"
    )

    fig.update_yaxes(
        gridcolor="rgba(255,244,232,0.08)",
        zerolinecolor="rgba(255,244,232,0.08)"
    )

    return fig

def popularity_trend_chart(df):
    daily_popularity = (
        df.groupby("date", as_index=False)["popularity"]
        .mean()
        .rename(columns={"popularity": "average_popularity"})
    )

    fig = px.line(
        daily_popularity,
        x="date",
        y="average_popularity",
        markers=False
    )

    fig.update_traces(
        line=dict(
            color=CORAL,
            width=3
        ),
        fill="tozeroy",
        fillcolor="rgba(242,107,91,0.10)",
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "Average popularity: %{y:.1f}"
            "<extra></extra>"
        )
    )

    fig.update_yaxes(
        title="Average Popularity",
        range=[0, 100]
    )

    fig.update_xaxes(title="Date")

    return apply_chart_layout(
        fig,
        "Average Popularity Trend"
    )


def album_type_donut(df):
    album_counts = (
        df["album_type"]
        .value_counts()
        .reset_index()
    )

    album_counts.columns = [
        "album_type",
        "count"
    ]

    fig = px.pie(
        album_counts,
        names="album_type",
        values="count",
        hole=0.62,
        color_discrete_sequence=[
            CORAL,
            AMBER,
            BROWN,
            CREAM
        ]
    )

    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Entries: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig.add_annotation(
        text=f"<b>{album_counts['count'].sum():,}</b><br>Entries",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=17,
            color=CREAM
        )
    )

    return apply_chart_layout(
        fig,
        "Release Type Distribution"
    )


def explicit_content_donut(df):
    explicit_counts = (
        df["is_explicit"]
        .map({
            True: "Explicit",
            False: "Clean"
        })
        .value_counts()
        .reset_index()
    )

    explicit_counts.columns = [
        "content_type",
        "count"
    ]

    fig = px.pie(
        explicit_counts,
        names="content_type",
        values="count",
        hole=0.62,
        color="content_type",
        color_discrete_map={
            "Explicit": CORAL,
            "Clean": AMBER
        }
    )

    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Entries: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig.add_annotation(
        text="<b>Content</b><br>Mix",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=19,
            color=CREAM
        )
    )

    return apply_chart_layout(
        fig,
        "Explicit vs Clean Content"
    )


def popularity_distribution_chart(df):
    fig = px.histogram(
        df,
        x="popularity",
        nbins=25
    )

    fig.update_traces(
        marker=dict(
            color=AMBER,
            line=dict(
                color="rgba(255,244,232,0.18)",
                width=1
            )
        ),
        hovertemplate=(
            "Popularity range: %{x}<br>"
            "Entries: %{y:,}"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Popularity Score"
    )

    fig.update_yaxes(
        title="Number of Entries"
    )

    return apply_chart_layout(
        fig,
        "Popularity Score Distribution"
    )


def top_artists_chart(df, top_n=12):
    artist_counts = (
        df["artist"]
        .value_counts()
        .head(top_n)
        .sort_values()
        .reset_index()
    )

    artist_counts.columns = [
        "artist",
        "appearances"
    ]

    fig = px.bar(
        artist_counts,
        x="appearances",
        y="artist",
        orientation="h",
        text="appearances"
    )

    fig.update_traces(
        marker=dict(color=CORAL),
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Chart appearances: %{x:,}"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Chart Appearances"
    )

    fig.update_yaxes(
        title=""
    )

    return apply_chart_layout(
        fig,
        f"Top {top_n} Artists by Chart Presence"
    )

def top_reentry_songs_chart(reentry_summary, top_n=15):
    top = (
        reentry_summary[
            reentry_summary["reentry_count"] > 0
        ]
        .sort_values(
            "reentry_count",
            ascending=False
        )
        .head(top_n)
        .sort_values("reentry_count")
    )

    fig = px.bar(
        top,
        x="reentry_count",
        y="song",
        orientation="h",
        text="reentry_count",
        hover_data=["artist"]
    )

    fig.update_traces(
        marker=dict(color=CORAL),
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Re-entries: %{x}<br>"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(title="Re-Entry Count")
    fig.update_yaxes(title="")

    return apply_chart_layout(
        fig,
        f"Top {top_n} Songs by Re-Entry Frequency"
    )


def reentry_gap_distribution_chart(reentry_events):
    fig = px.histogram(
        reentry_events,
        x="day_gap",
        nbins=30
    )

    fig.update_traces(
        marker=dict(color=AMBER),
        hovertemplate=(
            "Gap: %{x} days<br>"
            "Events: %{y}<extra></extra>"
        )
    )

    fig.update_xaxes(title="Days Outside the Chart")
    fig.update_yaxes(title="Number of Re-Entry Events")

    return apply_chart_layout(
        fig,
        "Distribution of Re-Entry Gaps"
    )


def reentry_timeline_chart(song_events, selected_song):
    fig = px.line(
        song_events,
        x="date",
        y="position",
        markers=True,
        hover_data=[
            "artist",
            "popularity",
            "day_gap",
            "is_reentry"
        ]
    )

    fig.update_traces(
        line=dict(
            color=CORAL,
            width=3
        ),
        marker=dict(
            size=9,
            color=AMBER
        ),
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "Rank: %{y}<br>"
            "<extra></extra>"
        )
    )

    fig.update_yaxes(
        title="Chart Position",
        autorange="reversed",
        range=[50, 1]
    )

    fig.update_xaxes(title="Date")

    return apply_chart_layout(
        fig,
        f"Chart Timeline — {selected_song}"
    )


def reentry_scatter_chart(reentry_summary):
    plot_df = reentry_summary[
        reentry_summary["reentry_count"] > 0
    ].copy()

    fig = px.scatter(
        plot_df,
        x="average_reentry_gap",
        y="reentry_count",
        size="total_chart_days",
        hover_name="song",
        hover_data=["artist"],
        size_max=40
    )

    fig.update_traces(
        marker=dict(
            color=CORAL,
            opacity=0.72,
            line=dict(
                color=CREAM,
                width=1
            )
        )
    )

    fig.update_xaxes(title="Average Re-Entry Gap (Days)")
    fig.update_yaxes(title="Re-Entry Frequency")

    return apply_chart_layout(
        fig,
        "Re-Entry Frequency vs Average Gap"
    )

def top_momentum_chart(song_momentum, top_n=15):
    top = (
        song_momentum
        .sort_values("maximum_momentum", ascending=False)
        .head(top_n)
        .sort_values("maximum_momentum")
    )

    fig = px.bar(
        top,
        x="maximum_momentum",
        y="song",
        orientation="h",
        text="maximum_momentum",
        hover_data=["artist", "comeback_events"]
    )

    fig.update_traces(
        marker=dict(color=CORAL),
        texttemplate="%{text:.1f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Maximum momentum: %{x:.2f}<br>"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Maximum Momentum Score",
        range=[0, 105]
    )

    fig.update_yaxes(title="")

    return apply_chart_layout(
        fig,
        f"Top {top_n} Songs by Comeback Momentum"
    )


def momentum_distribution_chart(comeback_events):
    fig = px.histogram(
        comeback_events,
        x="momentum_score",
        nbins=25
    )

    fig.update_traces(
        marker=dict(color=AMBER),
        hovertemplate=(
            "Momentum range: %{x:.1f}<br>"
            "Comeback episodes: %{y}<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Momentum Score",
        range=[0, 100]
    )

    fig.update_yaxes(title="Comeback Episodes")

    return apply_chart_layout(
        fig,
        "Momentum Score Distribution"
    )


def retention_vs_momentum_chart(comeback_events):
    fig = px.scatter(
        comeback_events,
        x="retention_days",
        y="momentum_score",
        size="rank_improvement",
        color="album_type",
        hover_name="song",
        hover_data=[
            "artist",
            "peak_rank",
            "popularity_gain",
            "days_to_peak"
        ],
        color_discrete_sequence=[
            CORAL,
            AMBER,
            BROWN,
            CREAM
        ],
        size_max=38
    )

    fig.update_xaxes(title="Post-Comeback Retention Days")
    fig.update_yaxes(
        title="Momentum Score",
        range=[0, 105]
    )

    return apply_chart_layout(
        fig,
        "Retention vs Comeback Momentum"
    )


def rank_recovery_chart(comeback_events, top_n=15):
    recovery = (
        comeback_events
        .sort_values(
            ["rank_improvement", "days_to_peak"],
            ascending=[False, True]
        )
        .head(top_n)
        .sort_values("rank_improvement")
    )

    fig = px.bar(
        recovery,
        x="rank_improvement",
        y="song",
        orientation="h",
        text="rank_improvement",
        hover_data=[
            "artist",
            "start_rank",
            "peak_rank",
            "days_to_peak"
        ]
    )

    fig.update_traces(
        marker=dict(color=AMBER),
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Rank improvement: %{x}<br>"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(title="Positions Recovered")
    fig.update_yaxes(title="")

    return apply_chart_layout(
        fig,
        "Strongest Rank Recovery After Re-Entry"
    )


def momentum_timeline_chart(song_events, selected_song):
    fig = px.scatter(
        song_events,
        x="comeback_date",
        y="momentum_score",
        size="retention_days",
        color="momentum_score",
        hover_data=[
            "peak_rank",
            "rank_improvement",
            "popularity_gain",
            "days_to_peak",
            "exit_date"
        ],
        color_continuous_scale=[
            [0, BROWN],
            [0.5, AMBER],
            [1, CORAL]
        ],
        size_max=38
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "Momentum: %{y:.2f}<br>"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(title="Comeback Date")

    fig.update_yaxes(
        title="Momentum Score",
        range=[0, 105]
    )

    fig.update_layout(
        coloraxis_showscale=False
    )
        

    return apply_chart_layout(
        fig,
        f"Comeback Momentum Timeline — {selected_song}"
    )

def top_fandom_songs_chart(fandom_summary, top_n=15):
    top = (
        fandom_summary
        .sort_values(
            "fandom_score",
            ascending=False
        )
        .head(top_n)
        .sort_values("fandom_score")
    )

    fig = px.bar(
        top,
        x="fandom_score",
        y="song",
        orientation="h",
        text="fandom_score",
        hover_data=[
            "artist",
            "reentry_count",
            "average_momentum",
            "total_chart_days",
            "fandom_tier"
        ]
    )

    fig.update_traces(
        marker=dict(color=CORAL),
        texttemplate="%{text:.1f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Fandom score: %{x:.2f}"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Fandom Intensity Proxy Score",
        range=[0, 105]
    )

    fig.update_yaxes(title="")

    return apply_chart_layout(
        fig,
        f"Top {top_n} Songs by Fandom Intensity"
    )


def fandom_distribution_chart(fandom_summary):
    fig = px.histogram(
        fandom_summary,
        x="fandom_score",
        nbins=20
    )

    fig.update_traces(
        marker=dict(color=AMBER),
        hovertemplate=(
            "Score range: %{x:.1f}<br>"
            "Songs: %{y}<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Fandom Intensity Score",
        range=[0, 100]
    )

    fig.update_yaxes(
        title="Number of Songs"
    )

    return apply_chart_layout(
        fig,
        "Fandom Score Distribution"
    )


def fandom_bubble_chart(fandom_summary):
    plot_df = fandom_summary[
        fandom_summary["reentry_count"] > 0
    ].copy()

    fig = px.scatter(
        plot_df,
        x="reentry_count",
        y="average_momentum",
        size="total_chart_days",
        color="fandom_score",
        hover_name="song",
        hover_data=[
            "artist",
            "maximum_momentum",
            "average_retention",
            "fandom_tier"
        ],
        color_continuous_scale=[
            [0, BROWN],
            [0.50, AMBER],
            [1, CORAL]
        ],
        size_max=42
    )

    fig.update_xaxes(
        title="Re-Entry Frequency"
    )

    fig.update_yaxes(
        title="Average Comeback Momentum"
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Fandom<br>Score"
        )
    )

    return apply_chart_layout(
        fig,
        "Re-Entry Frequency vs Momentum"
    )


def top_fandom_artists_chart(artist_fandom, top_n=12):
    top = (
        artist_fandom
        .sort_values(
            "average_fandom_score",
            ascending=False
        )
        .head(top_n)
        .sort_values("average_fandom_score")
    )

    fig = px.bar(
        top,
        x="average_fandom_score",
        y="artist",
        orientation="h",
        text="average_fandom_score",
        hover_data=[
            "songs",
            "total_reentries",
            "maximum_fandom_score",
            "average_momentum"
        ]
    )

    fig.update_traces(
        marker=dict(color=AMBER),
        texttemplate="%{text:.1f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Average fandom score: %{x:.2f}"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Average Fandom Score",
        range=[0, 105]
    )

    fig.update_yaxes(title="")

    return apply_chart_layout(
        fig,
        f"Top {top_n} Artists by Fandom Intensity"
    )


def fandom_tier_chart(fandom_summary):
    tier_order = [
        "Emerging",
        "Active",
        "Strong",
        "Intense"
    ]

    tier_counts = (
        fandom_summary["fandom_tier"]
        .value_counts()
        .reindex(
            tier_order,
            fill_value=0
        )
        .reset_index()
    )

    tier_counts.columns = [
        "fandom_tier",
        "songs"
    ]

    fig = px.pie(
        tier_counts,
        names="fandom_tier",
        values="songs",
        hole=0.62,
        color_discrete_sequence=[
            BROWN,
            CREAM,
            AMBER,
            CORAL
        ]
    )

    fig.update_traces(
        textinfo="percent+label",
        textposition="outside",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Songs: %{value}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig.add_annotation(
        text="<b>Fandom</b><br>Tiers",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=17,
            color=CREAM
        )
    )

    return apply_chart_layout(
        fig,
        "Fandom Intensity Segmentation"
    )

def momentum_by_album_type_chart(comeback_events):
    plot_df = comeback_events.copy()

    fig = px.box(
        plot_df,
        x="album_type",
        y="momentum_score",
        points="outliers",
        color="album_type",
        color_discrete_sequence=[
            CORAL,
            AMBER,
            BROWN,
            CREAM
        ]
    )

    fig.update_traces(
        hovertemplate=(
            "Release type: %{x}<br>"
            "Momentum score: %{y:.2f}"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Release Type"
    )

    fig.update_yaxes(
        title="Momentum Score",
        range=[0, 105]
    )

    fig.update_layout(
        showlegend=False
    )

    return apply_chart_layout(
        fig,
        "Comeback Momentum by Release Type"
    )


def momentum_by_explicit_chart(comeback_events):
    plot_df = comeback_events.copy()

    plot_df["content_type"] = plot_df[
        "is_explicit"
    ].map(
        {
            True: "Explicit",
            False: "Clean"
        }
    )

    fig = px.box(
        plot_df,
        x="content_type",
        y="momentum_score",
        points="outliers",
        color="content_type",
        color_discrete_map={
            "Explicit": CORAL,
            "Clean": AMBER
        }
    )

    fig.update_traces(
        hovertemplate=(
            "Content type: %{x}<br>"
            "Momentum score: %{y:.2f}"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Content Classification"
    )

    fig.update_yaxes(
        title="Momentum Score",
        range=[0, 105]
    )

    fig.update_layout(
        showlegend=False
    )

    return apply_chart_layout(
        fig,
        "Explicit vs Clean Comeback Momentum"
    )


def duration_vs_momentum_chart(comeback_events):
    fig = px.scatter(
        comeback_events,
        x="duration_min",
        y="momentum_score",
        size="retention_days",
        color="album_type",
        hover_name="song",
        hover_data=[
            "artist",
            "peak_rank",
            "rank_improvement",
            "popularity_gain"
        ],
        color_discrete_sequence=[
            CORAL,
            AMBER,
            BROWN,
            CREAM
        ],
        size_max=36,
        trendline="ols"
    )

    fig.update_xaxes(
        title="Song Duration (Minutes)"
    )

    fig.update_yaxes(
        title="Momentum Score",
        range=[0, 105]
    )

    return apply_chart_layout(
        fig,
        "Song Duration vs Comeback Momentum"
    )


def album_size_vs_momentum_chart(comeback_events):
    fig = px.scatter(
        comeback_events,
        x="total_tracks",
        y="momentum_score",
        size="retention_days",
        color="album_type",
        hover_name="song",
        hover_data=[
            "artist",
            "peak_rank",
            "rank_improvement",
            "popularity_gain"
        ],
        color_discrete_sequence=[
            CORAL,
            AMBER,
            BROWN,
            CREAM
        ],
        size_max=36,
        trendline="ols"
    )

    fig.update_xaxes(
        title="Tracks in Associated Release"
    )

    fig.update_yaxes(
        title="Momentum Score",
        range=[0, 105]
    )

    return apply_chart_layout(
        fig,
        "Album Size vs Comeback Momentum"
    )


def retention_by_album_type_chart(comeback_events):
    retention = (
        comeback_events.groupby(
            "album_type",
            as_index=False
        )
        .agg(
            average_retention=(
                "retention_days",
                "mean"
            ),
            comeback_events=(
                "episode",
                "count"
            )
        )
    )

    fig = px.bar(
        retention,
        x="album_type",
        y="average_retention",
        text="average_retention",
        color="album_type",
        color_discrete_sequence=[
            CORAL,
            AMBER,
            BROWN,
            CREAM
        ],
        hover_data=[
            "comeback_events"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.1f} days",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average retention: %{y:.1f} days"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Release Type"
    )

    fig.update_yaxes(
        title="Average Retention Days"
    )

    fig.update_layout(
        showlegend=False
    )

    return apply_chart_layout(
        fig,
        "Post-Comeback Retention by Release Type"
    )


def rank_recovery_by_content_chart(comeback_events):
    plot_df = comeback_events.copy()

    plot_df["content_type"] = plot_df[
        "is_explicit"
    ].map(
        {
            True: "Explicit",
            False: "Clean"
        }
    )

    recovery = (
        plot_df.groupby(
            "content_type",
            as_index=False
        )
        .agg(
            average_rank_improvement=(
                "rank_improvement",
                "mean"
            ),
            average_recovery_days=(
                "days_to_peak",
                "mean"
            )
        )
    )

    fig = px.bar(
        recovery,
        x="content_type",
        y="average_rank_improvement",
        text="average_rank_improvement",
        color="content_type",
        color_discrete_map={
            "Explicit": CORAL,
            "Clean": AMBER
        },
        hover_data=[
            "average_recovery_days"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average rank improvement: %{y:.2f}<br>"
            "<extra></extra>"
        )
    )

    fig.update_xaxes(
        title="Content Classification"
    )

    fig.update_yaxes(
        title="Average Positions Recovered"
    )

    fig.update_layout(
        showlegend=False
    )

    return apply_chart_layout(
        fig,
        "Rank Recovery by Content Classification"
    )