# import pandas module
import pandas as pd
import pygame
import OutputBase
from numpy import *
from sklearn.datasets import *
from sklearn.cluster import KMeans
import ORToolsBase as VRP
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import numpy
def main(_fileName):
    fileName = _fileName
    df = pd.read_csv(fileName + ".csv")
    df.head()
    cars = 3
    routes, times = VRP.main(df, cars, df[df.Customer == 1])
    return times
    # screen = OutputBase.main(df, routes, times, cars)
    # pygame.image.save(screen, "BaseOutput/" + fileName + ".png")