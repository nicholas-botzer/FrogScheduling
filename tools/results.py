from simso.core import Model
import os
import matplotlib.pyplot as plt
import numpy as np
import pickle

class Results():

    def __init__(self):
        self.dictOfIterationToGenerationList = {}
        self.graphDataList = []

    def insertNewGeneration(self, iteration, chromosomeGenerationList):
        self.dictOfIterationToGenerationList[iteration] = chromosomeGenerationList

    def setOptimalChromosome(self, optimalChromosome):
        self.optimalChromosome = optimalChromosome

    def createOutputFile(self, outputPath, configuration, scheduler,
                         fitness, GA=False):

        if(os.path.exists(outputPath)):
            outputFile = open(outputPath, 'a')
        
        if(not os.path.exists(outputPath)):
            outputFile = open(outputPath, 'w+')
            headerString = "Configuration,Scheduler,FitnessScore," \
                "Deadlines Exceeded,Pre-emptions,Migrations,NormalizeLaxity," \
                "Scheduler Overhead, Activate Overhead \n"
            outputFile.write(headerString)

        #Non GA techniques
        if(not GA):
            resultString = f"{configuration},{scheduler},," + \
                           fitness.getFitnessCSVStr()
        else:
            resultString =  f"{configuration},{scheduler}," + \
                            f"{self.optimalChromosome.fitnessScore}," + \
                            fitness.getFitnessCSVStr()
        
        outputFile.write(resultString)


    #Used for deubgging/testing
    def print_results(self,fitness):
        print("Total Migrations: " + str(model.results.total_migrations))
        print("Total Pre-emptions: " + str(model.results.total_preemptions))
        print("Total Exceeded Count: " + str(model.results.total_exceeded_count))


    @staticmethod
    def outputStatsForRun(organism):
        with open('organism.pkl','wb') as f:
            pickle.dump(organism, f)

        # grab metadata
        outputPath = organism.metadataDict['ResultsFile']
        configuration = organism.metadataDict['ConfigFile']
        scheduler = organism.metadataDict['SchedulerName']

        # setup output file
        outputFile = None
        if(os.path.exists(outputPath)): # if file exists, append
            outputFile = open(outputPath, 'a')
        else:
            outputFile = open(outputPath, 'w+') # if doesn't exist make new one
            headerString = "Generation,Deadlines Missed,Preemptions,Migrations,Fitness Score\n"
            outputFile.write(headerString)
        
        # write metadata to line in output file
        outputFile.write(f'{configuration},{scheduler},'
         f'TotalChrom{organism.numberOfChromosomes},MR{organism.mutationRate}\n')
        
        fsData = []
        for idx,bestChromList in enumerate(organism.optimalChromList):
            bestChrom = bestChromList[0]
            gen = idx+1
            dm = bestChrom.fitness.metricToVal['Total Exceeded Count'][idx]
            pr = bestChrom.fitness.metricToVal['Total Preemptions'][idx]
            mi = bestChrom.fitness.metricToVal['Total Migrations'][idx]
            fs = bestChrom.fitness.metricToVal['Fitness Score'][idx]
            printStr = f"{gen},{dm},{pr},{mi},{fs}\n"
            outputFile.write(printStr)
            fsData.append(fs)
        #self.graphDataList.append(fsData)
    
    @staticmethod
    def showGraph():
        legendLabels = ['100 Chromosomes, 0.5 MR',
                        '100 Chromosomes, 1.0 MR',
                        '100 Chromosomes, 1.5 MR']

        data05 = []
        data10 = []
        data15 = []
        x_gens = np.arange(20)

        plt.plot(x_gens, data05)
        plt.plot(x_gens, data10)
        plt.plot(x_gens, data15)

        plt.legend(['0.5 MR', '1.0 MR', '1.5 MR'], loc='upper left');
        plt.xlabel('Generations');
        plt.ylabel('Fitness Score');
        plt.show(block=False);
        input('press <ENTER> to continue');