# from tqdm import tqdm
from decimal import Decimal
import json, os
from pyproj import Proj, transform
import time

# import warnings
# warnings.filterwarnings("ignore")

WORKING_DIR = "Q:\Q_drive\semester221\ParallelComputing\Parallel_QuadTree_Partition"
DATA_FILE = "data.geojsonl.json"
BUILDINGS = 837583

WEST_POLE = Decimal('11370611.388418688')
SOUTH_POLE = Decimal('956734.3596371269')
EAST_POLE = Decimal('2679554.9980593426')
NORTH_POLE = Decimal('12185213.347147731')
GRID_LEN = 100

IMG_LEN = 512

class CoorConverter:
    def __init__(self, inProj:Proj, outProj:Proj):
        self.inProj = inProj
        self.outProj = outProj
    def __call__(self, point):
        x, y = transform(self.inProj, self.outProj, point[0], point[1])
        x, y = Decimal(str(x)), Decimal(str(y))
        return x, y




# if __name__ == '__main__':
file = open(os.path.join(WORKING_DIR, DATA_FILE), "rb")
convert = CoorConverter(inProj=Proj(init='epsg:4326'), outProj=Proj(init='epsg:3857'))
# data = {"images":[], "annotations":[]}

# for i in tqdm(range(BUILDINGS)):
for i in range(BUILDINGS):
    begin = time.time()
    with open(os.path.join(WORKING_DIR, "checkpoint.txt"), "w") as f:
        f.write(str(i))
    polygon = json.loads(file.readline())
    px, py, pgx, pgy = None, None, None, None

    # Determine which grids should be added
    grids = set()
    for point in polygon["geometry"]["coordinates"][0][0]:
        # print(point)
        x, y = convert(point)

        # Add the grids that contain the vertices
        gx, gy = int((x-WEST_POLE)/GRID_LEN), int((y-SOUTH_POLE)/GRID_LEN)
        grids.add((gx,gy))
        # print(gx,gy)

        # Add the grids that the lines pass through
        if px is not None:
            for gxx in range(min(pgx,gx)+1, max(pgx,gx)+1):
                xx = WEST_POLE + GRID_LEN*gxx
                yy = (y-py)*(xx-px)/(x-px)+py
                gyy = int((yy-SOUTH_POLE)/GRID_LEN)
                grids.add((gxx,gyy))
                # print(gxx,gyy)
            for gyy in range(min(pgy,gy)+1, max(pgy,gy)+1):
                yy = SOUTH_POLE + GRID_LEN*gyy
                xx = (x-px)*(yy-py)/(y-py)+px
                gxx = int((xx-WEST_POLE)/GRID_LEN)
                grids.add((gxx,gyy))
                # print(gxx,gyy)
        px, py, pgx, pgy = x, y, gx, gy

    # Make annotation(s) for the building
    for grid in grids:
        # print(grid)        
        with open(os.path.join(WORKING_DIR, "abstract_grids", str(grid[0])+"-"+str(grid[1])+".txt"), "a") as f:
            left = WEST_POLE + grid[0]*GRID_LEN
            right = left + GRID_LEN
            bottom = SOUTH_POLE + grid[1]*GRID_LEN
            top = bottom + GRID_LEN

            for point in polygon["geometry"]["coordinates"][0][0]:
                x, y = convert(point)
                w = (x - WEST_POLE - GRID_LEN*grid[0]) / GRID_LEN * IMG_LEN
                h = IMG_LEN - (y - SOUTH_POLE - GRID_LEN*grid[1]) / GRID_LEN * IMG_LEN

                f.write(str(w) + " " + str(h) + "\n")
            f.write("\n")
        # print()

    end = time.time()
    print(f"{i+1}: {end-begin}")
    
    # if i % 10000 == 9999:
    #     print("{} buildings proceeded".format(i+1))