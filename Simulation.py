import sys
from simso.core import Model
from simso.configuration import Configuration

def getAverageNormalizedLaxity(model):

    count = 0
    totalNormalizedLaxity = 0
    for task in model.results.tasks.values():
        for job in task.jobs:
            if(job.task.deadline and job.response_time):
                totalNormalizedLaxity += job.normalized_laxity
                count += 1

    return totalNormalizedLaxity / count
            

########### GA IMPLEMENTATION DETAILS BELOW ##############################

def initial_population():


def crossover():


def mutate():


def evaluate_fitness():


def genetic_algorithm(model):




########### GA IMPLEMENTATION DETAILS ABOVE ##############################

def main(argv):
    if len(argv) == 2:
        # Configuration load from a file.
        configuration = Configuration(argv[1])

    # Check the config before trying to run it.
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    # Execute the simulation.
    model.run_model()

    #Run genetic algorithm
    for x in range(0,20):
        for chromosome in geneticAlgorithm.chromosomeList:
            # Execute the simulation.
            model.scheduler.initalizePriorityQueue(chromosome.taskToPriorityDict)
            model.run_model()

            chromosome.evaluate_fitness(model)

        #Perform the selection, crossover, and mutation 
        nextChromosomeGenerationList = geneticAlgorithm.selection(8)
        childChromosomeList = geneticAlgorithm.crossover(nextChromosomeGenerationList, 4)

        # print(childChromosomeList)
        nextChromosomeGenerationList.extend(childChromosomeList)

        #mutate

        #set the GA's list of chromosomes to this new list
        geneticAlgorithm.chromosomeList = nextChromosomeGenerationList


    print("Total Migrations: " + str(model.results.total_migrations))
    print("Total Pre-emptions: " + str(model.results.total_preemptions))
    print("Total Exceeded Count: " + str(model.results.total_exceeded_count))
    print("Average Normalized Laxity: " +   "{:.3f}".format(getAverageNormalizedLaxity(model)))

if 
main(sys.argv)