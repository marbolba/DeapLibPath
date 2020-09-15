import numpy as np

from tools.terrainHandler import TerrainHandler

TerrainHandler.setName("case2rounded")

class Settings:
    def generationsNumber(self):
        return 40

    def populationSize(self):
        return 300

    def mutationProbability(self):
        return 0.01

    def crossoverProbability(self):
        return 1
