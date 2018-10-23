from simso.core import Model

class Results():

    def __init__(self, model):
        self.model = model


    def print_results(self):
        print("Total Migrations: " + str(self.model.results.total_migrations))
        print("Total Pre-emptions: " + str(self.model.results.total_preemptions))
        print("Total Exceeded Count: " + str(self.model.results.total_exceeded_count))