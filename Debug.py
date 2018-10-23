class Debug:

### Helper String/Print Statements
    @staticmethod
    def getTaskListStr(dic, name='TaskList'):
        retStr = ''
        dicList = []
        for (k1,v1) in dic.items():
            dicList.append((k1,v1))
        retStr += ('\n - - - - - - - - - - - - - - - -\n')
        retStr += ('{}\n'.format(name))
        for e in sorted(dicList, key=lambda x: x[1]):
            retStr += ('Priority: {}, TaskInfo - {}\n'.format(e[1],
                            e[0].name))
        retStr += ('- - - - - - - - - - - - - - - -\n\n')
        return retStr

    @staticmethod
    def getTaskInfoStr(task):
        retStr = 'Task Name: {}, Deadline: {}'.format(
            task.name, task._absolute_deadline)
        return retStr
        


    