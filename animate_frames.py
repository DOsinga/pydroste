#!/usr/bin/env python
import math

import argument
import imageio
import numpy as np
import tqdm
from PIL import Image


def zoom_at(org_img, zoom, x, y):
    w, h = org_img.size

    xz = x / zoom
    yz = y / zoom
    box = (int(x - xz), int(y - yz), int(x - xz + w / zoom), int(y - yz + h / zoom))

    img = org_img.crop(box)
    img = img.resize((w, h), Image.LANCZOS)
    return img


@argument.entrypoint
def main(*,
         frame_count: int = 38,
         target: str = 'dalle',
         frames: int = 40,
         fps: float = 30):
    log_scale = math.log(1.82)
    with imageio.get_writer(target + ".mp4", mode='I', fps=fps) as writer:
        for i in range(frame_count, 0, -1):
            img = Image.open(target + '/frame' + str(i) + ".png")
            w, h = img.size
            for frame in tqdm.tqdm(range(frames)):
                if i == 1 and frame == frames // 2:
                    break
                zoom = math.exp(log_scale * frame / (frames))
                zoomed = zoom_at(img, zoom, w // 2 + 64, h // 2 + 64)
                w, h = zoomed.size
                zoomed = zoomed.crop((16, 16, w - 32, h - 32))
                writer.append_data(np.array(zoomed))


if __name__ == '__main__':
    main()
