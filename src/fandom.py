import pandas as pd

from src.reentry import get_reentry_summary
from src.momentum import get_song_momentum_summary


def _minmax(series):
    """Normalize a numeric series to the range 0–1."""
    series = pd.to_numeric(
        series,
        errors="coerce"
    ).fillna(0)

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            0.0,
            index=series.index
        )

    return (
        series - minimum
    ) / (
        maximum - minimum
    )


def get_fandom_summary(df):
    """
    Build one fandom-intensity record per song.

    The score is a behavioural proxy rather than a direct
    measurement of fandom size.
    """

    reentry_summary = get_reentry_summary(df)
    momentum_summary = get_song_momentum_summary(df)

    fandom = reentry_summary.merge(
        momentum_summary,
        on=[
            "song_id",
            "song",
            "artist"
        ],
        how="left"
    )

    momentum_columns = [
        "comeback_events",
        "average_momentum",
        "maximum_momentum",
        "average_retention",
        "best_comeback_rank",
        "average_rank_improvement",
        "average_recovery_days"
    ]

    for column in momentum_columns:
        if column not in fandom.columns:
            fandom[column] = 0

    fandom[momentum_columns] = (
        fandom[momentum_columns]
        .fillna(0)
    )

    fandom["reentry_frequency_norm"] = _minmax(
        fandom["reentry_count"]
    )

    fandom["average_momentum_norm"] = _minmax(
        fandom["average_momentum"]
    )

    fandom["maximum_momentum_norm"] = _minmax(
        fandom["maximum_momentum"]
    )

    fandom["chart_persistence_norm"] = _minmax(
        fandom["total_chart_days"]
    )

    # Fewer days to recover is better.
    recovery_days = fandom[
        "average_recovery_days"
    ].replace(0, pd.NA)

    recovery_efficiency = (
        1 / recovery_days
    ).fillna(0)

    fandom["recovery_efficiency_norm"] = _minmax(
        recovery_efficiency
    )

    fandom["fandom_score"] = (
        0.35 * fandom["reentry_frequency_norm"]
        + 0.25 * fandom["average_momentum_norm"]
        + 0.15 * fandom["maximum_momentum_norm"]
        + 0.15 * fandom["chart_persistence_norm"]
        + 0.10 * fandom["recovery_efficiency_norm"]
    ) * 100

    fandom["fandom_score"] = (
        fandom["fandom_score"]
        .round(2)
    )

    fandom["fandom_tier"] = pd.cut(
        fandom["fandom_score"],
        bins=[
            -1,
            25,
            50,
            75,
            100
        ],
        labels=[
            "Emerging",
            "Active",
            "Strong",
            "Intense"
        ]
    )

    return fandom.sort_values(
        "fandom_score",
        ascending=False
    ).reset_index(drop=True)


def get_artist_fandom_summary(df):
    song_fandom = get_fandom_summary(df)

    artist_summary = (
        song_fandom.groupby("artist")
        .agg(
            songs=("song_id", "nunique"),
            average_fandom_score=("fandom_score", "mean"),
            maximum_fandom_score=("fandom_score", "max"),
            total_reentries=("reentry_count", "sum"),
            average_momentum=("average_momentum", "mean"),
            total_chart_days=("total_chart_days", "sum")
        )
        .reset_index()
    )

    numeric_columns = [
        "average_fandom_score",
        "maximum_fandom_score",
        "average_momentum"
    ]

    artist_summary[numeric_columns] = (
        artist_summary[numeric_columns]
        .round(2)
    )

    return artist_summary.sort_values(
        "average_fandom_score",
        ascending=False
    ).reset_index(drop=True)
