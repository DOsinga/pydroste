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


def main(input_fn, output_fn, center, scale=125, *, frames=90, fps=30):
    center_x, center_y = map(int, center.split(','))
    log_scale = math.log(scale)
    img = Image.open(input_fn)
    with imageio.get_writer(output_fn, mode='I', fps=fps) as writer:
        for frame in tqdm.tqdm(range(frames)):
            zoom = math.exp(log_scale * frame / frames)
            zoomed = zoom_at(img, zoom, scale, center_x, center_y)
            if frame == 0:
                # frame in frame:
                img = zoomed
            writer.append_data(np.array(zoomed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='beach.jpg')
    parser.add_argument('--output', type=str, default='beach.mp4')
    parser.add_argument('--center', type=str, default='1904,1940')
    parser.add_argument('--scale', type=float, default=125)
    parser.add_argument('--frames', type=float, default=90)
    parser.add_argument('--fps', type=float, default=30)

    args = parser.parse_args()

    main(args.input, args.output, args.center, args.scale,
         frames=args.frames, fps=args.fps)
