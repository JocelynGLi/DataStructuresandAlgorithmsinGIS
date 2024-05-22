import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
def point_buffer(p, r):
    circle = p.buffer(r)
    circle_gdf = gpd.GeoDataFrame(circle)
    return circle_gdf
