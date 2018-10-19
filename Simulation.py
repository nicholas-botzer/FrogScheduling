import sys
from simso.core import Model
from simso.configuration import Configuration
from GeneticAlgorithm import GeneticAlgorithm, Chromosome, Task


def getAverageNormalizedLaxity(model):

    count = 0
    totalNormalizedLaxity = 0
    for task in model.results.tasks.values():
        for job in task.jobs:
            if(job.task.deadline and job.response_time):
                totalNormalizedLaxity += job.normalized_laxity
                count += 1

    return totalNormalizedLaxity / count
            

def main(argv):
    if len(argv) == 2:
        # Configuration load from a file.
        configuration = Configuration(argv[1])

    # Check the config before trying to run it.
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    geneticAlgorithm = GeneticAlgorithm(model.task_list)

    # geneticAlgorithm.genetic_algorithm(model)

    print("Total Migrations: " + str(model.results.total_migrations))
    print("Total Pre-emptions: " + str(model.results.total_preemptions))
    print("Total Exceeded Count: " + str(model.results.total_exceeded_count))
    print("Average Normalized Laxity: " +   "{:.3f}".format(getAverageNormalizedLaxity(model)))

main(sys.argv)