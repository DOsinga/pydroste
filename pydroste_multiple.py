#!/usr/bin/env python
import argparse
import math

import imageio
import numpy as np
from PIL import Image
import tqdm


def zoom_at(org_img, zoom, scale, x, y):
    w, h = org_img.size

    xz = x / zoom
    yz = y / zoom
    box = (int(x - xz), int(y - yz), int(x - xz + w / zoom), int(y - yz + h / zoom))

    img = org_img.crop(box)
    img = img.resize((w, h), Image.LANCZOS)
    w2 = int(w * zoom / scale)
    h2 = int(h * zoom / scale)
    x2 = int(x - w2 * x / w)
    y2 = int(y - h2 * y / h)
    img.paste(org_img.resize((w2, h2), Image.LANCZOS), (x2, y2))
    return img


def main(input_fn, output_fn, zoom_points, *, frames=90, fps=30):
    zoom_points = [[*map(float, zoom_point.split(','))] for zoom_point in zoom_points.split(';')]
    base_img = Image.open(input_fn)
    with imageio.get_writer(output_fn, mode='I', fps=fps) as writer:
        for idx, (center_x, center_y, scale) in enumerate(zoom_points):
            log_scale = math.log(scale)
            next_idx = (idx + 1) % len(zoom_points)
            next_center_x, next_center_y, next_scale = zoom_points[next_idx]
            img = zoom_at(base_img, 1.0, next_scale, next_center_x, next_center_y)
            for frame in tqdm.tqdm(range(frames)):
                zoom = math.exp(log_scale * frame / frames)
                zoomed = zoom_at(img, zoom, scale, center_x, center_y)
                writer.append_data(np.array(zoomed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='Manhattanhenge.png')
    parser.add_argument('--output', type=str, default='manhattanhenge.mp4')
    parser.add_argument('--zoom_points', type=str, default='665,1440,27.8;'
                                                           '1410,1395,35;'
                                                           '380,1295,65;'
                                                           '1193,1460,35;'
                                                           '108,1320,41.6;'
                                                           '1230,1322,76')
    parser.add_argument('--frames', type=float, default=75)
    parser.add_argument('--fps', type=float, default=30)

    args = parser.parse_args()

    main(args.input, args.output, args.zoom_points,
         frames=args.frames, fps=args.fps)
