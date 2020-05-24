import numpy as np
import os
from tools.terrainHandler import TerrainHandler


class Reporter:
    def __init__(self):
        self.best = []
        self.avg = []
        self.online = 0
        self.offline = 0

    def reportBestIndividual(self, population, generationNr: int):
        sortedIndividuals = sorted(
            population, key=lambda x: x.fitness.values[0], reverse=True
        )
        self.best.insert(generationNr, sortedIndividuals[0].fitness.values[0])
        print(
            "Best individual: \n- genome: {} \n- adaptation: {} ".format(
                sortedIndividuals[0], sortedIndividuals[0].fitness.values[0],
            )
        )
        best = sortedIndividuals[0]
        values = [[0, 0]]
        for i in range(0, len(best), 2):
            values.append([best[i], best[i + 1]])
        TerrainHandler.drawTerrainWithPoints(values, generationNr)

    def reportPopulationAverage(self, population, generationNr: int):
        adaptationAvg = np.average(
            list(map(lambda indiv: indiv.fitness.values[0], population))
        )
        self.avg.insert(generationNr, adaptationAvg)
        print(
            "Population average: \n- adaptation: {} ".format(adaptationAvg)
        )  # tmp without indiv object

    def reportResults(self):
        self.saveToFile("avg", self.avg)
        self.saveToFile("best", self.best)
        self.saveToFile("online", self.online)
        self.saveToFile("offline", self.offline)

    def reportOutputPath(self, bestFenotype):
        values = [[0, 0]]
        for i in range(0, len(bestFenotype), 2):
            values.append([bestFenotype[i], bestFenotype[i + 1]])
        TerrainHandler.drawFinalRaport(values, self.best, self.avg)

    def reportConvergence(self):
        self.online = np.mean(self.avg)
        self.offline = np.mean(self.best)
        print("Online convergence: {}".format(self.online))
        print("Offline convergence: {}".format(self.offline))

    def saveToFile(self, name, value):
        historyFolder = f"{TerrainHandler.getName()}{TerrainHandler.getResultId()}"
        self.checkIfFolderExists(historyFolder)
        np.save("{}{}".format(historyFolder, name), value)

    def checkIfFolderExists(self, folderPath):
        if not (os.path.exists(folderPath)):
            # create the directory you want to save to
            os.mkdir(folderPath)
