import pandas as pd


def _safe_mean(series):
    if series is None or len(series) == 0:
        return 0.0

    value = pd.to_numeric(
        series,
        errors="coerce"
    ).mean()

    return 0.0 if pd.isna(value) else float(value)


def generate_recommendations(
    comeback_events,
    fandom_summary,
    artist_fandom
):
    recommendations = []

    if comeback_events.empty:
        return [
            {
                "icon": "ℹ️",
                "category": "Data Availability",
                "title": "Insufficient comeback activity",
                "message": (
                    "The selected filters contain no confirmed chart "
                    "re-entry episodes. Expand the date range or remove "
                    "some filters to generate strategic recommendations."
                ),
                "priority": "Information"
            }
        ]

    # -------------------------------------------------
    # Release-type recommendation
    # -------------------------------------------------
    release_summary = (
        comeback_events.groupby("album_type")
        .agg(
            average_momentum=("momentum_score", "mean"),
            average_retention=("retention_days", "mean"),
            comeback_events=("episode", "count")
        )
        .reset_index()
    )

    if not release_summary.empty:
        leading_release = release_summary.sort_values(
            "average_momentum",
            ascending=False
        ).iloc[0]

        recommendations.append(
            {
                "icon": "💿",
                "category": "Release Strategy",
                "title": (
                    f"Prioritize {leading_release['album_type'].title()} "
                    "campaigns for comeback activation"
                ),
                "message": (
                    f"{leading_release['album_type'].title()} releases "
                    f"record an average momentum score of "
                    f"{leading_release['average_momentum']:.1f} and "
                    f"retain chart presence for approximately "
                    f"{leading_release['average_retention']:.1f} days. "
                    "Use this release format when designing campaigns "
                    "that depend on post-launch resurgence."
                ),
                "priority": "High"
            }
        )

    # -------------------------------------------------
    # Strong fandom songs
    # -------------------------------------------------
    fandom_active = fandom_summary[
        fandom_summary["reentry_count"] > 0
    ].copy()

    if not fandom_active.empty:
        strongest_song = fandom_active.sort_values(
            "fandom_score",
            ascending=False
        ).iloc[0]

        recommendations.append(
            {
                "icon": "💗",
                "category": "Fandom Activation",
                "title": (
                    f"Build recurring campaigns around "
                    f"{strongest_song['song']}"
                ),
                "message": (
                    f"{strongest_song['song']} by "
                    f"{strongest_song['artist']} has the strongest "
                    f"fandom-intensity signal at "
                    f"{strongest_song['fandom_score']:.1f}, supported by "
                    f"{int(strongest_song['reentry_count'])} re-entries "
                    f"and {int(strongest_song['total_chart_days'])} chart "
                    "days. Anniversary content, performances, fan events "
                    "and social challenges may help reactivate similar "
                    "high-loyalty audiences."
                ),
                "priority": "High"
            }
        )

    # -------------------------------------------------
    # Fast-recovery campaigns
    # -------------------------------------------------
    fast_recovery = comeback_events[
        comeback_events["days_to_peak"] <= 2
    ]

    fast_recovery_share = (
        len(fast_recovery) / len(comeback_events) * 100
        if len(comeback_events) > 0
        else 0
    )

    recommendations.append(
        {
            "icon": "🚀",
            "category": "Promotion Timing",
            "title": "Concentrate promotion immediately after re-entry",
            "message": (
                f"{fast_recovery_share:.1f}% of comeback episodes reach "
                "their post-return peak within two days. Front-load "
                "social promotion, fan communication, short-form video "
                "and performance exposure during the first 48 hours "
                "after a track returns to the chart."
            ),
            "priority": "High"
        }
    )

    # -------------------------------------------------
    # Retention recommendation
    # -------------------------------------------------
    average_retention = _safe_mean(
        comeback_events["retention_days"]
    )

    long_retention = comeback_events[
        comeback_events["retention_days"] >= average_retention
    ]

    if not long_retention.empty:
        stable_episode = long_retention.sort_values(
            [
                "retention_days",
                "momentum_score"
            ],
            ascending=False
        ).iloc[0]

        recommendations.append(
            {
                "icon": "📆",
                "category": "Campaign Sustainability",
                "title": "Extend support for high-retention comeback tracks",
                "message": (
                    f"The average comeback remains charted for "
                    f"{average_retention:.1f} days. "
                    f"{stable_episode['song']} retained chart presence "
                    f"for {int(stable_episode['retention_days'])} days "
                    "after re-entry. Tracks that exceed the benchmark "
                    "should receive extended playlists, performance clips "
                    "and follow-up promotional content instead of a "
                    "single short campaign burst."
                ),
                "priority": "Medium"
            }
        )

    # -------------------------------------------------
    # Explicit-content recommendation
    # -------------------------------------------------
    explicit_mean = _safe_mean(
        comeback_events.loc[
            comeback_events["is_explicit"] == True,
            "momentum_score"
        ]
    )

    clean_mean = _safe_mean(
        comeback_events.loc[
            comeback_events["is_explicit"] == False,
            "momentum_score"
        ]
    )

    if explicit_mean > clean_mean:
        content_message = (
            f"Explicit tracks show stronger average momentum "
            f"({explicit_mean:.1f}) than clean tracks "
            f"({clean_mean:.1f}). Explicit content may work for "
            "audience-specific digital promotions, while broadcast and "
            "brand suitability should still be assessed separately."
        )
    else:
        content_message = (
            f"Clean tracks show stronger average momentum "
            f"({clean_mean:.1f}) than explicit tracks "
            f"({explicit_mean:.1f}). Prioritize clean versions for "
            "broad playlist placement, broadcast exposure and campaigns "
            "requiring maximum audience accessibility."
        )

    recommendations.append(
        {
            "icon": "🎙️",
            "category": "Content Positioning",
            "title": "Align content classification with market reach",
            "message": content_message,
            "priority": "Medium"
        }
    )

    # -------------------------------------------------
    # Artist portfolio recommendation
    # -------------------------------------------------
    if not artist_fandom.empty:
        top_artist = artist_fandom.sort_values(
            "average_fandom_score",
            ascending=False
        ).iloc[0]

        recommendations.append(
            {
                "icon": "🎤",
                "category": "Artist Portfolio",
                "title": (
                    f"Use {top_artist['artist']} as a benchmark "
                    "for fandom-led strategy"
                ),
                "message": (
                    f"{top_artist['artist']} leads the artist-level "
                    f"fandom analysis with an average score of "
                    f"{top_artist['average_fandom_score']:.1f} across "
                    f"{int(top_artist['songs'])} tracked songs and "
                    f"{int(top_artist['total_reentries'])} combined "
                    "re-entries. Review this artist's release timing, "
                    "fan communication and promotional cycles as a "
                    "benchmark for comparable acts."
                ),
                "priority": "Medium"
            }
        )

    # -------------------------------------------------
    # Volatility recommendation
    # -------------------------------------------------
    average_decay = _safe_mean(
        comeback_events["rank_decay_speed"]
    )

    volatile_events = comeback_events[
        comeback_events["rank_decay_speed"] > average_decay
    ]

    volatility_share = (
        len(volatile_events) / len(comeback_events) * 100
        if len(comeback_events) > 0
        else 0
    )

    recommendations.append(
        {
            "icon": "📉",
            "category": "Momentum Risk",
            "title": "Separate sharp fan surges from sustainable demand",
            "message": (
                f"{volatility_share:.1f}% of comeback episodes decay "
                "faster than the current average. Do not treat every "
                "large rank jump as sustained popularity. Combine "
                "momentum score with retention and decay speed before "
                "committing long-term marketing expenditure."
            ),
            "priority": "Medium"
        }
    )

    return recommendations


def generate_executive_summary(
    comeback_events,
    fandom_summary,
    artist_fandom
):
    if comeback_events.empty:
        return (
            "The selected data contains no confirmed comeback episodes, "
            "so momentum and fandom conclusions cannot be generated."
        )

    average_momentum = comeback_events[
        "momentum_score"
    ].mean()

    average_retention = comeback_events[
        "retention_days"
    ].mean()

    total_comebacks = len(comeback_events)

    fandom_active = fandom_summary[
        fandom_summary["reentry_count"] > 0
    ]

    if not fandom_active.empty:
        top_song = fandom_active.iloc[0]

        fandom_statement = (
            f"{top_song['song']} by {top_song['artist']} presents the "
            f"strongest fandom-intensity signal with a score of "
            f"{top_song['fandom_score']:.1f}."
        )
    else:
        fandom_statement = (
            "No songs with confirmed re-entry behaviour were available "
            "for fandom-intensity comparison."
        )

    if not artist_fandom.empty:
        top_artist = artist_fandom.iloc[0]

        artist_statement = (
            f"{top_artist['artist']} leads the artist-level fandom "
            f"benchmark with an average score of "
            f"{top_artist['average_fandom_score']:.1f}."
        )
    else:
        artist_statement = ""

    return (
        f"The filtered South Korea Top 50 dataset contains "
        f"{total_comebacks:,} confirmed comeback episodes. These "
        f"episodes achieve an average momentum score of "
        f"{average_momentum:.1f} and remain on the chart for an average "
        f"of {average_retention:.1f} days after re-entry. "
        f"{fandom_statement} {artist_statement} The analysis indicates "
        "that release decisions should account for repeated momentum "
        "bursts, immediate recovery speed and post-comeback stability, "
        "rather than evaluating tracks only through total longevity."
    )
