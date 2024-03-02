import random

def get_random_pastel_color():
    # List of standard HTML pastel colors based on common definitions and naming conventions.
    pastel_colors = [
        "LightPink", "Pink", "LightCoral", "LavenderBlush", "MistyRose",
        "LightSalmon", "Salmon", "LightSkyBlue", "PowderBlue", "LightBlue",
        "PaleTurquoise", "LightSteelBlue", "LightCyan", "PaleGoldenRod", 
        "LightGoldenRodYellow", "LightYellow", "LightGreen", "PaleGreen",
        "SeaShell", "MintCream", "LemonChiffon", "LightGray", "Lavender",
        "FloralWhite", "AliceBlue", "GhostWhite", "Honeydew", "Ivory",
        "Azure", "Snow", "Linen", "Beige", "OldLace"
    ]

    return random.choice(pastel_colors)
