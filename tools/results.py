from simso.core import Model
from tools.fitness import Fitness
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

    # Called by default runs.
    @staticmethod
    def outputDefResults(args,model):
        
        ### Grab Metadata
        outputPath = args.resultsFilePath
        configuration = args.configFileNames[args.currentConfigIdx]
        scheduler = args.schedNames[args.currentSchedIdx]

        if(os.path.exists(outputPath)):
            outputFile = open(outputPath, 'a')
        if(not os.path.exists(outputPath)):
            headerString = ('Configuration,'
                            'Scheduler,'
                            'Deadlines Exceeded,'
                            'Pre-emptions,'
                            'Migrations,'
                            'NormalizeLaxity,'
                            'FitnessScore,'
                            'Scheduler Overhead,' 
                            'Activate Overhead\n')
            outputFile = open(outputPath, 'w+')
            outputFile.write(headerString)

        de = model.results.total_exceeded_count
        pre = model.results.total_preemptions
        mig = model.results.total_migrations
        nl = Fitness.getAverageNormalizedLaxity(model)
        fs = Fitness.getFitnessScoreStatic(de,pre,mig)
        so = model.results.scheduler.schedule_overhead
        ao = model.results.scheduler.activate_overhead

        resultString = (f'{configuration},{scheduler}'
                         f'{de},{pre},{mig},{nl},{fs},{so},{ao}\n')
        outputFile.write(resultString)


    #Used for deubgging/testing
    def print_results(self,fitness):
        print("Total Migrations: " + str(model.results.total_migrations))
        print("Total Pre-emptions: " + str(model.results.total_preemptions))
        print("Total Exceeded Count: " + str(model.results.total_exceeded_count))

    # Called by GA runs
    @staticmethod
    def outputStatsForRun(organism,args):
        with open(args.pklFilePath,'wb') as f:
            pickle.dump(organism, f)

        # grab metadata
        outputPath = organism.metadataDict['ResultsFilePath']
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
         f'TotalChrom{organism.numberOfChromosomes},MR{organism.mutationRate},'
         f'{args.selection},{args.crossover},{args.cke}\n')
        
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