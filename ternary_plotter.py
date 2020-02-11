from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import datetime
import time
import os

"""
To add a new chart, add a record to the "charts" list below in the following form:

("NAME OF CHART", "URL TO IMAGE", (X,Y,"TOP LABEL"), (X,Y,"LEFT LABEL"), (X,Y,"RIGHT LABEL")),

X and Y are the coordinates of the relevant point in the image. This can be found 
using any photo editing software, including Microsoft Paint.

It is important that the points are listed in the order of top, left, right.
"""

charts = [("Blank", "blank.png", (428, 62, "Top"), (64, 691, "Left"), (793, 691, "Right")),
          ("Soil", "soil.png", (320, 34, "Clay"), (33, 531, "Sand"), (607, 531, "Silt")),
          ("Igneous Rock", "igneous.jpg", (300, 27, "Q"), (30, 494, "A"), (570, 494, "P")),

          ]


def plot_point(A, B, C, color, which, label, image):
    # To avoid dividing by zero.
    if A == 0 and B == 0 and C == 0:
        A = 1
        B = 1
        C = 1

    # Get the locations of the top, left, and right points in the image.
    top = (charts[which][2][0], charts[which][2][1])
    left = (charts[which][3][0], charts[which][3][1])
    right = (charts[which][4][0], charts[which][4][1])

    # Scale the values in proportion to sum to 1.0 if they don't already.
    G = (B + C + A) / 1.0
    B = B * G
    C = C * G
    A = A * G

    # Calculate x, y for the values with points A,B,C located at (0.5,1),(0,0),(1,0)
    x = (2.0 * C + A) / (A + B + C) / 2.0
    y = A / (A + B + C)

    # Scale x and y to proper dimensions for the chart, flipping the y axis, and
    # offsetting the points so that they line up with the image.
    x = (x * (right[0] - left[0])) + left[0]
    y = (-y * (left[1] - top[1])) + left[1]

    # Draw the dot on the image.
    r = 3
    leftUpPoint = (x - r, y - r)
    rightDownPoint = (x + r, y + r)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw = ImageDraw.Draw(image)
    try:
        draw.ellipse(twoPointList, fill=color, outline=color)
    except:
        print("Unknown color specifier '%s', using red instead." % color)
        color = "red"
        draw.ellipse(twoPointList, fill=color, outline=color)

    # Draw the label on the image.
    fnt = ImageFont.truetype("fonts/NotoMono-Regular.ttf", 20)
    draw.text((x, y), label, fill=color, font=fnt)

    return


def update_labels(*args):
    # A utility function that updates the titles of the A, B, and C text fields
    # when a chart is selected.
    a_widget.description = charts[which_plot.value][2][2]
    b_widget.description = charts[which_plot.value][3][2]
    c_widget.description = charts[which_plot.value][4][2]


for i, chart in enumerate(charts):
    print "%s: %s" % (i + 1, chart[0])
print
print "Please choose a number 1-%s to select a chart to plot on." % (len(charts))
which = int(raw_input(">").strip()) - 1

current_image = Image.open("images/" + charts[which][1])
current_image = current_image.convert("RGB")

print("Reading .csv file...")
with open("points.csv", "r") as f:
    for line in f:
        if line.strip() == "" or line.strip()[0] == "#":
            continue
        line = line.replace("\t", ",")
        parts = [i.strip() for i in line.split(",")]
        try:
            a_value = float(parts[0])
            b_value = float(parts[1])
            c_value = float(parts[2])
        except ValueError:
            print "Can't parse values %s,%s,%s into floating point numbers" % (parts[0], parts[1], parts[2])
            continue
        if len(parts) >= 4:
            color = parts[3]
            if color == "":
                color = "red"
        else:
            color = "red"
        if len(parts) >= 5:
            label = parts[4]
        else:
            label = ""
        plot_point(a_value, b_value, c_value, color, which, label, current_image)

current_image.show()

timestamp = datetime.datetime.now().strftime("%m-%d-%Y") + "-" + str(int(time.time()))
current_image.save("result-%s.png" % timestamp)
