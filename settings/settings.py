import numpy as np

from tools.terrainHandler import TerrainHandler

TerrainHandler.setName("case2")


class Settings:
    def generationsNumber(self):
        return 50

    def populationSize(self):
        return 100

    def mutationProbability(self):
        return 0.05

    def crossoverProbability(self):
        return 0.5

    # def setToolbox(self,toolbox):
