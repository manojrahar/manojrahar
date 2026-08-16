from pathlib import Path

from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("manoj-ascii.svg")

# Bright -> dark.
RAMP = " .`:-=+*cs#%@"

# More detail than the previous version.
TARGET_WIDTH = 110

# Character aspect correction.
CHAR_ASPECT = 0.50

# GitHub dark-mode background.
BG_COLOR = "#0d1117"

# Very bright pixels become background/empty space.
BACKGROUND_THRESHOLD = 235


def brightness_to_char(value: int) -> str:
    """
    Convert brightness to an ASCII character.

    Bright pixels -> sparse characters
    Dark pixels   -> dense characters
    """
    index = int(
        (255 - value)
        / 255
        * (len(RAMP) - 1)
    )

    return RAMP[index]


def brightness_to_gray(value: int) -> str:
    """
    Convert grayscale brightness into a visible
    grayscale text color.

    Dark source pixels become brighter characters.
    """

    inverted = 255 - value

    gray = int(
        105 + (inverted / 255) * 145
    )

    return f"rgb({gray},{gray},{gray})"


def escape(text: str) -> str:
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"{INPUT} not found. "
            "Run prep_photo.py first."
        )

    image = Image.open(INPUT).convert("L")

    width, height = image.size

    columns = TARGET_WIDTH

    rows = max(
        1,
        int(
            (height / width)
            * columns
            * CHAR_ASPECT
        )
    )

    image = image.resize(
        (columns, rows),
        Image.Resampling.LANCZOS
    )

    pixels = image.load()

    line_height = 13
    font_size = 11

    svg_width = columns * 7.0
    svg_height = (
        rows * line_height
        + 20
    )

    definitions = []
    text_elements = []

    for row in range(rows):

        y = 17 + row * line_height

        line_parts = []

        for x in range(columns):

            value = pixels[x, row]

            # Very bright background pixels are left empty.
            if value >= BACKGROUND_THRESHOLD:
                char = " "
            else:
                char = brightness_to_char(value)

            if char == " ":
                line_parts.append(
                    f'<tspan x="{x * 7.0:.1f}">{char}</tspan>'
                )
            else:
                gray = brightness_to_gray(value)

                line_parts.append(
                    f'''
                    <tspan
                        x="{x * 7.0:.1f}"
                        fill="{gray}"
                    >{escape(char)}</tspan>
                    '''
                )

        clip_id = f"row-{row}"

        definitions.append(
            f'''
            <clipPath id="{clip_id}">
                <rect
                    x="0"
                    y="{y - line_height + 2}"
                    width="0"
                    height="{line_height + 2}"
                >
                    <animate
                        attributeName="width"
                        from="0"
                        to="{svg_width}"
                        dur="0.55s"
                        begin="{row * 0.035:.3f}s"
                        fill="freeze"
                    />
                </rect>
            </clipPath>
            '''
        )

        text_elements.append(
            f'''
            <text
                x="0"
                y="{y}"
                font-family="monospace"
                font-size="{font_size}px"
                xml:space="preserve"
                clip-path="url(#{clip_id})"
            >
                {''.join(line_parts)}
            </text>
            '''
        )

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{svg_width:.0f}"
    height="{svg_height:.0f}"
    viewBox="0 0 {svg_width:.0f} {svg_height:.0f}"
>

    <rect
        width="100%"
        height="100%"
        fill="{BG_COLOR}"
    />

    <defs>
        {''.join(definitions)}
    </defs>

    {''.join(text_elements)}

</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
