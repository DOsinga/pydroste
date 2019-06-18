#!/usr/bin/env python
import math

import argument
import imageio
import numpy as np
import tqdm
from PIL import Image

from pydroste import zoom_at


@argument.entrypoint
def main(*,
         input: str = 'Manhattanhenge.png',
         output: str = 'manhattanhenge.mp4',
         zoom_points: str = '665,1440,27.8;1410,1395,35;380,1295,65;1193,1460,35;108,1320,41.6;1230,1322,76',
         frames: int = 75,
         fps: float = 30):
    """Create a Droste type of movie from a still by zooming in and replacing part of it by itself."""
    zoom_points = [[*map(float, zoom_point.split(','))] for zoom_point in zoom_points.split(';')]
    base_img = Image.open(input)
    with imageio.get_writer(output, mode='I', fps=fps) as writer:
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
    main()
