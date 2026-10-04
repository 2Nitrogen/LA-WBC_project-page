"""Render the locomotion-performance half of manuscript Table II as SVG.

Values are transcribed from camera_ready_MS.pdf, page 7. The 0.5 m/s
LA-WBC hardware CoT is the author-confirmed correction (0.221).
"""

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "images" / "locomotion_metrics.svg"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", {key.replace("_", "-"): str(value) for key, value in attrs.items()})


def label(parent, x, y, content, *, size=27, weight="normal", anchor="middle"):
    node = element(parent, "text", x=x, y=y, fill="#000000", font_size=size,
                   font_weight=weight, text_anchor=anchor,
                   font_family="Times New Roman, Georgia, serif")
    node.text = content
    return node


def metric_value(parent, x, y, value, *, bold=False):
    """Bold only the simulation value; hardware values in parentheses stay regular."""
    if not bold:
        label(parent, x, y, value, size=25)
    elif " (" in value:
        simulation, hardware = value.split(" (", 1)
        node = label(parent, x, y, "", size=25)
        element(node, "tspan", font_weight="bold").text = simulation
        element(node, "tspan", font_weight="normal").text = f" ({hardware}"
    else:
        label(parent, x, y, value, size=25, weight="bold")


root = ET.Element(f"{{{SVG}}}svg", {
    "viewBox": "0 0 1800 440",
    "width": "1800",
    "height": "440",
    "role": "img",
    "aria-label": "Locomotion performance metrics from Table II, comparing No-adapt, Vanilla RL, and LA-WBC at 0.5 and 0.7 meters per second",
})
element(root, "rect", x=0, y=0, width=1800, height=440, fill="#ffffff")
element(root, "line", x1=12, y1=5, x2=1788, y2=5, stroke="#000000", stroke_width=2)
label(root, 900, 39, "Locomotion Performance: Simulation (Hardware)", size=34, weight="bold")
element(root, "line", x1=12, y1=52, x2=1788, y2=52, stroke="#000000", stroke_width=2)
label(root, 815, 89, "vₓᵈ = 0.5 m/s", size=29)
label(root, 1472, 89, "vₓᵈ = 0.7 m/s", size=29)
element(root, "line", x1=485, y1=100, x2=1788, y2=100, stroke="#000000", stroke_width=1)

centers = [595, 815, 1035, 1255, 1475, 1695]
label(root, 24, 132, "Metric", size=27, anchor="start")
for x, heading in zip(centers, ["No-adapt", "Vanilla RL", "Ours"] * 2):
    label(root, x, 132, heading, size=27)
element(root, "line", x1=12, y1=145, x2=1788, y2=145, stroke="#000000", stroke_width=1)

rows = [
    ("Cost of Transport", ["0.203 (0.326)", "0.153", "0.299 (0.221)", "0.406 (0.225)", "0.136", "0.297 (0.224)"], {1, 4}),
    ("Tracking error (m/s)", ["0.105 (0.306)", "0.180", "0.070 (0.112)", "0.257 (0.591)", "0.212", "0.070 (0.111)"], {2, 5}),
    ("Mean velocity (m/s)", ["0.552 (0.444)", "0.332", "0.319 (0.363)", "0.614 (0.571)", "0.504", "0.318 (0.354)"], {0, 3}),
    ("Stance-foot velocity (m/s)", ["0.297 (0.109)", "0.219", "0.165 (0.087)", "0.354 (0.162)", "0.314", "0.164 (0.089)"], {2, 5}),
    ("Base-height std. (mm)", ["2.108 (47)", "2.308", "1.531 (3)", "38.419 (39)", "2.325", "1.532 (3)"], {2, 5}),
    ("Success rate (%), 100 trials", ["98", "100", "100", "1", "100", "100"], {1, 2, 4, 5}),
]
for row_index, (metric, values, bold_columns) in enumerate(rows):
    y = 181 + row_index * 43
    label(root, 24, y, metric, size=25, anchor="start")
    for column_index, (x, value) in enumerate(zip(centers, values)):
        metric_value(root, x, y, value, bold=column_index in bold_columns)

element(root, "line", x1=4, y1=5, x2=4, y2=425, stroke="#000000", stroke_width=2)
element(root, "line", x1=13, y1=5, x2=13, y2=425, stroke="#000000", stroke_width=1)
element(root, "line", x1=1145, y1=52, x2=1145, y2=425, stroke="#000000", stroke_width=1)
element(root, "line", x1=12, y1=425, x2=1788, y2=425, stroke="#000000", stroke_width=2)

OUTPUT.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
print(OUTPUT)
