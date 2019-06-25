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

def readMultiply(line, index):
    token = {'type': 'MULTI'}
    return token, index + 1

def readDivision(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1    

def readRightParenthesis(line, index):
    token = {'type': 'R_PARENTHESIS'}
    return token, index + 1

def readLeftParenthesis(line, index):
    token = {'type': 'L_PARENTHESIS'}
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
            (token, index) = readMultiply(line, index)    
        elif line[index] == '/':
            (token, index) = readDivision(line, index)
        elif line[index] == '(':
            (token, index) = readLeftParenthesis(line, index)
        elif line[index] == ')':
            (token, index) = readRightParenthesis(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
        #print(tokens)
    return tokens

def multiply(tokens, tmp, index):
    result = tmp['number'] * tokens[index+1]['number']
    tmp = {'type': 'NUMBER', 'number': result}
    return tmp, index+2

def division(tokens, tmp, index):
    result = tmp['number'] / tokens[index+1]['number']
    tmp = {'type': 'NUMBER', 'number': result}
    return tmp, index+2

def evaluate_multiply_division(tokens):
    tmp = {'type': 'PLUS'}
    evaluated_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTI':
            (tmp, index) = multiply(tokens, tmp, index)
        elif tokens[index]['type'] == 'DIVISION':
            (tmp, index) = division(tokens, tmp, index)
        else:
            evaluated_tokens.append(tmp)
            tmp = tokens[index]
            index += 1
    evaluated_tokens.append(tmp)
    return evaluated_tokens

def evaluate_plus_minus(tokens):
    answer = 0
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

def evaluate(tokens):
    evaluated_tokens = evaluate_multiply_division(tokens)
    answer = evaluate_plus_minus(evaluated_tokens)
    return answer

#左端から"("を探してかっこの中を計算する
def solve_parenthesis(tokens):
    left_pos = len(tokens)-1
    right_pos = 0
    while left_pos >= 0:
        if tokens[left_pos]['type'] == 'L_PARENTHESIS':
            right_pos = left_pos
            while right_pos < len(tokens):
                if tokens[right_pos]['type'] == 'R_PARENTHESIS':
                    calc_result_in_parenthesis = evaluate(tokens[left_pos+1:right_pos])
                    tokens[left_pos] = {'type': 'NUMBER', 'number': calc_result_in_parenthesis}
                    for _ in range(left_pos+1, right_pos+1):
                        tokens.pop(left_pos+1)
                    break
                right_pos += 1
        left_pos -= 1
    return tokens

def test(line):
    tokens = tokenize(line)
    solved_parenthesis_tokens = solve_parenthesis(tokens)
    actualAnswer = evaluate(solved_parenthesis_tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))

def runTest():
    print("==== Test started! ====")
    #たし算のみ
    test("1+2")
    test("2.8+3")
    test("3+4.6")
    test("1.2+3.4")
    test("1+2+3")
    test("1.2+3.4+5.6")
    #ひき算のみ
    test("1-2")
    test("5.2-3")
    test("1-2.3")
    test("1.2-3.4")
    test("1-2-3")
    test("1.2-3.4-5.6")
    #たしひき混合
    test("1+2-3")
    test("1+2.3-4.5")
    test("1.2+3.4-5.6")
    test("1-2+3")
    test("1-2.3+4.5")
    test("1.2-3.4+5.6")
    #たし算ひき算かっこ混合
    test("1+2-3")
    test("1+2.3-4.5")
    test("1.2+3.4-5.6")
    test("1-2+3")
    test("1-2.3+4.5")
    test("1.2-3.4+5.6")
    test("(1+2)+3")
    test("1-(2-3)")
    test("(1+2)-3")
    test("(1-2)+3")
    test("(1+2.2)+3")
    test("1.2-(2.2-3)")
    test("(1.3+2.5)-3.1")
    test("(1.2-2.4)+3.5")
   
    #かけ算のみ
    test("2*3")
    test("1.2*3")
    test("2*4.3")
    test("1.2*3.4")
    test("2*4*5")
    test("1.2*3.4*5.6")
    test("0*5")
    #わり算のみ
    test("5/2")
    test("1.2/3")
    test("2/2.3")
    test("1.2/3.4")
    test("4/2/3")
    test("1.2/3.4/5.6")
    test("0/5")
    #かけ算わり算かっこ混合
    test("2*3/5")
    test("2*2.3/4")
    test("2*2.3/4.5")
    test("1.2*3.4/5.6")
    test("1/2*3")
    test("1/2.3*4.5")
    test("1.2/3.4*5.6")
    test("0*4/2")
    test("(2*3)*5")
    test("2.1*(3*5)")
    test("(2.1*3.2)*5.1")
    test("(2/3)/5")
    test("2.1/(3/5)")
    test("(2.1/3.2)/5.1")
    test("(2*2.3)/4")
    test("2*(2.3/4.5)")
    test("(1.2*3.4)/5.6")
    test("1.2*(3.4/5.6)")
    test("(1.2*3.4)/(5.6*2)")
    test("1.2*(3.4/5.6)/3")

    
    #たし算とかけ算・わり算混合
    test("1+2*3")
    test("2.1+1.2*3.4")
    test("2*5+3")
    test("2.1*5+3")
    test("2.1*5+3.2")
    test("2*5+3*4")
    test("2.1*5.2+3*4")
    test("2*5+3.1*4.3")
    test("2.1*5.2+3.1*4.3")
    
    test("1+2/3")
    test("2.1+1.2/3.4")
    test("2/5+3")
    test("2.1/5+3")
    test("2.1/5+3.2")
    test("2/5+3/4")
    test("2.1/5.2+3/4")
    test("2/5+3.1/4.3")
    test("2.1/5.2+3.1/4.3")
    
    #ひき算とかけ算・わり算混合
    test("1-2*3")
    test("2.1-1.2*3.4")
    test("2*5-3")
    test("2.1*5-3")
    test("2.1*5-3.2")
    test("2*5-3*4")
    test("2.1*5.2-3*4")
    test("2*5-3.1*4.3")
    test("2.1*5.2-3.1*4.3")
    
    test("1-2/3")
    test("2.1-1.2/3.4")
    test("2/5-3")
    test("2.1/5-3")
    test("2.1/5-3.2")
    test("2/5-3/4")
    test("2.1/5.2-3/4")
    test("2/5-3.1/4.3")
    test("2.1/5.2-3.1/4.3")
 
    
    #たし算ひき算かけ算わり算混合
    test("1+2-3*4/5")
    test("1+2*3-4/5")
    test("1+2*3/4-5")
    test("1+2/3-4*5")
    test("1+2/3*4-5")
    test("1+2.3-4.5")
    test("1*2+3-4/5")
    test("1.2+3.4-5.6")
    test("1-2+3")
    test("1-2.3+4.5")
    test("1.2-3.4+5.6")
    
    #たし算ひき算かけ算わり算かっこ混合
    test("(1+2)*(3+4)")
    test("(1+2)*(3-4)")
    test("(1-2)*(3-4)")
    test("(1+2)*(3+4)+1")
    test("(1+2)*(3+4)-2")
    test("1+(1+2)*(3+4)")
    test("20-(1+2)*(3+4)")
    test("(1-2)*(3-4)+1")
    test("(1-2)*(3-4)-2")
    test("1+(1+2)*(3-4)")
    test("20-(1+2)*(3-4)")
    test("(1.1+2.2)*(3.3+4.4)")
    test("(1.1+2.2)*(3.3+4.4)+2.3")
    test("(1.1+2.2)*(3.3+4.4)-2.3")
    test("1.4+(1.1+2.2)*(3.3+4.4)")
    test("(1.1-2.2)*(3.3-4.4)")
    test("(1.1-2.2)*(3.3-4.4)+2.3")
    test("(1.1-2.2)*(3.3-4.4)-2.3")
    test("1.4+(1.1-2.2)*(3.3-4.4)")    
    test("20.5-(1.1-2.2)*(3.3-4.4)")
    
    
    test("(1+2)/(3+4)")
    test("(1+2)/(3+4)+1")
    test("(1+2)/(3+4)-2")
    test("1+(1+2)/(3+4)")
    test("(1-2)/(3-4)")
    test("(1-2)/(3-4)+1")
    test("(1-2)/(3-4)-2")
    test("1+(1-2)/(3-4)")
    test("20-(1-2)/(3-4)")
    test("(1.1+2.2)/(3.3+4.4)")
    test("(1.1+2.2)/(3.3+4.4)+2.3")
    test("(1.1+2.2)/(3.3+4.4)-2.3")
    test("1.4+(1.1+2.2)/(3.3+4.4)")
    test("20.5-(1.1+2.2)/(3.3+4.4)")
    test("(1.1-2.2)/(3.3-4.4)")
    test("(1.1-2.2)/(3.3-4.4)+2.3")
    test("(1.1-2.2)/(3.3-4.4)-2.3")
    test("1.4+(1.1-2.2)/(3.3-4.4)")
    test("20.5-(1.1-2.2)/(3.3-4.4)")
    
    test("((1.2+3.4*5.6)*2-1)*2")
    test("((1.2+3.4*5.6)/2-1)*2")
    test("((1.2+3.4*5.6)*2-1)/2")
    test("((3*1-4)+4/(3-7))")
    print("==== Test finished! ====")

#runTest()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    solved_parenthesis_tokens = solve_parenthesis(tokens)
    answer = evaluate(solved_parenthesis_tokens)
    print("answer = %f\n" % answer)