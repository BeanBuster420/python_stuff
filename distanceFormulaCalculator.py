#import math, needed for sqrt
from math import *

#define points
def definePoints():
  try:
    global x1, y1, x2, y2, point1, point2
    x1 = float(input("x1: "))
    y1 = float(input("y1: "))
    x2 = float(input("x2: "))
    y2 = float(input("y2: "))
    point1 = (x1, y1)
    point2 = (x2, y2)
  except ValueError:
    print("Please input a number.")
    definePoints()

#calculate distance
def Distance(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  distance = sqrt((x2-x1)**2 + (y2-y1)**2)
  return distance

#print distance
definePoints()
print("Distance = " + str(Distance(point1, point2)))
