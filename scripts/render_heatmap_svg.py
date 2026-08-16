from pathlib import Path
from datetime import date
import json


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

BG = "#0d1117"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
BORDER = "#30363d"

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

CELL = 13
GAP = 3

COLUMNS = 53
ROWS = 7

LABEL_WIDTH = 32
LEFT = 20 + LABEL_WIDTH
TOP = 58

GRID_WIDTH = COLUMNS * CELL + (COLUMNS - 1) * GAP
GRID_HEIGHT = ROWS * CELL + (ROWS - 1) * GAP

WIDTH = LEFT + GRID_WIDTH + 24
HEIGHT = TOP + GRID_HEIGHT + 72


def escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"{INPUT} not found. Run fetch_contributions.py first."
        )

    data = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    days = data["days"]

    by_date = {
        item["date"]: item
        for item in days
    }

    first_date = date.fromisoformat(
        days[0]["date"]
    )

    # Move backwards to the Sunday beginning the calendar.
    first_sunday = first_date.fromordinal(
        first_date.toordinal()
        - ((first_date.weekday() + 1) % 7)
    )

    cells = []

    for column in range(COLUMNS):
        for row in range(ROWS):

            current = first_sunday.fromordinal(
                first_sunday.toordinal()
                + column * 7
                + row
            )

            key = current.isoformat()

            item = by_date.get(
                key,
                {
                    "date": key,
                    "count": 0,
                    "level": 0,
                }
            )

            x = LEFT + column * (CELL + GAP)
            y = TOP + row * (CELL + GAP)

            delay = (
                column * 0.018
                + row * 0.025
            )

            level = max(
                0,
                min(
                    len(PALETTE) - 1,
                    int(item["level"])
                )
            )

            color = PALETTE[level]

            cells.append(
                f'''
                <rect
                    x="{x}"
                    y="{y}"
                    width="{CELL}"
                    height="{CELL}"
                    rx="3"
                    fill="{color}"
                    opacity="0"
                >
                    <animate
                        attributeName="opacity"
                        from="0"
                        to="1"
                        dur="0.3s"
                        begin="{delay:.3f}s"
                        fill="freeze"
                    />
                </rect>
                '''
            )

    total = data["total"]
    longest = data["longest_streak"]
    best = data["best_day"]

    title = f"{total:,} contributions in the last year"

    footer = (
        f"Longest streak: {longest} days"
        f"   •   Best day: {best['date']}"
        f" ({best['count']} contributions)"
    )

    # Day labels.
    labels = []

    for row, label in [
        (0, "Sun"),
        (2, "Tue"),
        (4, "Thu"),
        (6, "Sat"),
    ]:
        y = TOP + row * (CELL + GAP) + 10

        labels.append(
            f'''
            <text
                x="{LEFT - 9}"
                y="{y}"
                text-anchor="end"
                fill="{MUTED}"
                font-family="monospace"
                font-size="9"
            >{label}</text>
            '''
        )

    # Legend.
    legend_width = len(PALETTE) * 17
    legend_x = WIDTH - legend_width - 38
    legend_y = HEIGHT - 42

    legend = [
        f'''
        <rect
            x="{legend_x + i * 17}"
            y="{legend_y}"
            width="12"
            height="12"
            rx="3"
            fill="{color}"
        />
        '''
        for i, color in enumerate(PALETTE)
    ]

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>
    <rect
        x="0.5"
        y="0.5"
        width="{WIDTH - 1}"
        height="{HEIGHT - 1}"
        rx="12"
        fill="{BG}"
        stroke="{BORDER}"
    />

    <text
        x="20"
        y="30"
        fill="{TEXT}"
        font-family="monospace"
        font-size="14"
        font-weight="bold"
    >manoj@github:~ $ ./contributions.sh</text>

    <text
        x="20"
        y="48"
        fill="{MUTED}"
        font-family="monospace"
        font-size="10"
    >{escape(title)}</text>

    {''.join(labels)}

    {''.join(cells)}

    <text
        x="20"
        y="{HEIGHT - 40}"
        fill="{MUTED}"
        font-family="monospace"
        font-size="9"
    >Less</text>

    {''.join(legend)}

    <text
        x="{legend_x + legend_width + 6}"
        y="{legend_y + 10}"
        fill="{MUTED}"
        font-family="monospace"
        font-size="9"
    >More</text>

    <text
        x="20"
        y="{HEIGHT - 16}"
        fill="{MUTED}"
        font-family="monospace"
        font-size="9"
    >{escape(footer)}</text>
</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Created: {OUTPUT}")
    print(f"Total displayed: {total}")


if __name__ == "__main__":
    main()
