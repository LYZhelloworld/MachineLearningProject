#!/usr/bin/python

NPC = r'.\NPC'
NPC_DEV_IN = NPC + r'\dev.in'
NPC_DEV_OUT = NPC + r'\dev.out'
NPC_TRAIN = NPC + r'\train'
POS = r'.\POS'
POS_DEV_IN = POS + r'\dev.in'
POS_DEV_OUT = POS + r'\dev.out'
POS_TRAIN = POS + r'\train'

RESULT = r'.\result'
RESULT_POS = RESULT + r'\POS'
RESULT_POS_P2 = RESULT_POS + r'\dev.p2.out'
RESULT_NPC = RESULT + r'\NPC'
RESULT_NPC_P2 = RESULT_NPC + r'\dev.p2.out'

# This function can be used to read both training data and parsed data
def readTraining(filename):
    result = []
    fo = open(filename, 'r')
    while True:
        line = fo.readline()
        if(line == ''):
            break
        if(line == '\n'):
            result.append((None, None))
            continue
        temp = line.replace('\n','').split(' ')
        result.append(tuple(temp))
        
    fo.close()
    return result
    
def readTesting(filename):
    result = []
    fo = open(filename, 'r')
    while True:
        line = fo.readline()
        if(line == ''):
            break
        if(line == '\n'):
            result.append(None)
            continue
        result.append(line.replace('\n',''))
        
    fo.close()
    return result

def writeResult(filename, result):
    fo = open(filename, 'w')
    for item in result:
        if item == (None, None):
            fo.write('\n')
            continue
        fo.write(item[0])
        fo.write(' ')
        fo.write(item[1])
        fo.write('\n')
    fo.close()
    
def calculate_part2(filename_train, filename_test):
    emission = {}
    train_data = {}
    train = readTraining(filename_train)
    
    # Count tags and words
    for item in train:
        if item == (None, None):
            continue
        if not train_data.has_key(item[1]):
            train_data[item[1]] = {}
        if not train_data[item[1]].has_key(item[0]):
            train_data[item[1]][item[0]] = 0
        train_data[item[1]][item[0]] += 1
        
    # Calculate emission probability
    for tagname, tag in train_data.iteritems():
        count_y = sum(tag.values())
        for word, frequency in tag.iteritems():
            emission[(tagname, word)] = float(frequency) / count_y
            
    # Start parsing
    test = readTesting(filename_test)
    result = []
    for w in test:
        if w == None:
            result.append((None, None))
            continue
        prob = {}
        for key in emission:
            if(key[1] == w):
                prob[key[0]] = key[1]
        if prob == {}: # New word
            for tagname, tag in train_data.iteritems():
                prob[tagname] = 1.0 / (sum(tag.values()) + 1)
        result.append((w, max(prob, key = prob.get)))
        
    return result
    
def accuracy(result, correct):
    count = 0
    correct_count = 0
    
    for i in range(len(result)):
        if(result[i][0] != correct[i][0]):
            print 'Inconsistency detected.'
            return None
        count += 1
        if(result[i][1] == correct[i][1]):
            correct_count += 1
    
    return float(correct_count) / count
    
def part2():
    result = calculate_part2(POS_TRAIN, POS_DEV_IN)
    writeResult(RESULT_POS_P2, result)
    correct = readTraining(POS_DEV_OUT)
    acc = accuracy(result, correct)
    if acc != None:
        print '[Part 2] POS Accuracy:', acc
        
    result = calculate_part2(NPC_TRAIN, NPC_DEV_IN)
    writeResult(RESULT_NPC_P2, result)
    correct = readTraining(NPC_DEV_OUT)
    acc = accuracy(result, correct)
    if acc != None:
        print '[Part 2] NPC Accuracy:', acc
    
if __name__ == '__main__':
    part2()