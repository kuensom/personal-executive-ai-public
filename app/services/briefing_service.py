from app.services.analysis_service import analyse_daily_context

from app.models import DailyAnalysis

def render_morning_briefing(
        analysis: DailyAnalysis,
):
    # analysis = analyse_daily_context()
    
    lines = []

    lines.append(
        "PERSONAL EXECUTIVE AI ASSISTANT"
    )
    lines.append(
        "MORNING BRIEFING"
    )
    lines.append("=" * 60)

    lines.append("")
    lines.append("1. IMMEDIATE PRIORITIES")

    if analysis.immediate_priorities:
        for index, item in enumerate(
            analysis.immediate_priorities,
            start=1,
        ):
            lines.append(
                f"{index}. {item}"
            )
    else:
        lines.append(
            "No immediate priorities identified."
        )

    lines.append("")
    lines.append("2. EMAILS REQUIRING ATTENTION")

    important_emails = [
        email
        for email in analysis.emails
        if email.priority in {
            "high",
            "medium",
        }
        or email.action_required
    ]

    if important_emails:
        for email in important_emails:
            lines.append(
                f"- [{email.priority.upper()}] "
                f"{email.summary}"
            )

            if email.suggested_action:
                lines.append(
                    f"  Suggested action: "
                    f"{email.suggested_action}"
                )

            if email.deadline:
                lines.append(
                    f"  Deadline: "
                    f"{email.deadline}"
                )
    else:
        lines.append(
            "No emails currently require attention."
        )

    lines.append("")
    lines.append("3. CALENDAR OBSERVATIONS")

    if analysis.calendar_observations:
        for observation in (
            analysis.calendar_observations
        ):
            lines.append(
                f"- {observation.message}"
            )
    else:
        lines.append(
            "No significant calendar issues identified."
        )

    lines.append("")
    lines.append("4. SUGGESTED NEXT ACTIONS")

    if analysis.suggested_next_actions:
        for index, item in enumerate(
            analysis.suggested_next_actions,
            start=1,
        ):
            lines.append(
                f"{index}. {item}"
            )
    else:
        lines.append(
            "No additional actions suggested."
        )

    return "\n".join(lines)

def main():
    analysis = analyse_daily_context()
    briefing = render_morning_briefing(analysis)

    print(briefing)


if __name__ == "__main__":
    main()