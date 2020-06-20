import os
import math
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime
import os


class TerrainHandler:
    folderPath = ""
    resultId = "results{}/".format(datetime.now().strftime("%d-%b-%Y_%H%M%S"))
    terrain = []
    accessibility = []
    waypoints = []
    domain = ()

    @staticmethod
    def readFromFile(fileName):
        return np.load(fileName)

    @staticmethod
    def checkIfFolderExists(folderPath):
        if not (os.path.exists(folderPath)):
            # create the directory you want to save to
            os.mkdir(folderPath)

    @staticmethod
    def slope(point1, point2):
        a = (point2[1] - point1[1]) / (point2[0] - point1[0])
        b = point1[1] - a * point1[0]  # b = y - ax
        return a, b

    @staticmethod
    def distance(point1, point2):
        return distance.euclidean(point1, point2)

    @staticmethod
    def getSize():
        return TerrainHandler.domain[1], TerrainHandler.domain[0]

    @staticmethod
    def getWaypoints():
        return TerrainHandler.waypoints[0], TerrainHandler.waypoints[1]

    @staticmethod
    def getPointHeight(x, y):
        size = TerrainHandler.getSize()
        if x < size[0] and x >= 0 and y < size[1] and y >= 0:
            return TerrainHandler.terrain[y][x]
        else:
            return 0

    @staticmethod
    def getPointAccessibility(x, y):
        return TerrainHandler.accessibility[y][x]

    @staticmethod
    def travelCost(point1, point2):
        oneUpCost = 30  # cost of traveling one point height

        size = TerrainHandler.getSize()
        fi = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
        maxR = TerrainHandler.distance(point1, point2)
        sinFi = np.sin(fi)
        cosFi = np.cos(fi)

        stepLength = 1
        cost = 0
        previousHeight = TerrainHandler.getPointHeight(
            round(point1[0]), round(point1[1])
        )
        for r in range(1, int(round(maxR) + 1), stepLength):
            x, y = int(round(point1[0] + r * cosFi)), int(round(point1[1] + r * sinFi))
            if x < size[0] and x >= 0 and y < size[1] and y >= 0:
                # print(":",x,y,TerrainHandler.getPointHeight(x,y),previousHeight,"=",stepLength + abs(TerrainHandler.getPointHeight(x,y)-previousHeight)*5)
                cost = cost + (
                    stepLength
                    + abs(TerrainHandler.getPointHeight(x, y) - previousHeight)
                    * oneUpCost
                ) * TerrainHandler.getPointAccessibility(x, y)
                previousHeight = TerrainHandler.getPointHeight(x, y)
            else:
                cost = cost + 100  # punish
        # print("cost",point1,point2," = ",cost)
        return cost

    @staticmethod
    def getNextStepPosition(position, fi, r):
        sinFi = np.sin(fi)
        cosFi = np.cos(fi)
        x, y = int(round(position[0] + r * cosFi)), int(round(position[1] + r * sinFi))
        return (x, y)

    @staticmethod
    def setName(folderName):
        TerrainHandler.folderPath = "assets/terrains/{}/".format(folderName)
        TerrainHandler.fetchAssets(folderName)

    @staticmethod
    def getName():
        return TerrainHandler.folderPath

    @staticmethod
    def getResultId():
        return TerrainHandler.resultId

    @staticmethod
    def fetchAssets(folderName):
        TerrainHandler.terrain = TerrainHandler.readFromFile(
            "assets/terrains/{}/terrain.npy".format(folderName)
        )
        TerrainHandler.domain = TerrainHandler.readFromFile(
            "assets/terrains/{}/terrain-size.npy".format(folderName)
        )
        TerrainHandler.waypoints = TerrainHandler.readFromFile(
            "assets/terrains/{}/terrain-waypoints.npy".format(folderName)
        )
        try:
            TerrainHandler.accessibility = TerrainHandler.readFromFile(
                "assets/terrains/{}/accessibility.npy".format(folderName)
            )
        except IOError:
            print("WARN: No accessibility mesh")
            TerrainHandler.accessibility = np.ones(TerrainHandler.domain)

    @staticmethod
    def drawTerrainWithPoints(points: [int], generationNr: int):
        historyFolder = f"{TerrainHandler.folderPath}{TerrainHandler.resultId}"
        # terrain + accessibility
        terrain = TerrainHandler.terrain * TerrainHandler.accessibility

        # terrain
        plt.figure(figsize=(8, 4))
        plt.subplots_adjust(
            top=0.95, bottom=0.07, left=0.05, right=0.5, hspace=0.27, wspace=0.05
        )
        plt.matshow(terrain, fignum=1)
        plt.plot(
            TerrainHandler.getWaypoints()[0][0],
            TerrainHandler.getWaypoints()[0][1],
            "o",
            color="green",
        )
        plt.plot(
            TerrainHandler.getWaypoints()[1][0],
            TerrainHandler.getWaypoints()[1][1],
            "o",
            color="red",
        )
        cbar = plt.colorbar()
        cbar.set_label("Z", rotation=270)

        # route
        items = np.transpose([list(item) for item in points])
        plt.plot(items[0], items[1], "xr-")
        plt.title("Trasa")
        plt.xlabel("X")
        plt.ylabel("Y")

        TerrainHandler.checkIfFolderExists(historyFolder)
        plt.savefig(f"{historyFolder}generation-{generationNr}.png")
        plt.show(block=False)
        plt.pause(0.05)
        plt.close()

    @staticmethod
    def drawFinalRaport(bestFenotype: [int], best: [int], avg: [int]):
        historyFolder = f"{TerrainHandler.folderPath}{TerrainHandler.resultId}"
        gs = gridspec.GridSpec(2, 4)
        # terrain + accessibility
        terrain = TerrainHandler.terrain * TerrainHandler.accessibility

        # terrain
        plt.figure(figsize=(17, 7))
        plt.subplot(gs[:, :3])
        plt.matshow(terrain, fignum=0)
        plt.plot(
            TerrainHandler.getWaypoints()[0][0],
            TerrainHandler.getWaypoints()[0][1],
            "o",
            color="green",
        )
        plt.plot(
            TerrainHandler.getWaypoints()[1][0],
            TerrainHandler.getWaypoints()[1][1],
            "o",
            color="red",
        )
        cbar = plt.colorbar()
        cbar.set_label("Z", rotation=270)

        # route
        items = np.transpose([list(item) for item in bestFenotype])
        plt.plot(items[0], items[1], "xr-")
        plt.title("Trasa")
        plt.xlabel("X")
        plt.ylabel("Y")

        # best
        plt.subplot(gs[0, 3])
        plt.plot(range(0, len(best)), best)
        plt.title("Dostosowanie najlepszego osobnika")
        plt.ylabel("Dostosowanie")
        plt.xlabel("PokolenieDostosowanie")

        # avg
        plt.subplot(gs[1, 3])
        plt.plot(range(0, len(avg)), avg)
        plt.title("Dostosowanie przeciętnego osobnika")
        plt.ylabel("Dostosowanie")
        plt.xlabel("PokolenieDostosowanie")

        TerrainHandler.checkIfFolderExists(historyFolder)
        plt.subplots_adjust(
            top=0.95, bottom=0.07, left=0.05, right=0.95, hspace=0.27, wspace=0.05
        )
        plt.savefig("{}result.png".format(historyFolder))
        plt.show()
