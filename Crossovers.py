import random

"""
Holds static methods implementing different crossover algorithms.
"""
class Crossovers(object):

####### HELPER FUNCTIONS #######
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
            if task.name == t.name:
                return True
        return False


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
        for idx, taskTuple in enumerate(zip(newTaskList1,newTaskList2)):
            task1, task2 = taskTuple
            newTaskDict1[task1] = idx
            newTaskDict2[task2] = idx
        return newTaskDict1, newTaskDict2
    '''
    Args
    - taskDict1: chrom. dictionary that maps tasks to its priority (Obj -> int)
    - taskDict2: chrom. dictionary that maps tasks to its priority (Obj -> int)
    - numPositions: optionally indicate the number of positions to generate
    - positionList: optionally indicate a custom position list
    Return
    - New taskDict with the crossover of taskDict1 and taskDict2
    '''
    @classmethod 
    def OX2(cls, taskDict1, taskDict2, numPositions=0, positionList=None):
        ## Verification
        if len(taskDict1) != len(taskDict2):
            raise ValueError('Dictionary sizes don\'t match!')
        positionList = sorted(list(set(positionList))) #cleanup duplicates/sort
        if numPositions > len(taskDict1) or len(positionList) > len(taskDict1):
            raise ValueError('Number of positions is greater than total items!')
        for pos in positionList:
            if pos >= len(taskDict1):
                raise ValueError('Given invalid position!')

        ## Get positions list
        #cls.generateRandIdxList(0,numTasks,2)



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
        print 'Idx: %d: TL: %s' % (idx,s)
    
'''
Emulator task object.
'''
class taskObj:
    def __init__(self,name):
        self.name = name

###  Tests
def testOX1():
    TD1 = {taskObj('1'):0,taskObj('2'):1,taskObj('3'):2,taskObj('4'):3,
            taskObj('5'):4,taskObj('6'):5,taskObj('7'):6,taskObj('8'):7}
    TD2 = {taskObj('2'):0,taskObj('4'):1,taskObj('6'):2,taskObj('8'):3,
            taskObj('7'):4,taskObj('5'):5,taskObj('3'):6,taskObj('1'):7,taskObj('10'):70}
    newTD1, newTD2 = Crossovers.OX1(TD1,TD2,partition1=2,partition2=5)
    print 'Test 1:'
    for k,v in newTD1.items():
        print 'Task: %s, Idx/Priority: %d' % (k.name,v)
    print 'Test 2:'
    for k,v in newTD2.items():
        print 'Task: %s, Idx/Priority: %d' % (k.name,v)

testOX1()

    

        
