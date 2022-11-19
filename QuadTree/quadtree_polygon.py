# -*- coding: utf-8 -*-
from matplotlib.axes import Axes
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import gridspec


class Point:
    def __init__(self, lon: float, lat: float) -> None:
        self.lon: float = lon
        self.lat: float = lat


class Polygon:
    COLLINEAR = 0
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = 2

    def __init__(self, points: list[Point]) -> None:
        """
        A polygon is instantiated using:
        points: list of points
        """
        self.points: list[Point] = points
        self.maxLon = float("-inf")

        for point in points:
            if self.maxLon < point.lon:
                self.maxLon = point.lon

    def __onSegment(self, p: Point, q: Point, r: Point) -> bool:
        if (
            (q.lon <= max(p.lon, r.lon))
            and (q.lon >= min(p.lon, r.lon))
            and (q.lat <= max(p.lat, r.lat))
            and (q.lat >= min(p.lat, r.lat))
        ):
            return True
        return False

    def __orientation(self, p: Point, q: Point, r: Point) -> int:
        """
        Find the orientation of an ordered triplet (p,q,r)
        function returns the following values:
        0 : Collinear points
        1 : Clockwise points
        2 : Counterclockwise

        See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        for details of below formula.
        """
        val = (float(q.lat - p.lat) * (r.lon - q.lon)) - (
            float(q.lon - p.lon) * (r.lat - q.lat)
        )
        if val > 0:
            return self.CLOCKWISE
        elif val < 0:
            return self.COUNTER_CLOCKWISE
        else:
            return self.COLLINEAR

    def __doIntersect(self, p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
        """
        The function that returns true if
        the line segment 'p1q1' and 'p2q2' intersect.
        """
        # Find the 4 orientations required for
        # the general and special cases
        o1 = self.__orientation(p1, q1, p2)
        o2 = self.__orientation(p1, q1, q2)
        o3 = self.__orientation(p2, q2, p1)
        o4 = self.__orientation(p2, q2, q1)
        # General case
        if (o1 == 0 or o2 == 0 or o3 == 0 or o4 == 0):
            return False
        if (o1 != o2) and (o3 != o4):
            return True
        # Special Cases
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        # if (o1 == 0) and self.__onSegment(p1, p2, q1):
        #     return True
        # # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        # if (o2 == 0) and self.__onSegment(p1, q2, q1):
        #     return True
        # # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        # if (o3 == 0) and self.__onSegment(p2, p1, q2):
        #     return True
        # # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        # if (o4 == 0) and self.__onSegment(p2, q1, q2):
        #     return True
        # If none of the cases
        return False

    def __doIntersectv2(self, p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
        """
        The function that returns true if
        the line segment 'p1q1' and 'p2q2' intersect.
        """
        # Find the 4 orientations required for
        # the general and special cases
        o1 = self.__orientation(p1, q1, p2)
        o2 = self.__orientation(p1, q1, q2)
        o3 = self.__orientation(p2, q2, p1)
        o4 = self.__orientation(p2, q2, q1)
        # General case
        if (o1 != o2) and (o3 != o4):
            return True
        # Special Cases
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if (o1 == 0) and self.__onSegment(p1, p2, q1):
            return True
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if (o2 == 0) and self.__onSegment(p1, q2, q1):
            return True
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if (o3 == 0) and self.__onSegment(p2, p1, q2):
            return True
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if (o4 == 0) and self.__onSegment(p2, q1, q2):
            return True
        # If none of the cases
        return False

    def intersectLine(self, p0: Point, p1: Point) -> bool:
        """
        Returns true if the line segment intersects with
        the edges of self
        p0: starting point of line segment
        p1: ending point of line segment
        """
        for idx in range(len(self.points)):
            e0 = self.points[idx]
            e1 = self.points[(idx + 1) % len(self.points)]
            if self.__doIntersect(p0, p1, e0, e1):
                return True
        return False

    def numIntersect(self, p0: Point, p1: Point) -> int:
        """
        Calculate the number of times a line segment intersects with
        the edges of self
        p0: starting point of line segment
        p1: ending point of line segment
        """
        cnt = 0
        for i in range(len(self.points)):
            e0 = self.points[i]
            e1 = self.points[(i + 1) % len(self.points)]
            if self.__doIntersectv2(p0, p1, e0, e1):
                cnt += 1
        return cnt

    def containsPoint(self, p: Point) -> bool:
        right = self.numIntersect(p, Point(300, p.lat))
        left = self.numIntersect(Point(-1, p.lat),p)
        up = self.numIntersect(p, Point(p.lon, 180))
        down = self.numIntersect(p, Point(p.lon, -1))
        return right and left and up and down


class BoundingBox:
    PARTIAL_OVERLAP = 0
    INSIDE = 1
    OUTSIDE = 2

    def __init__(self, center: Point, width: float, height: float):
        self.center: Point = center
        self.width: float = width
        self.height: float = height
        self.west: float = self.center.lon - width / 2
        self.east: float = self.center.lon + width / 2
        self.north: float = self.center.lat - height / 2
        self.south: float = self.center.lat + height / 2

    def containsPoint(self, point: Point) -> bool:
        """
        Returns true if the bounding box contains point
        """
        return (point is not None) and (
            self.west < point.lon < self.east and self.north < point.lat < self.south
        )

    def positionVsPolygon(self, polygon: Polygon) -> int:
        """
        Returns the relative position of the bounding box with respect to polygon
        """
        # bounding box intersects partially with the polygon
        if (
            any([self.containsPoint(point) for point in polygon.points])
            or polygon.intersectLine(
                Point(self.east, self.north), Point(self.west, self.north)
            )
            or polygon.intersectLine(
                Point(self.west, self.north), Point(self.west, self.south)
            )
            or polygon.intersectLine(
                Point(self.west, self.south), Point(self.east, self.south)
            )
            or polygon.intersectLine(
                Point(self.east, self.south), Point(self.east, self.north)
            )
        ):
            return self.PARTIAL_OVERLAP
        else:
            if polygon.containsPoint(self.center):
                return self.INSIDE
            else:
                return self.OUTSIDE

    def draw(self, ax: Axes) -> None:
        box = patches.Rectangle(
            (self.west, self.north),
            self.width,
            self.height,
            linewidth=0.1,
            edgecolor="r",
            facecolor="r",
        )
        ax.add_patch(box)


class PolygonQuadTree:
    DIVISION_UNIT = 1  # smallest width of a node

    def __init__(self, boundBox: BoundingBox) -> None:
        self.boundBox: BoundingBox = boundBox
        self.isColored: bool = False
        self.children: list["PolygonQuadTree"] = None

    def insertPolygon(self, polygon: Polygon) -> None:
        """
        Insert new polygon into the root node of self
        """
        position = self.boundBox.positionVsPolygon(polygon)
        if position == self.boundBox.PARTIAL_OVERLAP:
            if self.boundBox.width > self.DIVISION_UNIT:
                self.__divide(polygon)
            else:
                # overdrawn
                self.isColored = True
        else:
            self.isColored = position == self.boundBox.INSIDE

    def __divide(self, polygon: Polygon):
        """ """
        newWidth = self.boundBox.width / 2
        newHeight = self.boundBox.height / 2
        self.children = []

        for i in range(4):
            child = PolygonQuadTree(
                BoundingBox(
                    Point(
                        self.boundBox.center.lon + pow(-1, i & 1) * newWidth/2,
                        self.boundBox.center.lat + pow(-1, i >> 1) * newHeight/2,
                    ),
                    newWidth,
                    newHeight,
                )
            )
            child.insertPolygon(polygon)
            self.children.append(child)
            

    def draw(self, ax: Axes) -> None:
        if self.isColored:
            self.boundBox.draw(ax)
        if self.children is not None:
            for child in self.children:
                child.draw(ax)

DPI = 72  # dots (pixels) per inch

width, height = 360, 180

#test01
# A=Point(20,40)
# B=Point(39,96)
# C=Point(71,68)
# D=Point(99,115)
# E=Point(120,60)
# F=Point(75,53)
# G=Point(115,24)
# H=Point(7,4)
# I=Point(40,20)
# J=Point(3,4)
# K=Point(7,32)

#test02
A=Point(11,20)
B=Point(23,47)
C=Point(7,38)
D=Point(40,111)
E=Point(33,79)
F=Point(80,120)
G=Point(120,80)
H=Point(40,60)
I=Point(62,53)
J=Point(119,52)
K=Point(120,20)
L=Point(79,8)
M=Point(37,49)



listP = []
listP.append(A)
listP.append(B)
listP.append(C)
listP.append(D)
listP.append(E)
listP.append(F)
listP.append(G)
listP.append(H)
listP.append(I)
listP.append(J)
listP.append(K)
listP.append(L)
listP.append(M)

center = Point(64,64)
testBB = BoundingBox(center,128,128)
testQT = PolygonQuadTree(testBB)
testPoly = Polygon(listP)

testQT.insertPolygon(testPoly)


# draw rectangles
fig = plt.figure(
    figsize=(700 / DPI, 500 / DPI), dpi=DPI
)  # each figure has to have w=700px and h=500px
ax = plt.subplot()
ax.set_xlim(0, width)  # The right limit of x axis is 360
ax.set_ylim(0, height)  # The upper limit of y axis is 180
testQT.draw(ax)


plt.tight_layout()
plt.savefig("search-quadtree.png", dpi=72)
plt.show()
