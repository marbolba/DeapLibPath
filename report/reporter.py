import numpy as np
import os
from tools.terrainHandler import TerrainHandler
from settings.settings import Settings


settings = Settings()


class Reporter:
    def __init__(self, problem):
        self.best = []
        self.avg = []
        self.online = 0
        self.offline = 0
        self.problem = problem

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
        values = self.problem.getPoints(best)
        values.insert(0, TerrainHandler.getWaypoints()[0])
        TerrainHandler.drawTerrainWithPoints(values, generationNr)

    def reportPopulationAverage(self, population, generationNr: int):
        adaptationAvg = np.average(
            list(map(lambda indiv: indiv.fitness.values[0], population))
        )
        self.avg.insert(generationNr, adaptationAvg)
        print(
            "Population average: \n- adaptation: {} ".format(adaptationAvg)
        )  # tmp without indiv object

    def reportResults(self, bestIndividual):
        try:
            self.reportOutputPath(bestIndividual)
            self.saveToFile("avg", self.avg)
            self.saveToFile("best", self.best)

            self.saveToFile("online", self.online)
            self.saveToFile("offline", self.offline)
            # readable report
            historyFolder = f"{TerrainHandler.getName()}{TerrainHandler.getResultId()}"
            with open(f"{historyFolder}result.txt", "w") as text_file:
                text_file.write(
                    "Generations nr: {} \n".format(settings.generationsNumber())
                )
                text_file.write(
                    "Population size: {} \n".format(settings.populationSize())
                )
                text_file.write("Best individual: {} \n".format(bestIndividual))
                text_file.write("Avg history: {} \n".format(self.avg))
                text_file.write("Best history: {} \n".format(self.best))
                text_file.write("Convergence online: {} \n".format(self.online))
                text_file.write("Convergence offline: {} \n".format(self.offline))
        except:
            print("reportResults error")

    def reportOutputPath(self, best):
        values = TerrainHandler.getWaypoints()[0] + self.problem.getPoints(best)
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
