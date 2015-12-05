#!/usr/bin/python
from heapq import nlargest

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
RESULT_POS_P3 = RESULT_POS + r'\dev.p3.out'
RESULT_POS_P4 = RESULT_POS + r'\dev.p4.out'
RESULT_NPC = RESULT + r'\NPC'
RESULT_NPC_P2 = RESULT_NPC + r'\dev.p2.out'
RESULT_NPC_P3 = RESULT_NPC + r'\dev.p3.out'
RESULT_NPC_P4 = RESULT_NPC + r'\dev.p4.out'

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
            emission[(tagname, word)] = float(frequency) / (count_y + 1)

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
                prob[key[0]] = emission[key]
        if prob == {}: # New word
            for tagname, tag in train_data.iteritems():
                prob[tagname] = 1.0 / (sum(tag.values()) + 1)
                #prob[tagname] = 1.0 / (len(train_data) + 1)
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

def calculate_part3(filename_train, filename_test):
    train = readTraining(filename_train)

    # Build transition probability
    # Count every tags and transitions
    count = {'_START': 0, '_STOP': 0}
    trans = {}
    for i in range(len(train)):
        if i == 0:
            count['_START'] += 1
        elif train[i - 1] == (None, None):
            count['_START'] += 1

        if train[i] == (None, None): # End of sentence
            count['_STOP'] += 1
            if not trans.has_key(train[i - 1][1]):
                trans[train[i - 1][1]] = {}
            if not trans[train[i - 1][1]].has_key('_STOP'):
                trans[train[i - 1][1]]['_STOP'] = 0
            trans[train[i - 1][1]]['_STOP'] += 1
        else: # A word
            if not count.has_key(train[i][1]):
                count[train[i][1]] = 0
            count[train[i][1]] += 1
            if i == 0: # Start
                if not trans.has_key('_START'):
                    trans['_START'] = {}
                if not trans['_START'].has_key(train[i][1]):
                    trans['_START'][train[i][1]] = 0
                trans['_START'][train[i][1]] += 1
            if train[i - 1] == (None, None): # Start
                if not trans.has_key('_START'):
                    trans['_START'] = {}
                if not trans['_START'].has_key(train[i][1]):
                    trans['_START'][train[i][1]] = 0
                trans['_START'][train[i][1]] += 1
            else: # In the middle of sentence
                if not trans.has_key(train[i - 1][1]):
                    trans[train[i - 1][1]] = {}
                if not trans[train[i - 1][1]].has_key(train[i][1]):
                    trans[train[i - 1][1]][train[i][1]] = 0
                trans[train[i - 1][1]][train[i][1]] += 1

    # Calculate transition probability
    transition = {}
    for key1 in count:
        if not transition.has_key(key1):
            transition[key1] = {}
        for key2 in count:
            if not transition[key1].has_key(key2):
                transition[key1][key2] = 0.0
            if trans.has_key(key1):
                if trans[key1].has_key(key2):
                    transition[key1][key2] = float(trans[key1][key2]) / count[key1]

    # Count emissions
    em = {}
    for item in train:
        if item == (None, None):
            continue
        if not em.has_key(item[1]):
            em[item[1]] = {}
        if not em[item[1]].has_key(item[0]):
            em[item[1]][item[0]] = 0
        em[item[1]][item[0]] += 1

    # Calculate emission probability
    emission = {}
    for tag in em:
        if not emission.has_key(tag):
            emission[tag] = {}
        for word in em[tag]:
            if not emission[tag].has_key(word):
                emission[tag][word] = 0.0
            emission[tag][word] = float(em[tag][word]) / (count[tag] + 1)

    # Viterbi
    test = readTesting(filename_test)
    result = []
    sentence = []
    for w in test:
        if(w != None):
            sentence.append(w)
        else: # End of a sentence
            # Initialize viterbi
            viterbi = [{} for i in range(len(sentence) + 1)]
            for k in viterbi:
                for tag in count:
                    if count == '_STOP': # Skip STOP tag
                        continue
                    k[tag] = (0.0, None)
            viterbi[0]['_START'] = (1.0, None)

            n = len(viterbi) - 1
            for k in range(1, n + 1):
                for tag in viterbi[k]:
                    if tag == '_START':
                        viterbi[k][tag] = (0.0, None)
                        continue
                    values = []
                    for prev_tag in viterbi[k-1]:
                        temp = 1.0
                        temp *= viterbi[k-1][prev_tag][0] # pi(k-1, u)
                        if transition.has_key(prev_tag): # * a(u, v)
                            if transition[prev_tag].has_key(tag):
                                temp *= transition[prev_tag][tag]
                            else:
                                temp *= 0.0
                        else:
                            temp *= 0.0
                        if emission.has_key(tag): # * b(v, x_k)
                            if emission[tag].has_key(sentence[k - 1]):
                                temp *= emission[tag][sentence[k - 1]]
                            else:
                                temp *= 1.0 / (count[tag] + 1)
                                #temp *= 1.0 / (len(emission) + 1)
                        else:
                            temp *= 1.0 / (count[tag] + 1)
                            #temp *= 1.0 / (len(emission) + 1)
                        values.append((temp, prev_tag))
                    viterbi[k][tag] = max(values, key = lambda x: x[0])

            values = []
            for tag in viterbi[n]: # STOP
                temp = 1.0
                temp *= viterbi[n][tag][0]
                if transition.has_key(tag):
                    if transition[tag].has_key('_STOP'):
                        temp *= transition[tag]['_STOP']
                    else:
                        temp *= 0.0
                else:
                    temp *= 0.0
                values.append((temp, tag))
            stop_value = max(values, key = lambda x: x[0])

            # Backtracking
            result_tags = [stop_value[1]]
            for i in range(n, 0, -1):
                if viterbi[i][result_tags[-1]][1] != '_START':
                    result_tags.append(viterbi[i][result_tags[-1]][1])
                else:
                    break
            result_tags.reverse()

            for i in range(len(sentence)):
                result.append((sentence[i], result_tags[i]))
            result.append((None, None))
            # Prepare for next sentence
            sentence = []
    return result

def part3():
    result = calculate_part3(POS_TRAIN, POS_DEV_IN)
    writeResult(RESULT_POS_P3, result)
    correct = readTraining(POS_DEV_OUT)
    acc = accuracy(result, correct)
    if acc != None:
        print '[Part 3] POS Accuracy:', acc

    result = calculate_part3(NPC_TRAIN, NPC_DEV_IN)
    writeResult(RESULT_NPC_P3, result)
    correct = readTraining(NPC_DEV_OUT)
    acc = accuracy(result, correct)
    if acc != None:
        print '[Part 3] NPC Accuracy:', acc

def calculate_part4(filename_train, filename_test):
    train = readTraining(filename_train)

    # Build transition probability
    # Count every tags and transitions
    count = {'_START': 0, '_STOP': 0}
    trans = {}
    for i in range(len(train)):
        if i == 0:
            count['_START'] += 1
        elif train[i - 1] == (None, None):
            count['_START'] += 1

        if train[i] == (None, None): # End of sentence
            count['_STOP'] += 1
            if not trans.has_key(train[i - 1][1]):
                trans[train[i - 1][1]] = {}
            if not trans[train[i - 1][1]].has_key('_STOP'):
                trans[train[i - 1][1]]['_STOP'] = 0
            trans[train[i - 1][1]]['_STOP'] += 1
        else: # A word
            if not count.has_key(train[i][1]):
                count[train[i][1]] = 0
            count[train[i][1]] += 1
            if i == 0: # Start
                if not trans.has_key('_START'):
                    trans['_START'] = {}
                if not trans['_START'].has_key(train[i][1]):
                    trans['_START'][train[i][1]] = 0
                trans['_START'][train[i][1]] += 1
            if train[i - 1] == (None, None): # Start
                if not trans.has_key('_START'):
                    trans['_START'] = {}
                if not trans['_START'].has_key(train[i][1]):
                    trans['_START'][train[i][1]] = 0
                trans['_START'][train[i][1]] += 1
            else: # In the middle of sentence
                if not trans.has_key(train[i - 1][1]):
                    trans[train[i - 1][1]] = {}
                if not trans[train[i - 1][1]].has_key(train[i][1]):
                    trans[train[i - 1][1]][train[i][1]] = 0
                trans[train[i - 1][1]][train[i][1]] += 1

    # Calculate transition probability
    transition = {}
    for key1 in count:
        if not transition.has_key(key1):
            transition[key1] = {}
        for key2 in count:
            if not transition[key1].has_key(key2):
                transition[key1][key2] = 0.0
            if trans.has_key(key1):
                if trans[key1].has_key(key2):
                    transition[key1][key2] = float(trans[key1][key2]) / count[key1]

    # Count emissions
    em = {}
    for item in train:
        if item == (None, None):
            continue
        if not em.has_key(item[1]):
            em[item[1]] = {}
        if not em[item[1]].has_key(item[0]):
            em[item[1]][item[0]] = 0
        em[item[1]][item[0]] += 1

    # Calculate emission probability
    emission = {}
    for tag in em:
        if not emission.has_key(tag):
            emission[tag] = {}
        for word in em[tag]:
            if not emission[tag].has_key(word):
                emission[tag][word] = 0.0
            emission[tag][word] = float(em[tag][word]) / (count[tag] + 1)

    # Viterbi
    test = readTesting(filename_test)
    result = []
    sentence = []
    for w in test:
        if(w != None):
            sentence.append(w)
        else: # End of a sentence
            # Initialize viterbi
            viterbi = [{} for i in range(len(sentence) + 1)]
            for k in viterbi:
                for tag in count:
                    if count == '_STOP': # Skip STOP tag
                        continue
                    k[tag] = (0.0, None)
            viterbi[0]['_START'] = (1.0, None)

            n = len(viterbi) - 1
            for k in range(1, n + 1):
                for tag in viterbi[k]:
                    if tag == '_START':
                        viterbi[k][tag] = (0.0, None)
                        continue
                    values = []
                    for prev_tag in viterbi[k-1]:
                        temp = 1.0
                        temp *= viterbi[k-1][prev_tag][0] # pi(k-1, u)
                        if transition.has_key(prev_tag): # * a(u, v)
                            if transition[prev_tag].has_key(tag):
                                temp *= transition[prev_tag][tag]
                            else:
                                temp *= 0.0
                        else:
                            temp *= 0.0
                        if emission.has_key(tag): # * b(v, x_k)
                            if emission[tag].has_key(sentence[k - 1]):
                                temp *= emission[tag][sentence[k - 1]]
                            else:
                                temp *= 1.0 / (count[tag] + 1)
                                #temp *= 1.0 / (len(emission) + 1)
                        else:
                            temp *= 1.0 / (count[tag] + 1)
                            #temp *= 1.0 / (len(emission) + 1)
                        values.append((temp, prev_tag))
                    viterbi[k][tag] = nlargest(10, values, key = lambda x: x[0])[-1]

            values = []
            for tag in viterbi[n]: # STOP
                temp = 1.0
                temp *= viterbi[n][tag][0]
                if transition.has_key(tag):
                    if transition[tag].has_key('_STOP'):
                        temp *= transition[tag]['_STOP']
                    else:
                        temp *= 0.0
                else:
                    temp *= 0.0
                values.append((temp, tag))
            stop_value = max(values, key = lambda x: x[0])

            # Backtracking
            result_tags = [stop_value[1]]
            for i in range(n, 0, -1):
                if viterbi[i][result_tags[-1]][1] != '_START':
                    result_tags.append(viterbi[i][result_tags[-1]][1])
                else:
                    break
            result_tags.reverse()

            for i in range(len(sentence)):
                result.append((sentence[i], result_tags[i]))
            result.append((None, None))
            # Prepare for next sentence
            sentence = []

    return result

def part4():
    result = calculate_part4(POS_TRAIN, POS_DEV_IN)
    writeResult(RESULT_POS_P4, result)
    correct = readTraining(POS_DEV_OUT)
    acc = accuracy(result, correct)
    if acc != None:
        print '[Part 4] POS Accuracy:', acc

    result = calculate_part4(NPC_TRAIN, NPC_DEV_IN)
    writeResult(RESULT_NPC_P4, result)
    correct = readTraining(NPC_DEV_OUT)
    acc = accuracy(result, correct)
    if acc != None:
        print '[Part 4] NPC Accuracy:', acc

def test():
    result = calculate_part2(r'.\train', r'.\test')
    writeResult(r'.\test_result', result)

if __name__ == '__main__':
    pass
    part2()
    part3()
    part4()
