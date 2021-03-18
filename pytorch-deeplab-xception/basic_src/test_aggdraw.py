#!/usr/bin/env python
# Filename: test_aggdraw.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 24 June, 2016
"""

import aggdraw
import math

from PIL import Image

##
# (Internal) Calculates arrowhead polygon for a given line segment.

def draw_text(draw,xy,text_str):
    # font = aggdraw.Font('black', 'times')
    font = aggdraw.Font('red','/Library/Fonts/Georgia.ttf')
    draw.text(xy, text_str, font)
    # draw.text(xy, text_str)
    return True


def arrowhead((x0, y0), (x1, y1), width=1, arrowshape=(8, 10, 3)):

    # determine arrowhead orientation
    dx, dy = x0 - x1, y0 - y1
    l = math.hypot(dx, dy)
    if l == 0: # zero length, no specific direction
        return (x0, y0, x1, y1), (x0, y0, x0, y0, x0, y0)
    t, o = complex(dx/l, dy/l), complex(x0, y0) # orientation (theta), offset

    # create an arrowhead, rotate it according to orientation,
    # and translate it to match the starting point
    w = width/2.0
    if isinstance(arrowshape, type(())):
        a, b, c = arrowshape
    else:
        # if not a tuple, assume it's a string
        a, b, c = map(int, arrowshape.split())

    head = []
    for x, y in [(0, 0), (-b, -(c+w)), (-a, -w), (-a, w), (-b, c+w)]:
        c = complex(x, y)*t + o
        head.append(c.real)
        head.append(c.imag)

    # adjust endpoint to make sure the line doesn't show through
    end = complex(-a, 0)*t + o

    return (end.real, end.imag, x1, y1), head

##
# Draws a polyline on an aggdraw canvas, adding arrows to the line ends.
#
# @param draw An aggdraw drawing handle.
# @param data Coordinate array [x0, y0, x1, y1, ...].
# @keyparam color The line color.
# @keyparam width The line width.
# @keyparam arrow Arrow style ("none", "first", "last", or "both").
# @keyparam arrowshape Arrow shape descriptor.

def line(draw, data, color="black", width=1, arrow="both", arrowshape=(8, 10, 3)):

    data = list(data)

    last = first = None
    if arrow == "first" or arrow == "both":
        lxy, first = arrowhead(
            (data[0], data[1]), (data[2], data[3]), width, arrowshape
            )
        data[0], data[1] = lxy[0], lxy[1]
    if arrow == "last" or arrow == "both":
        lxy, last = arrowhead(
            (data[-2], data[-1]), (data[-4], data[-3]), width, arrowshape
            )
        data[-2], data[-1] = lxy[0], lxy[1]

    draw.line(data, aggdraw.Pen(color, width))

    if first:
        draw.polygon(first, aggdraw.Brush(color))
    if last:
        draw.polygon(last, aggdraw.Brush(color))

# --------------------------------------------------------------------

if __name__ == "__main__":

    im = Image.new("RGB", (200, 200), "black")
    draw = aggdraw.Draw(im)
    # line(draw, (50, 110, 100, 160), arrow="both")
    line(draw, (50, 50, 50, 80), color='red',width=2,arrow='last',arrowshape=(8,10,3))
    draw.flush()
    im.show()
