import os
import json
import re

def read_data(filename):
    if not os.path.isfile(FILENAME):
        return
    
    with open(filename, 'r') as f:
        return json.loads(f.read())

def translate(code, data):
    result = []
    for row in code.split('\n'):
        prepared = row.lstrip()
        if not prepared:
            result.append(row)
            continue
        
        resultRow = row
        spaceCount = len(row) - len(prepared)
        words = findEnglishWords(prepared)
        for (start, word) in words[::-1]:
            key = word.lower()
            if not key in data:
                rawInput = input(f'Введите перевод {word} (по умолчанию {word}): ').strip()
                data[key] = rawInput if rawInput else word
                if not rawInput:
                    continue
            
            translation = data[key]
            resultRow = replace(resultRow, word, translation, spaceCount + start)
    
        result.append(resultRow)
    return str.join('\n', result)

def findEnglishWords(row):
    pattern = r'[A-Za-z]{1}[A-Za-z\d]*'
    words = re.findall(pattern, row)
    
    # group words with start indexes
    return [(m.start(0), words[i]) for i, m in enumerate(re.finditer(pattern, row))]

def replace(s, oldvalue, newvalue, fromIndex, count=1):
    if fromIndex not in range(len(s)):
        raise ValueError("index outside given string")
    return s[:fromIndex] + s[fromIndex:].replace(oldvalue, newvalue, count)


if __name__ == '__main__':
    FILENAME = 'data.json'
    row = '''&AtClient
Procedure РасчетПоФормуле(Command)	
    Rate = 20;
    Factor = 25;
    
    SellingPrice = (ИсходноеЧисло + ИсходноеЧисло * Rate / 100) * (1 + Factor / 100);
    SellingPriceSum = SellingPrice * РезультатЧислом;
    
    Message(SellingPriceSum);
    Message(Round(SellingPriceSum, 1, Mode.Round15as20));
    Message(Round(SellingPriceSum, -2, Mode.Round15as20) - 5);
    
EndProcedure'''

    data = read_data(FILENAME)
    if not data:
        print('Конфиг не найден')
        exit()

    result = translate(row, data)
    print()
    print('=' * 20)
    print()
    print(result)
