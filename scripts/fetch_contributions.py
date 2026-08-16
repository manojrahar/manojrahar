from pathlib import Path
from collections import defaultdict
from datetime import date, timedelta
import json
import re

import requests
from bs4 import BeautifulSoup


USERNAME = "manojrahar"
URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def get_count_from_tooltip(cell, soup):
    """Read the contribution count from GitHub's tooltip."""

    cell_id = cell.get("id")

    if not cell_id:
        return 0

    tooltip = soup.find(
        "tool-tip",
        attrs={"for": cell_id}
    )

    if not tooltip:
        return 0

    text = tooltip.get_text(" ", strip=True)

    # Examples:
    # "15 contributions on August 24th."
    # "1 contribution on January 4th."
    # "No contributions on August 17th."

    match = re.search(
        r"([\d,]+)\s+contribution",
        text,
        flags=re.IGNORECASE
    )

    if match:
        return int(match.group(1).replace(",", ""))

    return 0


def main():
    print(f"Fetching contributions for @{USERNAME}...")

    response = requests.get(
        URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "Chrome/151.0.0.0 Safari/537.36"
            )
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    cells = soup.select(
        "td.ContributionCalendar-day[data-date][data-level]"
    )

    if not cells:
        raise RuntimeError(
            "Could not find GitHub contribution cells."
        )

    days = []

    for cell in cells:
        raw_date = cell.get("data-date")
        level = cell.get("data-level")

        if not raw_date or level is None:
            continue

        try:
            contribution_date = date.fromisoformat(raw_date)
            contribution_level = int(level)
        except ValueError:
            continue

        count = get_count_from_tooltip(
            cell,
            soup
        )

        days.append(
            {
                "date": contribution_date.isoformat(),
                "count": count,
                "level": contribution_level,
            }
        )

    if not days:
        raise RuntimeError(
            "No contribution data was extracted."
        )

    # Remove duplicates.
    unique = {
        day["date"]: day
        for day in days
    }

    days = sorted(
        unique.values(),
        key=lambda item: item["date"]
    )

    # GitHub currently returns the contribution calendar
    # starting on a Sunday and covering the visible year.
    # Keep the complete returned calendar.
    start = date.fromisoformat(days[0]["date"])
    end = date.fromisoformat(days[-1]["date"])

    existing = {
        item["date"]: item
        for item in days
    }

    complete_days = []

    current = start

    while current <= end:
        key = current.isoformat()

        complete_days.append(
            existing.get(
                key,
                {
                    "date": key,
                    "count": 0,
                    "level": 0,
                }
            )
        )

        current += timedelta(days=1)

    days = complete_days

    # Total contributions.
    total = sum(
        day["count"]
        for day in days
    )

    # Best day.
    best_day = max(
        days,
        key=lambda day: day["count"]
    )

    # Longest streak.
    longest_streak = 0
    running = 0

    for day in days:
        if day["count"] > 0:
            running += 1
            longest_streak = max(
                longest_streak,
                running
            )
        else:
            running = 0

    # Current streak.
    current_streak = 0

    for day in reversed(days):
        if day["count"] > 0:
            current_streak += 1
        else:
            break

    # Monthly totals.
    monthly_totals = defaultdict(int)

    for day in days:
        month = day["date"][:7]
        monthly_totals[month] += day["count"]

    data = {
        "username": USERNAME,
        "generated_at": date.today().isoformat(),
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {
            "date": best_day["date"],
            "count": best_day["count"],
        },
        "monthly_totals": dict(
            monthly_totals
        ),
        "days": days,
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            data,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"Fetched {len(days)} days.")
    print(f"Total contributions: {total}")
    print(f"Current streak: {current_streak}")
    print(f"Longest streak: {longest_streak}")
    print(
        f"Best day: {best_day['date']} "
        f"({best_day['count']} contributions)"
    )
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
