from pathlib import Path


OUTPUT = Path("info-card.svg")

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"

TEXT = "#e6edf3"
MUTED = "#8b949e"

GREEN = "#39d353"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"
ORANGE = "#f0883e"


WIDTH = 560
HEIGHT = 390


ROWS = [
    ("Role", "Full Stack Developer", GREEN),
    ("Focus", "React.js • Next.js • MERN", BLUE),
    ("Frontend", "React • Next • Tailwind CSS", BLUE),
    ("Backend", "Node • Express • REST APIs", PURPLE),
    ("Database", "MongoDB • PostgreSQL", ORANGE),
    ("React", "Hooks • Context API • State", PURPLE),
    ("Tools", "Git • GitHub • Vercel • Axios", GREEN),
]


def escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():

    row_start = 92
    row_gap = 34

    row_elements = []

    for index, (label, value, accent) in enumerate(ROWS):

        y = row_start + index * row_gap

        delay = 0.25 + index * 0.12

        row_elements.append(
            f'''
            <g opacity="0">
                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    dur="0.35s"
                    begin="{delay:.2f}s"
                    fill="freeze"
                />

                <text
                    x="30"
                    y="{y}"
                    fill="{accent}"
                    font-family="monospace"
                    font-size="13"
                    font-weight="bold"
                >{escape(label)}</text>

                <text
                    x="145"
                    y="{y}"
                    fill="{TEXT}"
                    font-family="monospace"
                    font-size="13"
                >{escape(value)}</text>
            </g>
            '''
        )

    current_y = 92 + len(ROWS) * row_gap + 16

    current_section = f'''
        <g opacity="0">
            <animate
                attributeName="opacity"
                from="0"
                to="1"
                dur="0.4s"
                begin="1.35s"
                fill="freeze"
            />

            <text
                x="30"
                y="{current_y}"
                fill="{MUTED}"
                font-family="monospace"
                font-size="11"
            >CURRENT</text>

            <text
                x="30"
                y="{current_y + 23}"
                fill="{GREEN}"
                font-family="monospace"
                font-size="13"
                font-weight="bold"
            >CubeStaX</text>

            <text
                x="145"
                y="{current_y + 23}"
                fill="{TEXT}"
                font-family="monospace"
                font-size="13"
            >Full Stack Developer Intern</text>
        </g>
    '''

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

    <rect
        x="1"
        y="1"
        width="{WIDTH - 2}"
        height="42"
        rx="11"
        fill="{PANEL}"
    />

    <circle
        cx="24"
        cy="22"
        r="5"
        fill="#ff5f56"
    />

    <circle
        cx="42"
        cy="22"
        r="5"
        fill="#ffbd2e"
    />

    <circle
        cx="60"
        cy="22"
        r="5"
        fill="#27c93f"
    />

    <text
        x="85"
        y="27"
        fill="{MUTED}"
        font-family="monospace"
        font-size="12"
    >manoj@github:~ $ whoami</text>

    <text
        x="30"
        y="68"
        fill="{TEXT}"
        font-family="monospace"
        font-size="14"
        font-weight="bold"
    >manojrahar</text>

    {''.join(row_elements)}

    {current_section}

</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
