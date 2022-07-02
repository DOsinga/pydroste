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
         output: str = 'dalle.mp4',
         frames: int = 40,
         fps: float = 30):
    log_scale = math.log(1.82)
#    img1 = Image.open('dalle/frame1.png')
#    img2 = Image.open('dalle/frame2.png')
#    zoom = zoom_at(img2, 1.82, 512 + 64, 512 + 66)
#    zoom = zoom.crop((512, 0, 1024, 1024))
#    img1.paste(zoom, (512, 0))
#    img1.save("test.png")
#    return
    with imageio.get_writer(output, mode='I', fps=fps) as writer:
        for i in range(frame_count, 0, -1):
            img = Image.open('dalle/frame' + str(i) + ".png")
            w, h = img.size
            #img = img.crop((16, 16, w - 32, h - 32))
            #img = img.resize((1024, 1024))
            for frame in tqdm.tqdm(range(frames)):
                zoom = math.exp(log_scale * frame / (frames))
                zoomed = zoom_at(img, zoom, w // 2 + 64, h // 2 + 64)
                w, h = zoomed.size
                zoomed = zoomed.crop((16, 16, w - 32, h - 32))
                #zoomed = zoom_at(img, zoom, w // 2, h // 2)
                writer.append_data(np.array(zoomed))


if __name__ == '__main__':
    main()
