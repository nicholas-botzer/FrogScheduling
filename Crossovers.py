import random

"""
Holds static methods implementing different crossover algorithms.
"""
class Crossovers(object):

####### HELPER FUNCTIONS #######
    '''
    Args
    - mini: minimum value in partition range
    - maxi: maximum value in partition range
    - n: number of partitions to return
    Return
    - list of partition indexes in increasing order
    '''
    @staticmethod #prevents python from passing self instance
    def generateRPartitions(mini,maxi,n):
        if n >= maxi-mini:
            return range(mini,maxi+1)
        partitions = []
        while len(partitions) < n:
            ri = random.randint(mini,maxi)
            if ri not in partitions:
                partitions.append(ri)
        return sorted(partitions)

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
    def OX1(cls, taskDict1, taskDict2, partition1=None, partition2= None):
        
    ### Verification
        if len(taskDict1) != len(taskDict2):
            raise ValueError('Dictionary sizes don\'t match!')
        if partition1 < 0 or partition2 < 0 or \
            partition1 > len(taskDict1)+1 or partition2 > len(taskDict2)+1:
            raise ValueError('Invalid partition indexes!')

    ### Shuffle
        numTasks = len(taskDict1)
        newTaskList = numTasks*[None]
        taskList1, taskList2 = numTasks*[None], numTasks*[None]
        for (k1,v1), (k2,v2) in zip(taskDict1.items(), taskDict2.items()):
            taskList1[v1], taskList2[v2] = k1, k2
        
        #Get Random Partitions
        p1,p2 = cls.generateRPartitions(0,numTasks,2)
        if partition1 == None:
            partition1 = p1
        if partition2 == None:
            partition2 = p2
        #Crossover
        for idx in range(partition1,partition2): #copy elems from p1 to p2-1 
            newTaskList[idx] = taskList1[idx]
        tL2idx = nTLidx = partition2
        while None in newTaskList:
            if tL2idx >= numTasks:
                tL2idx = 0
            if nTLidx >= numTasks:
                nTLidx = 0
            if taskList2[tL2idx] not in newTaskList:
                newTaskList[nTLidx] = taskList2[tL2idx]
                nTLidx += 1
            tL2idx += 1 #task list 2 index incremented either way
        #Return dict
        newTaskDict = {}
        for task in newTaskList:
            newTaskDict[task] = taskDict1[task]
        return newTaskDict

    @staticmethod
    def OX2(taskDict1, taskDict2, partition1=None, partition2= None):
        pass #TODO


    
        
        
