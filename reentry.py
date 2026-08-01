import pandas as pd


def prepare_reentry_data(df):
    data = df.copy()

    data["song_id"] = (
        data["song"].str.strip().str.lower()
        + " | "
        + data["artist"].str.strip().str.lower()
    )

    data = data.sort_values(
        ["song_id", "date", "position"]
    ).reset_index(drop=True)

    data["day_gap"] = (
        data.groupby("song_id")["date"]
        .diff()
        .dt.days
    )

    data["is_reentry"] = data["day_gap"] > 1

    return data


def get_reentry_summary(df):
    data = prepare_reentry_data(df)

    reentry_only = data[data["is_reentry"]].copy()

    summary = (
        data.groupby("song_id")
        .agg(
            song=("song", "first"),
            artist=("artist", "first"),
            total_chart_days=("date", "count"),
            first_entry=("date", "min"),
            last_entry=("date", "max"),
            reentry_count=("is_reentry", "sum")
        )
        .reset_index()
    )

    gap_summary = (
        reentry_only.groupby("song_id")
        .agg(
            average_reentry_gap=("day_gap", "mean"),
            maximum_reentry_gap=("day_gap", "max")
        )
        .reset_index()
    )

    summary = summary.merge(
        gap_summary,
        on="song_id",
        how="left"
    )

    summary[
        ["average_reentry_gap", "maximum_reentry_gap"]
    ] = summary[
        ["average_reentry_gap", "maximum_reentry_gap"]
    ].fillna(0)

    return summary


def get_reentry_events(df):
    data = prepare_reentry_data(df)

    events = data[data["is_reentry"]].copy()

    return events[
        [
            "date",
            "song_id",
            "song",
            "artist",
            "position",
            "popularity",
            "day_gap",
            "album_type",
            "is_explicit"
        ]
    ]