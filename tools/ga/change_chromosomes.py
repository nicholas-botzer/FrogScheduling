import random

"""
Holds methods implementing chromosome manipulation including crossover 
algorithms and selection methods.
"""
class ChangeChromosomes:

    ####### SELECTION IMPLEMENTATIONS #######
    '''
    Performs a roulette wheel selection, weighted by fitness score, and returns

    Args:
    - List of chromosomes
    Return:
    - Chromosome selected to continue living it's life
    '''
    @staticmethod #prevents python from passing self instance
    def rouletteWheelSelection(chromosomeList,sumInvFS):
        if(sumInvFS == 0):
            pick = random.randint(0, len(chromosomeList)-1)
            return chromosomeList[pick]
        else:
            pick = random.uniform(0, sumInvFS)
            current = 0
            for chromosome in chromosomeList:
                current += chromosome.inverseFitnessScore
                if current > pick:
                    return chromosome
    '''
    Performs a tournament selection amongst k chromosomes and chooses the best
    Args:
    -chromosomeList: List of chromosomes
    Return:
    -Chromosome: the winning chromosome
    '''
    @staticmethod
    def tournamentSelection(chromosomeList, k):
        tournamentChromosomes = ChangeChromosomes.selectRandom(chromosomeList,k)
        winnerChromosome = max(tournamentChromosomes, key= lambda x: x.fitness.getFitnessScore())
        return winnerChromosome

    '''
    Randomly chooses k elements from a list
    '''
    @staticmethod
    def selectRandom(chromosomeList, k):
        return [random.choice(chromosomeList) for x in range(k)]

    @staticmethod #prevents python from passing self instance
    def selectElitePopulation(chromosomeList, numberOfChromosomesToSelect):
        indexs = sorted(range(len(chromosomeList)), key=lambda i: chromosomeList[i].fitnessScore)[-numberOfChromosomesToSelect:]
        eliteChromosomes = []
        for i in range(0,numberOfChromosomesToSelect):
            eliteChromosomes.append(chromosomeList[indexs[i]])

        return eliteChromosomes

    ####### CROSSOVER IMPLEMENTATIONS #######
    '''
    Args
    - taskDict1: chrom. dictionary that maps tasks to its priority (Obj -> int)
    - taskDict2: chrom. dictionary that maps tasks to its priority (Obj -> int)
    - partition1: dictate first partition
    - partition2: dictate second partition
    Return
    - New taskDict with the crossover of taskDict1 and taskDict2
    '''
    @classmethod 
    def OX1Cross(cls, taskDict1, taskDict2, partition1=None, partition2= None):
        
    ### Verification
        if not isinstance(taskDict1, dict): raise ValueError('Dict 1 not a dict!')
        if not isinstance(taskDict2, dict): raise ValueError('Dict 2 not a dict!')
        if partition1 != None and not isinstance(partition1, int): 
            raise ValueError('Partition1 is not an int!')
        if partition2 != None and not isinstance(partition2, int):
            raise ValueError('Partition2 is not an int!') 
        if len(taskDict1) != len(taskDict2):
            raise ValueError('Dictionary sizes don\'t match!')
        if partition1 and ( partition1 < 0 or partition1 > len(taskDict1)+1 ):
            raise ValueError('Invalid partition indexes!')
        if partition2 and  ( partition2 < 0 or partition2 > len(taskDict1)+1 ):
            raise ValueError('Invalid partition indexes!')

    ### Shuffle
        numTasks = len(taskDict1)
        taskList1 = cls.dictToList(taskDict1)
        taskList2 = cls.dictToList(taskDict2)
        newTaskList1, newTaskList2 = numTasks*[None], numTasks*[None]

        #Get Random Partitions
        p1,p2 = cls.generateRandIdxList(0,numTasks,2)
        if partition1 == None:
            partition1 = p1
        if partition2 == None:
            partition2 = p2
        #Crossover
        for idx in range(partition1,partition2): #copy elems from p1 to p2-1 
            newTaskList1[idx] = taskList1[idx] # * * * | l1idx3 l1idx4 | * ...
            newTaskList2[idx] = taskList2[idx] # * * * | l2idx3 l2idx4 | * ...
        tL1idx = tL2idx = nTL1idx = nTL2idx = partition2
        nTL1done, nTL2done = False, False
        while not (nTL1done and nTL2done):
            if tL1idx >= numTasks:
                tL1idx = 0
            if tL2idx >= numTasks:
                tL2idx = 0
            if nTL1idx >= numTasks:
                nTL1idx = 0
            if nTL2idx >= numTasks:
                nTL2idx = 0
            if newTaskList1[nTL1idx]:
                nTL1done = True
            if newTaskList2[nTL2idx]:
                nTL2done = True
            if not cls.checkTaskInTList(taskList2[tL2idx],newTaskList1):
                newTaskList1[nTL1idx] = taskList2[tL2idx]
                nTL1idx += 1
            if not cls.checkTaskInTList(taskList1[tL1idx],newTaskList2):
                newTaskList2[nTL2idx] = taskList1[tL1idx]
                nTL2idx += 1
            tL1idx += 1
            tL2idx += 1 #task list indices incremented either way
        #Return dict
        newTaskDict1, newTaskDict2 = {}, {}
        for idx, (task1, task2) in enumerate(zip(newTaskList1,newTaskList2)):
            newTaskDict1[task1] = idx
            newTaskDict2[task2] = idx
        return newTaskDict1, newTaskDict2
    '''
    Args
    - taskDict1: chrom. dictionary that maps task names to its priority (str -> int)
    - taskDict2: chrom. dictionary that maps task names to its priority (str -> int)
    - numPositions: optionally indicate the number of positions to generate
    - positionList: optionally indicate a custom position list
    Return
    - New taskDict with the crossover of taskDict1 and taskDict2
    '''
    @classmethod 
    def OX2Cross(cls, taskDict1, taskDict2, numPositions=0, positionList=None):
        ## Verification and Cleanup
        # Type checking
        if not isinstance(taskDict1, dict): raise ValueError('Dict 1 not a dict!')
        if not isinstance(taskDict2, dict): raise ValueError('Dict 2 not a dict!')
        if not isinstance(numPositions, int): 
            raise ValueError('Number of positions is not an int!')
        if positionList and not isinstance(positionList, list):
            raise ValueError('Position list is not a list!')
        # Value checking
        if len(taskDict1) != len(taskDict2):
            raise ValueError('Dictionary sizes don\'t match!')
        if numPositions > len(taskDict1):
            raise ValueError('Number of positions is greater than total items!')
        if positionList: #cleanup duplicates/sort
            positionList = sorted(list(set(positionList)))
            if len(positionList) > len(taskDict1):
                raise ValueError('Number of positions is greater than total items!')
            for pos in positionList:
                if pos >= len(taskDict1):
                    raise ValueError('Given invalid position!')

        ## Get positions list and partial new task lists
        numTasks = len(taskDict1)
        taskList1 = cls.dictToList(taskDict1)
        taskList2 = cls.dictToList(taskDict2)
        newTaskList1, newTaskList2 = list(taskList1), list(taskList2) #copy
        if positionList == None or len(positionList) == 0:
            if numPositions == 0:
                positionList = cls.generateRandIdxList(0,numTasks-1,
                    random.randint(int(numTasks/5),int(4*numTasks/5)))
            else:
                positionList = cls.generateRandIdxList(0,numTasks-1,
                    numPositions)
        for pos in positionList:
            taskinP1, taskinP2 = taskList1[pos], taskList2[pos]
            t1done,t2done = False,False
            for idx, (t1, t2) in enumerate(zip(taskList1,taskList2)):
                if t2 == taskinP1:
                    newTaskList2[idx] = None
                    t2done = True
                if t1 == taskinP2:
                    newTaskList1[idx] = None
                    t1done = True
                if t1done and t2done:
                    break
        
        ## Crossover
        TL1idx, TL2idx = 0, 0
        for idx,(t1,t2) in enumerate(zip(newTaskList1,newTaskList2)):
            if t1 == None:
                while True:
                    if not cls.checkTaskInTList(taskList2[TL2idx],newTaskList1):
                        newTaskList1[idx] = taskList2[TL2idx]
                        TL2idx += 1
                        break
                    TL2idx += 1
            if t2 == None:
                while True:
                    if not cls.checkTaskInTList(taskList1[TL1idx],newTaskList2):
                        newTaskList2[idx] = taskList1[TL1idx]
                        TL1idx += 1
                        break
                    TL1idx += 1

        # Return dicts
        newTaskDict1, newTaskDict2 = {}, {}
        for idx, (task1, task2) in enumerate(zip(newTaskList1,newTaskList2)):
            newTaskDict1[task1] = idx
            newTaskDict2[task2] = idx
        return newTaskDict1, newTaskDict2

    '''
    Args
    - taskDict1: chrom. dictionary that maps task names to its priority (str -> int)
    - taskDict2: chrom. dictionary that maps task names to its priority (str -> int)
    - numPositions: optionally indicate the number of positions to generate
    - positionList: optionally indicate a custom position list
    Return
    - New taskDict with the crossover of taskDict1 and taskDict2
    '''
    @classmethod
    def POSCross(cls, taskDict1, taskDict2, numPositions=0, positionList=None):
        ## Verification and Cleanup
        # Type checking
        if not isinstance(taskDict1, dict): raise ValueError('Dict 1 not a dict!')
        if not isinstance(taskDict2, dict): raise ValueError('Dict 2 not a dict!')
        if not isinstance(numPositions, int): 
            raise ValueError('Number of positions is not an int!')
        if positionList and not isinstance(positionList, list):
            raise ValueError('Position list is not a list!')
        # Value checking
        if len(taskDict1) != len(taskDict2):
            raise ValueError('Dictionary sizes don\'t match!')
        if numPositions > len(taskDict1):
            raise ValueError('Number of positions is greater than total items!')
        if positionList: #cleanup duplicates/sort
            positionList = sorted(list(set(positionList)))
            if len(positionList) > len(taskDict1):
                raise ValueError('Number of positions is greater than total items!')
            for pos in positionList:
                if pos >= len(taskDict1):
                    raise ValueError('Given invalid position!')

        ## Get positions list and partial new task lists
        numTasks = len(taskDict1)
        taskList1 = cls.dictToList(taskDict1)
        taskList2 = cls.dictToList(taskDict2)
        newTaskList1, newTaskList2 = numTasks*[None], numTasks*[None]
        if positionList == None or len(positionList) == 0:
            if numPositions == 0:
                positionList = cls.generateRandIdxList(0,numTasks-1,
                    random.randint(int(numTasks/5),int(4*numTasks/5)))
            else:
                positionList = cls.generateRandIdxList(0,numTasks-1,
                    numPositions)
        for pos in positionList:
            taskinP1, taskinP2 = taskList1[pos], taskList2[pos]
            newTaskList1[pos] = taskinP2
            newTaskList2[pos] = taskinP1
        
        ## Crossover
        TL1idx, TL2idx = 0, 0
        for idx,(t1,t2) in enumerate(zip(newTaskList1,newTaskList2)):
            if t1 == None:
                while True:
                    if taskList1[TL1idx] not in newTaskList1:
                        newTaskList1[idx] = taskList1[TL1idx]
                        break
                    TL1idx += 1
            if t2 == None:
                while True:
                    if taskList2[TL2idx] not in newTaskList2:
                        newTaskList2[idx] = taskList2[TL2idx]
                        break
                    TL2idx += 1

        # Return dicts
        newTaskDict1, newTaskDict2 = {}, {}
        for idx, (task1, task2) in enumerate(zip(newTaskList1,newTaskList2)):
            newTaskDict1[task1] = idx
            newTaskDict2[task2] = idx
        return newTaskDict1, newTaskDict2        

    '''
    Has a top partition and positionList. The idea is take most crossover
    features from the superior parent (P1). We keep the top partition of P1
    unchanged. The positionList idxes of P1 are then transferred to the new P2.
    The rest of the elements are crossed normally.
    Args
    - taskDict1: chrom. dictionary that maps task name to its priority (str -> int)
    - taskDict2: chrom. dictionary that maps task name to its priority (str -> int)
    - p1partition: specify the partition for P1 (superior parent)
    - positionList: list of idxs to crossover in crossover region
    Return
    - New taskDicts with the crossover of taskDict1 and taskDict2
    '''
    @classmethod 
    def customCross(cls, taskDict1, taskDict2, p1partition=None, positionList=None):
        ## Verification and Cleanup
        # Type checking
        if not isinstance(taskDict1, dict): raise ValueError('Dict 1 not a dict!')
        if not isinstance(taskDict2, dict): raise ValueError('Dict 2 not a dict!')
        if p1partition is not None:
            if p1partition is not isinstance(p1partition, int): 
                raise ValueError('Number of positions is not an int!')
            if p1partition > len(taskDict1):
                raise ValueError('Number of positions is greater than total items!')
        if positionList and not isinstance(positionList, list):
            raise ValueError('Position list is not a list!')
        # Value checking
        if len(taskDict1) != len(taskDict2):
            raise ValueError('Dictionary sizes don\'t match!')
    
        if positionList: #cleanup duplicates/sort
            positionList = sorted(list(set(positionList)))
            if len(positionList) > len(taskDict1):
                raise ValueError('Number of positions is greater than total items!')
            for pos in positionList:
                if pos >= len(taskDict1):
                    raise ValueError('Given invalid position!')

        ## Generate partitions, positionList, and new task lists
        N = len(taskDict1)
        taskList1 = cls.dictToList(taskDict1)
        taskList2 = cls.dictToList(taskDict2)
        if p1partition is None:
            p1partition = random.randint(N//3,3*N//5)

        if positionList == None or len(positionList) == 0:
            positionList = cls.generateRandIdxList(0,N-1,
                    random.randint(int(N/5),int(4*N/5)))
        
        newTaskList1, newTaskList2 = N*[None],N*[None]
        for p1idx in range(p1partition):
            newTaskList1[p1idx] = taskList1[p1idx]
        for pos in positionList:
            newTaskList2[pos] = taskList1[pos]

        ## Crossover
        l2sidx, l2idx = 0, 0
        for idx in range(N):
            if idx >= p1partition:
                while True:
                    if taskList2[l2idx] not in newTaskList1:
                        newTaskList1[idx] = taskList2[l2idx]
                        break
                    l2idx += 1
            if newTaskList2[idx] is None:
                while True:
                    if taskList2[l2sidx] not in newTaskList2:
                        newTaskList2[idx] = taskList2[l2sidx]
                        break
                    l2sidx += 1
        
        ## Return new dicts
        newTaskDict1, newTaskDict2 = {}, {}
        for idx, (task1, task2) in enumerate(zip(newTaskList1,newTaskList2)):
            newTaskDict1[task1] = idx
            newTaskDict2[task2] = idx
        return newTaskDict1, newTaskDict2
    
    ######### HELPER FUNCTIONS #########
    ''' (For OX1)
    Args
    - mini: minimum value in partition range
    - maxi: maximum value in partition range
    - n: number of partitions to return
    Return
    - list of partition indexes in increasing order
    '''
    @staticmethod #prevents python from passing self instance
    def generateRandIdxList(mini,maxi,n):
        if n >= maxi-mini:
            return range(mini,maxi+1)
        partitions = []
        while len(partitions) < n:
            ri = random.randint(mini,maxi)
            if ri not in partitions:
                partitions.append(ri)
        return sorted(partitions)
    '''
    Args
    - taskDict: dictionary that maps tasks to their order index / priority
    Return
    - List of tasks where its index indicates its priority
    '''
    @staticmethod 
    def dictToList(taskDict):
        taskList = len(taskDict)*[None]
        for k,v in taskDict.items():
            if v > len(taskDict) - 1:
                raise ValueError('Dictionary value incorrect! You have'
                ' index %d in %d number of items' % (v,len(taskDict)))
            taskList[v] = k
        if None in taskList:
            raise ValueError('Dictionary mapping is incorrect!')
        return taskList
    '''
    Args
    - task: task object 
    - taskList: list to check if task object is in
    Return
    - True if in list, false otherwise
    '''
    @staticmethod 
    def checkTaskInTList(task,taskList):
        for t in taskList:
            if t == None:
                continue
            if task == t:
                return True
        return False


## ======================================================================== ##
## Testing Crossovers
## ======================================================================== ##

### Testing Helper Functions
'''
Args
- taskList: List of tasks where its index indicates its priority
'''
def printTaskList(taskList):
    for idx,task in enumerate(taskList):
        if task == None:
            s = 'None'
        else:
            s = task.name
        print('Idx: %d: TL: %s' % (idx,s))
    
'''
Emulator task object.
'''
class taskObj:
    def __init__(self,name):
        self.name = name

   
###  Tests
def testOX1():
    TD1 = {'1':0,'2':1,'3':2,'4':3,
           '5':4,'6':5,'7':6,'8':7}
    TD2 = {'2':0,'4':1,'6':2,'8':3,
            '7':4,'5':5,'3':6,'1':7}
    newTD1, newTD2 = ChangeChromosomes.OX1Cross(TD1,TD2,partition1=2,partition2=5)
    test1,test2 = [],[]
    for (k1,v1),(k2,v2) in zip(newTD1.items(),newTD2.items()):
        test1.append((k1,v1))
        test2.append((k2,v2))
    print ('Test 1:')
    for e in sorted(test1, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))
    print ('Test 2:')
    for e in sorted(test2, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))

def testOX2():
    TD1 = {'1':0,'2':1,'3':2,'4':3,
           '5':4,'6':5,'7':6,'8':7}
    TD2 = {'2':0,'4':1,'6':2,'8':3,
            '7':4,'5':5,'3':6,'1':7}
    
    newTD1, newTD2 = ChangeChromosomes.OX2Cross(TD1,TD2,positionList=[1,2,5])
    test1,test2 = [],[]
    for (k1,v1),(k2,v2) in zip(newTD1.items(),newTD2.items()):
        test1.append((k1,v1))
        test2.append((k2,v2))
        
    print ('Test 1:')
    for e in sorted(test1, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))
    print ('Test 2:')
    for e in sorted(test2, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))

def testPOS():
    TD1 = {'1':0,'2':1,'3':2,'4':3,
           '5':4,'6':5,'7':6,'8':7}
    TD2 = {'2':0,'4':1,'6':2,'8':3,
            '7':4,'5':5,'3':6,'1':7}
    
    newTD1, newTD2 = ChangeChromosomes.POSCross(TD1,TD2,positionList=[1,2,5])
    test1,test2 = [],[]
    for (k1,v1),(k2,v2) in zip(newTD1.items(),newTD2.items()):
        test1.append((k1,v1))
        test2.append((k2,v2))
        
    print ('Test 1:')
    for e in sorted(test1, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))
    print ('Test 2:')
    for e in sorted(test2, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))

def testCustom():
    TD1 = {'1':0,'2':1,'3':2,'4':3,
           '5':4,'6':5,'7':6,'8':7}
    TD2 = {'2':0,'4':1,'6':2,'8':3,
            '7':4,'5':5,'3':6,'1':7}
    
    newTD1, newTD2 = ChangeChromosomes.customCross(TD1,TD2,p1partition=3,positionList=[1,3,5,7])
    test1,test2 = [],[]
    for (k1,v1),(k2,v2) in zip(newTD1.items(),newTD2.items()):
        test1.append((k1,v1))
        test2.append((k2,v2))
        
    print ('Test 1:')
    for e in sorted(test1, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))
    print ('Test 2:')
    for e in sorted(test2, key=lambda x: x[1] ):
        print ('Task: %s, Idx/Priority: %d' % (e[0],e[1]))

if __name__ == "__main__":
    #testOX1()
    #testOX2()
    #testPOS()
    testCustom()
    

        
