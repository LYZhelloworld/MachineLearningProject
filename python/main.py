#!/usr/bin/python

class hmmfile:
    def __init__(self, filename):
        self.f = filename
        
    def readTraining(self):
        result = []
        fo = open(self.f, 'r')
        while True:
            line = fo.readline()
            if(line == ''):
                break
            if(line == '\n'):
                continue
            temp = line.replace('\n','').split(' ')
            result.append(tuple(temp))
            
        fo.close()
        return result
        
    def readTesting(self):
        result = []
        fo = open(self.f, 'r')
        while True:
            line = fo.readline()
            if(line == ''):
                break
            if(line == '\n'):
                continue
            result.append(line.replace('\n',''))
            
        fo.close()
        return result

def main():
    pass
    
if __name__ == '__main__':
    main()