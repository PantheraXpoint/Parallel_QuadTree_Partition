# -*- coding: utf-8 -*-
import numpy as np
import math
from matplotlib.axes import Axes


class Point:
    def __init__(self, lon: float, lat: float) -> None:
        self.lon: float = lon
        self.lat: float = lat


class BoundingBox:
    def __init__(self, center: Point, width: float, height: float):
        self.center: Point = center
        self.width: float = width
        self.height: float = height
        self.west: float = self.center.lon - width / 2
        self.east: float = self.center.lon + width / 2
        self.north: float = self.center.lat - height / 2
        self.south: float = self.center.lat + height / 2

    def containsPoint(self, point: Point) -> bool:
        return (
            self.west <= point.lon < self.east and self.north <= point.lat < self.south
        )

    def draw(self, ax: Axes, c: str = "k", lw: int = 1, **kwargs) -> None:
        x1, y1 = self.west, self.north
        x2, y2 = self.east, self.south
        ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c=c, lw=lw, **kwargs)


class QuadTree:
    def __init__(self, boundary: BoundingBox, cap: int = 2) -> None:
        self.boundary: BoundingBox = boundary
        self.capacity: int = cap
        self.points: list[Point] = []
        self.divided: bool = False
        self.nw: "QuadTree" = None
        self.ne: "QuadTree" = None
        self.se: "QuadTree" = None
        self.sw: "QuadTree" = None

    def insert(self, point: Point) -> None:
        """
        Insert new point into a node in quadtree
        """
        # point not in bounding box
        if not self.boundary.containsPoint(point):
            return
        # number of points < limit and leaf node
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
        # number of points >= limit or not leaf node
        else:
            if not self.divided:
                self.divided = True
                self.divide()
                while len(self.points) != 0:
                    p = self.points.pop(0)
                    if (
                        self.nw.insert(p)
                        or self.ne.insert(p)
                        or self.se.insert(p)
                        or self.sw.insert(p)
                    ):
                        pass
            self.nw.insert(point)
            self.ne.insert(point)
            self.se.insert(point)
            self.sw.insert(point)

    def divide(self):
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2
        northwest = BoundingBox(
            Point(
                self.boundary.center.lon - new_width / 2,
                self.boundary.center.lat - new_height / 2,
            ),
            new_width,
            new_height,
        )
        self.nw = QuadTree(northwest)
        northeast = BoundingBox(
            Point(
                self.boundary.center.lon + new_width / 2,
                self.boundary.center.lat - new_height / 2,
            ),
            new_width,
            new_height,
        )
        self.ne = QuadTree(northeast)

        southeast = BoundingBox(
            Point(
                self.boundary.center.lon + new_width / 2,
                self.boundary.center.lat + new_height / 2,
            ),
            new_width,
            new_height,
        )
        self.se = QuadTree(southeast)

        southwest = BoundingBox(
            Point(
                self.boundary.center.lon - new_width / 2,
                self.boundary.center.lat + new_height / 2,
            ),
            new_width,
            new_height,
        )
        self.sw = QuadTree(southwest)

    def __len__(self) -> int:
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)
        return count

    def traverse(self, root: "QuadTree") -> None:
        if root:
            self.traverse(root.nw)
            self.traverse(root.ne)
            self.traverse(root.se)
            self.traverse(root.sw)
            [print(p.lon, p.lat) for p in root.points]

    def draw(self, ax: Axes) -> None:
        self.boundary.draw(ax)
        if self.divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.se.draw(ax)
            self.sw.draw(ax)
