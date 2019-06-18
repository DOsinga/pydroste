#!/usr/bin/env python
import math

import argument
import imageio
import numpy as np
import tqdm
from PIL import Image


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


@argument.entrypoint
def main(*,
         input: str = 'beach.jpg',
         output: str = 'beach.mp4',
         center: str = '1904,1940',
         scale: float = 125,
         frames: int = 90,
         fps: float = 30):
    """Create a Droste type of movie from a still by zooming in and replacing part of it by itself."""
    center_x, center_y = map(int, center.split(','))
    log_scale = math.log(scale)
    img = Image.open(input)
    with imageio.get_writer(output, mode='I', fps=fps) as writer:
        for frame in tqdm.tqdm(range(frames)):
            zoom = math.exp(log_scale * frame / frames)
            zoomed = zoom_at(img, zoom, scale, center_x, center_y)
            if frame == 0:
                # frame in frame:
                img = zoomed
            writer.append_data(np.array(zoomed))


if __name__ == '__main__':
    main()
