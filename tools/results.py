from simso.core import Model
import os

class Results():

    def __init__(self):
        self.dictOfIterationToGenerationList = {}

    def insertNewGeneration(self, iteration, chromosomeGenerationList):
        self.dictOfIterationToGenerationList[iteration] = chromosomeGenerationList

    def setOptimalChromosome(self, optimalChromosome):
        self.optimalChromosome = optimalChromosome

    def createOutputFile(self, outputPath, configuration, scheduler,model,GA=False):

        if(os.path.exists(outputPath)):
            outputFile = open(outputPath, 'a')
        
        if(not os.path.exists(outputPath)):
            outputFile = open(outputPath, 'w+')
            headerString = "Configuration,Scheduler,FitnessScore,Deadlines Exceeded,Pre-emptions,Migrations,NormalizeLaxity \n"
            outputFile.write(headerString)

        res = model.results
        normalizedLaxity = self.getAverageNormalizedLaxity(model)
        #Non GA techniques
        if(not GA):
            resultString = f"{configuration},{scheduler},,{res.total_exceeded_count},{res.total_preemptions},{res.total_migrations},{normalizedLaxity} \n"
        else:
            resultString = f"{configuration},{scheduler},{self.optimalChromosome.fitnessScore},{res.total_exceeded_count},{res.total_preemptions},{res.total_migrations},{normalizedLaxity} \n"
        
        outputFile.write(resultString)


    def getAverageNormalizedLaxity(self, model):
        count = 0
        totalNormalizedLaxity = 0
        for task in model.results.tasks.values():
            for job in task.jobs:
                if(job.task.deadline and job.response_time):
                    totalNormalizedLaxity += job.normalized_laxity
                    count += 1

        return totalNormalizedLaxity / count

    #Used for deubgging/testing
    def print_results(self,model):
        print("Total Migrations: " + str(model.results.total_migrations))
        print("Total Pre-emptions: " + str(model.results.total_preemptions))
        print("Total Exceeded Count: " + str(model.results.total_exceeded_count))