def readNumber(line, index):  
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def readDivision(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1    

def tokenize(line):  
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)    
        elif line[index] == '/':
            (token, index) = readDivision(line, index)    
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
        #print(tokens)
    return tokens

def evaluate_first(tokens):
    answer = 1
    tokens.insert(0, {'type': 'TIMES'}) # Insert a dummy '*' token
    index = 1
    while index < len(tokens):
        #print(index)
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'TIMES':
                answer *= tokens[index]['number']
                tokens[index-1]['type'] = 'PLUS'
                tokens[index]['number'] = 0
            elif tokens[index - 1]['type'] == 'DIVISION':
                answer /= tokens[index]['number']
                tokens[index-1]['type'] = 'PLUS'
                tokens[index]['number'] = 0
            elif tokens[index - 1]['type'] == 'PLUS' or tokens[index-1]['type'] == 'MINUS':
                tokens[index-2]['type'] = 'NUMBER'
                tokens[index-2]['number'] = answer
                answer = tokens[index]['number']
                if (index!=len(tokens)-1) and (tokens[index+1]['type'] == 'TIMES' or tokens[index+1]['type'] == 'DIVISION'):
                    tokens[index]['number'] = 0
            else:
                print('Invalid syntax')
                exit(1)
        # print(tokens)
        # print(answer)
        # print("="*10)
        index += 1
    tokens[index-1]['type'] = 'NUMBER'
    tokens[index-1]['number'] = answer
    #print(tokens)
    return tokens

def evaluate_second(tokens):
    answer = 0
    if tokens[0] != {'type': 'PLUS'}:
        tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    # print("~"*10)
    # print(tokens)
    # print("~"*10)
    #actualAnswer = evaluate_first(tokens)
    if '*' in line or '/' in line:
        #print("OK")
        tokens = evaluate_first(tokens)
    answer = evaluate_second(tokens)
    print("answer:%s" % answer)
    return answer

while True:
    print('> ', end="")
    line = input()
    #tokens = tokenize(line)
    answer = test(line)
    #print("answer = %f\n" % answer)

