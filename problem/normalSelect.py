from tools.terrainHandler import TerrainHandler
import random
from deap import creator, base, tools, algorithms


class NormalSelect:
    maxStepsNr = 6

    def setChromosome(self, toolbox):
        toolbox.register("steps_nr", random.randint, 0, self.maxStepsNr)
        toolbox.register("attr_X", random.randint, 0, TerrainHandler.getSize()[0] - 1)
        toolbox.register("attr_Y", random.randint, 0, TerrainHandler.getSize()[1] - 1)
        # inicjalizacja Individual-a przy pomocy wybranej funckji n razy
        toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            (toolbox.steps_nr, toolbox.attr_X, toolbox.attr_Y),
            n=self.maxStepsNr,
        )
        # inicjalizacja populacji - listy Individuals-ów
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.adaptationFunction)

    def getPoints(self, individual):
        stepsNr = round(individual[0])
        values = []
        for i in range(0, 3 * self.maxStepsNr, 3):
            if i < (3 * stepsNr)-1:
                values.append([round(individual[i + 1]), round(individual[i + 2])])
        return values

    def adaptationFunction(self, individual):
        costFunction = lambda x: 187.5 * (pow(1.028, x * 100))
        values = self.getPoints(individual)

        # settings
        startPoint = [0, 0]
        endPoint = [250, 100]

        distanceMax = TerrainHandler.distance(startPoint, endPoint)
        costMax = 10000

        # sprawdzenie czy sa punkty do przejscia
        if len(values) < 1:
            return (0,)

        # składowa dystansu - ostatni element do endpoint
        distanceElement = TerrainHandler.distance(
            (values[len(values) - 1][0], values[len(values) - 1][1]), endPoint
        )

        # skladowa kosztu podróży
        cost = 0
        values.insert(0, startPoint)
        for i in range(0, len(values) - 1):
            cost = cost + TerrainHandler.travelCost(values[i], values[i + 1])

        adaptationVal = 5000 * (
            distanceMax - distanceElement
        ) / distanceMax + costFunction((costMax - cost) / costMax)
        return (adaptationVal,) if adaptationVal > 0 else (0,)
