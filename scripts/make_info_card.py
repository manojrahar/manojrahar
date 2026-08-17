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
HEIGHT = 748


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

    # The portrait is tall, so spread the card content
    # vertically instead of leaving a large empty area.
    row_start = 170
    row_gap = 58

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
                    font-size="14"
                    font-weight="bold"
                >{escape(label)}</text>

                <text
                    x="145"
                    y="{y}"
                    fill="{TEXT}"
                    font-family="monospace"
                    font-size="14"
                >{escape(value)}</text>
            </g>
            '''
        )

    current_y = 640

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

            <line
                x1="30"
                y1="{current_y - 42}"
                x2="{WIDTH - 30}"
                y2="{current_y - 42}"
                stroke="{BORDER}"
                stroke-width="1"
            />

            <text
                x="30"
                y="{current_y}"
                fill="{MUTED}"
                font-family="monospace"
                font-size="12"
            >CURRENT</text>

            <text
                x="30"
                y="{current_y + 30}"
                fill="{GREEN}"
                font-family="monospace"
                font-size="14"
                font-weight="bold"
            >CubeStaX</text>

            <text
                x="145"
                y="{current_y + 30}"
                fill="{TEXT}"
                font-family="monospace"
                font-size="14"
            >Full Stack Developer Intern</text>
        </g>
    '''

    footer = f'''
        <g opacity="0">
            <animate
                attributeName="opacity"
                from="0"
                to="1"
                dur="0.4s"
                begin="1.65s"
                fill="freeze"
            />

            <text
                x="30"
                y="720"
                fill="{MUTED}"
                font-family="monospace"
                font-size="11"
            >status: building • learning • shipping</text>
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
        height="48"
        rx="11"
        fill="{PANEL}"
    />

    <circle
        cx="24"
        cy="25"
        r="5"
        fill="#ff5f56"
    />

    <circle
        cx="42"
        cy="25"
        r="5"
        fill="#ffbd2e"
    />

    <circle
        cx="60"
        cy="25"
        r="5"
        fill="#27c93f"
    />

    <text
        x="85"
        y="30"
        fill="{MUTED}"
        font-family="monospace"
        font-size="12"
    >manoj@github:~ $ whoami</text>

    <text
        x="30"
        y="95"
        fill="{TEXT}"
        font-family="monospace"
        font-size="16"
        font-weight="bold"
    >manojrahar</text>

    <line
        x1="30"
        y1="120"
        x2="{WIDTH - 30}"
        y2="120"
        stroke="{BORDER}"
        stroke-width="1"
    />

    {''.join(row_elements)}

    {current_section}

    {footer}

</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Created: {OUTPUT}")
    print(f"Size: {WIDTH}x{HEIGHT}")


if __name__ == "__main__":
    main()
