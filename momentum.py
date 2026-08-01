import numpy as np
import pandas as pd

from src.reentry import prepare_reentry_data


def _minmax(series):
    """Normalize a numeric series to the range 0–1."""
    series = pd.to_numeric(series, errors="coerce").fillna(0)

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0.0, index=series.index)

    return (series - minimum) / (maximum - minimum)


def prepare_episode_data(df):
    """
    Divide every song's chart history into continuous chart episodes.

    Episode 0 = initial chart run
    Episode 1+ = genuine comeback/re-entry episodes
    """
    data = prepare_reentry_data(df)

    data["episode"] = (
        data.groupby("song_id")["is_reentry"]
        .cumsum()
        .astype(int)
    )

    return data


def get_episode_summary(df):
    data = prepare_episode_data(df)

    episode_rows = []

    for (song_id, episode), group in data.groupby(
        ["song_id", "episode"],
        sort=False
    ):
        group = group.sort_values("date").reset_index(drop=True)

        peak_index = group["position"].idxmin()
        peak_row = group.loc[peak_index]

        start_date = group["date"].iloc[0]
        end_date = group["date"].iloc[-1]
        peak_date = peak_row["date"]

        retention_days = group["date"].nunique()
        days_to_peak = int((peak_date - start_date).days)

        days_after_peak = int((end_date - peak_date).days)

        start_rank = int(group["position"].iloc[0])
        peak_rank = int(group["position"].min())
        end_rank = int(group["position"].iloc[-1])

        start_popularity = float(group["popularity"].iloc[0])
        peak_popularity = float(group["popularity"].max())

        rank_improvement = max(start_rank - peak_rank, 0)
        popularity_gain = max(
            peak_popularity - start_popularity,
            0
        )

        if days_after_peak > 0:
            rank_decay_speed = max(
                (end_rank - peak_rank) / days_after_peak,
                0
            )
        else:
            rank_decay_speed = 0

        episode_rows.append(
            {
                "song_id": song_id,
                "episode": episode,
                "song": group["song"].iloc[0],
                "artist": group["artist"].iloc[0],
                "comeback_date": start_date,
                "exit_date": end_date,
                "peak_date": peak_date,
                "retention_days": retention_days,
                "days_to_peak": days_to_peak,
                "start_rank": start_rank,
                "peak_rank": peak_rank,
                "end_rank": end_rank,
                "rank_improvement": rank_improvement,
                "start_popularity": start_popularity,
                "peak_popularity": peak_popularity,
                "popularity_gain": popularity_gain,
                "rank_decay_speed": rank_decay_speed,
                "album_type": group["album_type"].iloc[0],
                "total_tracks": group["total_tracks"].iloc[0],
                "duration_min": (
                    group["duration_ms"].iloc[0] / 60000
                ),
                "is_explicit": group["is_explicit"].iloc[0]
            }
        )

    episode_summary = pd.DataFrame(episode_rows)

    return episode_summary


def get_comeback_events(df):
    """
    Return genuine comeback episodes only.
    Episode 0, the initial chart entry, is excluded.
    """
    episode_summary = get_episode_summary(df)

    comeback_events = episode_summary[
        episode_summary["episode"] > 0
    ].copy()

    if comeback_events.empty:
        comeback_events["momentum_score"] = pd.Series(dtype=float)
        comeback_events["recovery_speed"] = pd.Series(dtype=float)

        return comeback_events

    # Faster peak achievement receives a higher recovery score.
    comeback_events["recovery_speed"] = (
        1 / (comeback_events["days_to_peak"] + 1)
    )

    comeback_events["rank_improvement_norm"] = _minmax(
        comeback_events["rank_improvement"]
    )

    comeback_events["popularity_gain_norm"] = _minmax(
        comeback_events["popularity_gain"]
    )

    comeback_events["retention_norm"] = _minmax(
        comeback_events["retention_days"]
    )

    comeback_events["recovery_speed_norm"] = _minmax(
        comeback_events["recovery_speed"]
    )

    # Lower decay is better, so the normalized value is inverted.
    comeback_events["stability_norm"] = (
        1 - _minmax(comeback_events["rank_decay_speed"])
    )

    comeback_events["momentum_score"] = (
        0.30 * comeback_events["rank_improvement_norm"]
        + 0.20 * comeback_events["popularity_gain_norm"]
        + 0.25 * comeback_events["retention_norm"]
        + 0.15 * comeback_events["recovery_speed_norm"]
        + 0.10 * comeback_events["stability_norm"]
    ) * 100

    comeback_events["momentum_score"] = (
        comeback_events["momentum_score"].round(2)
    )

    return comeback_events


def get_song_momentum_summary(df):
    comeback_events = get_comeback_events(df)

    if comeback_events.empty:
        return pd.DataFrame(
            columns=[
                "song_id",
                "song",
                "artist",
                "comeback_events",
                "average_momentum",
                "maximum_momentum",
                "average_retention",
                "best_comeback_rank",
                "average_rank_improvement",
                "average_recovery_days"
            ]
        )

    summary = (
        comeback_events.groupby("song_id")
        .agg(
            song=("song", "first"),
            artist=("artist", "first"),
            comeback_events=("episode", "count"),
            average_momentum=("momentum_score", "mean"),
            maximum_momentum=("momentum_score", "max"),
            average_retention=("retention_days", "mean"),
            best_comeback_rank=("peak_rank", "min"),
            average_rank_improvement=("rank_improvement", "mean"),
            average_recovery_days=("days_to_peak", "mean")
        )
        .reset_index()
    )

    numeric_columns = [
        "average_momentum",
        "maximum_momentum",
        "average_retention",
        "average_rank_improvement",
        "average_recovery_days"
    ]

    summary[numeric_columns] = summary[numeric_columns].round(2)

    return summary