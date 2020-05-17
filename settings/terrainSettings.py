import numpy as np

from tools.terrainHandler import TerrainHandler


class TerrainSetting:
    def generationsNumber(self):
        return 50

    def populationSize(self):
        return 100

    def mutationProbability(self):
        return 0.05

    def crossoverProbability(self):
        return 0.5
