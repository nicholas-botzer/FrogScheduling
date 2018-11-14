import sys, logging
from simso.core import Model
from simso.configuration import Configuration
from tools.results import Results
from tools.debug import Debug
from tools.fitness import Fitness

logger = logging.getLogger('root')

"""
Runs EDF (earliest deadline first) scheduling algorithm.
"""
def main(args):
    
    # Load configuration file and check
    configPath = args.configPaths[args.currentConfigIdx]
    configuration = Configuration(configPath)
    configuration.check_all()

    # Init a model from the configuration.
    model = Model(configuration)

    # Execute the simulation.
    model.run_model()

    # Write results to csv file
    logger.log(15,"Total Migrations: " + str(model.results.total_migrations))
    logger.log(15,"Total Pre-emptions: " + str(model.results.total_preemptions))
    logger.log(15,"Total Exceeded Count: " + str(model.results.total_exceeded_count))
    logger.log(15,"Fitness Score: " + str(Fitness.getFitnessScore(
                                          model.results.total_exceeded_count,
                                          model.results.total_preemptions,
                                          model.results.total_migrations)))
    Results.outputDefResults(args,model)


if __name__ == '__main__':
    main(sys.argv)