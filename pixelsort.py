#!/usr/bin/env python3
"""
pixelsort - rearranges the pixels of an input image via sorting them by color
"""
import math
import sys

import colorsys
from PIL import Image


__version__ = "0.2.0"


def lum (r,g,b):
    """
    sorting directly for the perceived luminosity of a colour
    """
    return math.sqrt( .241 * r + .691 * g + .068 * b )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        img_in = Image.open("img0.png")
    else:
        img_in = Image.open(sys.argv[1])

    # get the image as pixelmap (PixelAcces instance)
    # this allows accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img_in_pixels = img_in.load()
    [xs, ys] = img_in.size
    colors_rgb = []
    # Examine each pixel in the image file
    for x in range(0, xs):
      for y in range(0, ys):
        # ( )  Get the RGB color of the pixel
        [r, g, b] = img_in_pixels[x, y]
        colors_rgb.append([r,g,b])

    # sort the colors by choosen algo
    colors_s = colors_rgb
    sort_algo = 10
    if len(sys.argv) >= 4:
        sort_algo = int(sys.argv[3])
    if sort_algo == 0: # selftest 1:1 samme picture out as in
        colors_s = colors_rgb
    elif sort_algo == 1:
        colors_s.sort() # stupido
    elif sort_algo == 10:
        colors_s.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb) )
    elif sort_algo == 20:
        colors_s.sort(key=lambda rgb: lum(*rgb) )

    # create the suiting output image
    img_out = Image.new('RGB', (xs, ys), 'white')
    img_out_pixels = img_out.load()
    # iterate over every pixel of the image and set it to the value
    # corresponding the now ordered colors  ...
    for x in range(0, xs):
      for y in range(0, ys):
          idx = x * ys + y
          img_out_pixels[x,y] = tuple(colors_s[idx])
    if len(sys.argv) < 3:
        img_out.show()
    else:
        f_out = sys.argv[2]
        img_out.save(f_out)
