#!/usr/bin/env python

import argument
from PIL import Image


@argument.entrypoint
def main(*,
         input: str = 'frame_01.png',
         output: str = 'frame_02.png',
):
    img = Image.open(input)
    w, h = img.size
    img = img.crop((16, 16, w - 32, h - 32))
    img_out = Image.new("RGBA", img.size, (255, 255, 255, 0))
    img = img.resize((w // 2, h // 2))
    img_out.paste(img, (w // 4, h // 4))
    img_out.save(output)


if __name__ == '__main__':
    main()
