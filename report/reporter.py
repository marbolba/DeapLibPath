import numpy as np

from tools.terrainHandler import TerrainHandler


class Reporter:
    def reportOutputPath(self, bestFenotype):
        values = [[0, 0]]
        for i in range(0, len(bestFenotype), 2):
            values.append([bestFenotype[i], bestFenotype[i + 1]])
        TerrainHandler.drawTerrainWithPoints(values, 30)
