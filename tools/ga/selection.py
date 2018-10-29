import random

"""
Holds static methods implementing different selection algorithms.
"""
class Selection(object):

    '''
    Performs a roulette wheel selection, weighted by fitness score, and returns
    
    Args:
    - List of chromosomes
    Return:
    - Chromosome selected to continue living it's life
    '''
    @staticmethod #prevents python from passing self instance
    def rouletteWheelSelection(chromosomeList):

        maximum = sum(chromosome.fitnessScore for chromosome in chromosomeList)


        if(maximum == 0):
            pick = random.randint(0, len(chromosomeList)-1)
            return chromosomeList[pick]
        else:
            pick = random.uniform(0, maximum)
            current = 0
            for chromosome in chromosomeList:
                current += chromosome.fitnessScore
                if current > pick:
                    return chromosome

    @staticmethod #prevents python from passing self instance
    def selectElitePopulation(chromosomeList, numberOfChromosomesToSelect):
        indexs = sorted(range(len(chromosomeList)), key=lambda i: chromosomeList[i].fitnessScore)[-numberOfChromosomesToSelect:]
        eliteChromosomes = []
        for i in range(0,numberOfChromosomesToSelect):
            eliteChromosomes.append(chromosomeList[indexs[i]])

        return eliteChromosomes