import numpy as np
import math

class Point:
    def __init__(self,lon,lat):
        self.lon = lon
        self.lat = lat


class BoundingBox:
    def __init__(self, center, width,height):
        self.center = center
        self.width = width
        self.height = height
        self.west = self.center.lon - width/2
        self.east = self.center.lon + width/2
        self.north = self.center.lat - height/2
        self.south = self.center.lat + height/2
        

    def containsPoint(self, point):
        return (self.west <= point.lon < self.east and 
                self.north <= point.lat < self.south)

    def draw(self, ax, c='k', lw=1, **kwargs):
        x1, y1 = self.west, self.north
        x2, y2 = self.east, self.south
        ax.plot([x1,x2,x2,x1,x1], [y1,y1,y2,y2,y1], c=c, lw=lw, **kwargs)
    

    
class QuadTree:
    def __init__(self,boundary:BoundingBox,cap = 2):
        self.boundary = boundary
        self.capacity = cap
        self.points = []
        self.divided = False

        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None

    def insert(self,point):
        if not self.boundary.containsPoint(point):
            return

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
        else:
            if not self.divided:
                self.divided = True
                self.divide()
                while len(self.points) != 0:
                    p = self.points.pop(0)
                    if self.nw.insert(p) or self.ne.insert(p) or self.se.insert(p) or self.sw.insert(p):
                        pass
            self.nw.insert(point)
            self.ne.insert(point)
            self.se.insert(point)
            self.sw.insert(point)
        
    def divide(self):
        new_width = self.boundary.width/2
        new_height = self.boundary.height/2

        northwest  = BoundingBox(Point(self.boundary.center.lon - new_width/2,self.boundary.center.lat - new_height/2),new_width,new_height)
        self.nw = QuadTree(northwest)

        northeast = BoundingBox(Point(self.boundary.center.lon + new_width/2,self.boundary.center.lat - new_height/2),new_width,new_height)
        self.ne = QuadTree(northeast)

        southeast = BoundingBox(Point(self.boundary.center.lon + new_width/2,self.boundary.center.lat + new_height/2),new_width,new_height)
        self.se = QuadTree(southeast)

        southwest = BoundingBox(Point(self.boundary.center.lon - new_width/2,self.boundary.center.lat + new_height/2),new_width,new_height)
        self.sw = QuadTree(southwest)


    def __len__(self):
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se) 
        
        return count
    

    def traverse(self,root):
        if root:
            self.traverse(root.nw)

            self.traverse(root.ne)

            self.traverse(root.se)

            self.traverse(root.sw)

            [print(p.lon,p.lat) for p in root.points]

    def draw(self, ax):
        self.boundary.draw(ax)

        if self.divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.se.draw(ax)
            self.sw.draw(ax)
    