# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from quadtree import Point, BoundingBox, QuadTree

DPI = 72  # dots (pixels) per inch

width, height = 360, 180

N = 1000
xs = np.random.rand(N) * width
ys = np.random.rand(N) * height
points = [Point(xs[i], ys[i]) for i in range(1000)]


domain = BoundingBox(Point(180, 90), width, height)
qtree = QuadTree(domain)

for point in points:
    qtree.insert(point)

print("Total points: ", len(qtree))

# #first quadrant
# qtree.insert(Point(50,50))
# qtree.insert(Point(30,30))
# qtree.insert(Point(70,70))
# qtree.insert(Point(60,60))
# qtree.insert(Point(10,10))
# qtree.insert(Point(20,20))

# #second quadrant
# qtree.insert(Point(250,70))
# qtree.insert(Point(300,70))

# #third quadrant
# qtree.insert(Point(250,150))
# qtree.insert(Point(300,150))

# #fourth quadrant
# qtree.insert(Point(30,150))
# qtree.insert(Point(10,150))


# qtree.traverse(qtree)


# draw rectangles
fig = plt.figure(
    figsize=(700 / DPI, 500 / DPI), dpi=DPI
)  # each figure has to have w=700px and h=500px
ax = plt.subplot()
ax.set_xlim(0, width)  # The right limit of x axis is 360
ax.set_ylim(0, height)  # The upper limit of y axis is 180
qtree.draw(ax)

# draw points
ax.scatter(
    [p.lon for p in points], [p.lat for p in points], s=2
)  # plot points based on longtitudes and latitudes
ax.set_xticks([])
ax.set_yticks([])


ax.invert_yaxis()
plt.tight_layout()
plt.savefig("search-quadtree.png", dpi=72)
plt.show()
