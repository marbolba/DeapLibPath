from tools.terrainHandler import TerrainHandler
import random
from deap import creator, base, tools, algorithms


def setChromosome(toolbox):
    toolbox.register("attr_X", random.randint, 0, TerrainHandler.getSize()[0] - 1)
    toolbox.register("attr_Y", random.randint, 0, TerrainHandler.getSize()[1] - 1)
    # inicjalizacja Individual-a przy pomocy wybranej funckji n razy
    toolbox.register(
        "individual",
        tools.initCycle,
        creator.Individual,
        (toolbox.attr_X, toolbox.attr_Y),
        n=6,
    )
    # inicjalizacja populacji - listy Individuals-ów
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", adaptationFunction)


# funkcja evaluacji fitness
def adaptationFunction(individual):
    costFunction = lambda x: 187.5 * (pow(1.028, x * 100))
    values = []
    for i in range(0, len(individual), 2):
        values.append([individual[i], individual[i + 1]])

    # settings
    startPoint = [0, 0]
    endPoint = [260, 110]

    distanceMax = TerrainHandler.distance(startPoint, endPoint)
    costMax = 10000

    # składowa dystansu - ostatni element do endpoint
    distanceElement = TerrainHandler.distance(
        (values[len(values) - 1][0], values[len(values) - 1][1]), endPoint
    )

    # skladowa kosztu podróży
    cost = 0
    values.insert(0, [0, 0])
    for i in range(0, len(values) - 1):
        cost = cost + TerrainHandler.travelCost(values[i], values[i + 1])

    adaptationVal = 5000 * (distanceMax - distanceElement) / distanceMax + costFunction(
        (costMax - cost) / costMax
    )
    # if (costMax - cost) /costMax*100>70:
    # print("distanceElement:",(distanceMax - distanceElement) / distanceMax*100,"%, cost of travel: ", (costMax - cost) /costMax*100,"% cost function",costFunction((costMax - cost) / costMax))
    return (adaptationVal,) if adaptationVal > 0 else 0
