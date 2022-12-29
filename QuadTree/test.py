# -*- coding: utf-8 -*-
COLLINEAR = 0
CLOCKWISE = 1
COUNTER_CLOCKWISE = 2


class Point:
    def __init__(self, lon: float, lat: float) -> None:
        self.lon: float = lon
        self.lat: float = lat


def onSegment(p: Point, q: Point, r: Point) -> bool:
    if (
        (q.lon <= max(p.lon, r.lon))
        and (q.lon >= min(p.lon, r.lon))
        and (q.lat <= max(p.lat, r.lat))
        and (q.lat >= min(p.lat, r.lat))
    ):
        return True
    return False


def orientation(p: Point, q: Point, r: Point) -> int:
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
        return CLOCKWISE
    elif val < 0:
        return COUNTER_CLOCKWISE
    else:
        return COLLINEAR


def doIntersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """
    The function that returns true if
    the line segment 'p1q1' and 'p2q2' intersect.
    """
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    # General case
    if o1 == 0 or o2 == 0 or o3 == 0 or o4 == 0:
        return False
    if (o1 != o2) and (o3 != o4):
        return True
    return False


A = Point(100, 100)
B = Point(110, 110)
C = Point(105, 106)
D = Point(109, 101)

o1 = orientation(A, B, C)
o2 = orientation(A, B, D)
o3 = orientation(C, D, A)
o4 = orientation(C, D, B)

print(o1, o2, o3, o4)
print(doIntersect(A, B, C, D))
