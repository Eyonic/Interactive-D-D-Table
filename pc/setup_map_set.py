#!/usr/bin/env python3
"""Create map sets for the Interactive D&D Table."""
import os
import shutil
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw


def draw_square_grid(draw, width, height, cols, rows, color=(0, 255, 0)):
    cell_w = width / cols
    cell_h = height / rows
    for c in range(cols + 1):
        x = int(c * cell_w)
        draw.line([(x, 0), (x, height)], fill=color)
    for r in range(rows + 1):
        y = int(r * cell_h)
        draw.line([(0, y), (width, y)], fill=color)


def draw_hex_grid(draw, width, height, radius, color=(0, 255, 255)):
    hex_h = math.sqrt(3) * radius
    hex_w = 2 * radius
    horiz = hex_w * 0.75
    vertical_cells = int(math.ceil(height / hex_h))
    horizontal_cells = int(math.ceil(width / horiz))
    for r in range(vertical_cells):
        for c in range(horizontal_cells):
            x = c * horiz
            y = r * hex_h + (c % 2) * (hex_h / 2)
            points = [
                (x + radius * math.cos(math.pi / 3 * i),
                 y + radius * math.sin(math.pi / 3 * i))
                for i in range(6)
            ]
            points.append(points[0])
            draw.line(points, fill=color)


def overlay_grid(image_path, grid_type, cols=5, rows=5, radius=40):
    """Overlay a grid on the given map image."""
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    if grid_type == "hex":
        draw_hex_grid(draw, img.width, img.height, radius)
    else:
        draw_square_grid(draw, img.width, img.height, cols, rows)
    return Image.alpha_composite(img, overlay)


def copy_media(src, dest):
    if src:
        shutil.copy2(src, dest)


def main():
    set_name = input("Set name (e.g., set1): ").strip()
    if not set_name:
        print("Set name required")
        return
    out_dir = Path("sets") / set_name
    out_dir.mkdir(parents=True, exist_ok=True)

    map_path = input("Map image path (PNG/JPG): ").strip()
    if not os.path.exists(map_path):
        print("Map file not found")
        return

    grid_type = input("Grid type (square/hex) [square]: ").strip() or "square"
    if grid_type not in {"square", "hex"}:
        print("Invalid grid type")
        return

    if grid_type == "hex":
        radius = float(input("Hex radius in pixels [40]: ") or 40)
        cols = rows = 0
    else:
        cols = int(input("Grid columns [5]: ") or 5)
        rows = int(input("Grid rows [5]: ") or 5)
        radius = 40

    result = overlay_grid(map_path, grid_type, cols, rows, radius)
    map_out = out_dir / "map.png"
    result.save(map_out)
    print(f"Map saved to {map_out}")

    bgm = input("Background music path (mp3/wav): ").strip()
    if bgm:
        copy_media(bgm, out_dir / ("bgm" + Path(bgm).suffix))

    sfx_names = []
    for i in range(1, 10):
        path = input(f"Sound effect {i} path (enter to skip): ").strip()
        if path:
            dest = out_dir / f"sfx{i}" + Path(path).suffix
            copy_media(path, dest)
            sfx_names.append(dest.name)
        else:
            sfx_names.append("")

    config = {
        "grid_type": grid_type,
        "cols": cols,
        "rows": rows,
        "radius": radius,
        "bgm": Path(bgm).name if bgm else "",
        "sfx": sfx_names,
    }
    with open(out_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)
    print(f"Set created in {out_dir}")


if __name__ == "__main__":
    main()
