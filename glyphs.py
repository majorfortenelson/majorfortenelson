"""Clean vector versions of the three hand-drawn symbols shown beside the name header.

Each returns an inline <svg> (viewBox 100x40) drawn in currentColor.
"""
import math


def _fit(points, pad_x=6, pad_y=6, w=100, h=40):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    sx = (w - 2 * pad_x) / (max(xs) - min(xs))
    sy = (h - 2 * pad_y) / (max(ys) - min(ys))
    s = min(sx, sy)
    ox = (w - (max(xs) - min(xs)) * s) / 2
    oy = (h - (max(ys) - min(ys)) * s) / 2
    return [((x - min(xs)) * s + ox, (y - min(ys)) * s + oy) for x, y in points]


def _pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def _svg(inner):
    return ('<svg viewBox="0 0 100 40" aria-hidden="true" fill="none" '
            'stroke="currentColor" stroke-linecap="round">' + inner + "</svg>")


def zigzag():
    # Sharp zigzag, traced from the drawing's corners.
    raw = [(405, 350), (465, 230), (510, 365), (595, 215), (640, 350),
           (715, 225), (770, 350), (835, 245)]
    return _svg(f'<polyline points="{_pts(_fit(raw))}" stroke-width="3" stroke-linejoin="miter"/>')


def loops():
    # Zigzag with a loop at every turn: x = t + b*sin(2t), y = -sin(t); b > 0.5 makes the loops.
    raw = []
    t, end = 0.0, 6.25 * math.pi
    while t <= end:
        raw.append((t + 1.25 * math.sin(2 * t), -math.sin(t) * 3.2))
        t += 0.04
    return _svg(f'<polyline points="{_pts(_fit(raw))}" stroke-width="2.6" stroke-linejoin="round"/>')


def ribbon():
    # Thick zigzag drawn as an outline: a wide dark stroke with a white stroke on top.
    raw = [(345, 830), (440, 700), (490, 850), (590, 690), (650, 850),
           (735, 690), (790, 850), (870, 700)]
    pts = _pts(_fit(raw, pad_x=9, pad_y=8))
    return _svg(
        f'<polyline points="{pts}" stroke-width="9" stroke-linejoin="bevel" stroke-linecap="square"/>'
        f'<polyline points="{pts}" stroke="#fff" stroke-width="5" stroke-linejoin="bevel" stroke-linecap="square"/>'
    )


ALL = [zigzag, loops, ribbon]
