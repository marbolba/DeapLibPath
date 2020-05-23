import random
from deap import creator, base, tools, algorithms
from settings.settings import Settings
from tools.terrainHandler import TerrainHandler
from report.reporter import Reporter
from problem.normal import setChromosome

reporter = Reporter()
settings = Settings()
print("Terrain size:", TerrainHandler.getSize())

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# funkcja randomizacyjna
setChromosome(toolbox)

# inicjalizacja operatorów genetycznych
toolbox.register("mate", tools.cxOnePoint)
toolbox.register(
    "mutate", tools.mutGaussian, mu=0, sigma=10, indpb=settings.mutationProbability()
)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=settings.populationSize())


# start algorithm
NGEN = settings.generationsNumber()
for generationId in range(NGEN):
    print("Generation {}".format(generationId))
    # Select the next generation individuals
    offspring = toolbox.select(population, len(population))
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < settings.crossoverProbability():
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    # Apply mutation on the offspring
    for mutant in offspring:
        # if random.random() < settings.mutationProbability(): #all might be mutante
        toolbox.mutate(mutant)
        del mutant.fitness.values

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # The population is entirely replaced by the offspring
    population[:] = offspring

    # stats
    # fits = [ind.fitness.values[0] for ind in population]
    # maximum = max(fits)
    # mean = sum(fits) / len(fits)
    reporter.reportBestIndividual(population, generationId)
    reporter.reportPopulationAverage(population, generationId)
best = tools.selBest(population, k=1)
reporter.reportOutputPath(best[0])
