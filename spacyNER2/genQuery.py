import ollama
import json

def generateAnnotations(filename, annotFileName):
    data = {
        'classes': ["gender","occassion","wearable","color","location","age"],
        'annotations': []
    }
    modfile = '''FROM mistral
    SYSTEM "you can answer in only 1-2 key words"
    '''
    ollama.create('example', modelfile=modfile)
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            # dictionary which contains the entities for the given line
            ents = {
                'entities' : []
            }
            print(f'sent: {line}')
            for i in data['classes']:
                print(f'Class: {i}')
                response = ollama.chat(model='example', messages=[
                    {
                        'role' : 'user',
                        'content' : f'give me the {i} of the following sentence in one word: {line}'
                    },
                ])
                print(response['message']['content'])
                firstword = response['message']['content'].split('.')
                ents['entities'].append(firstword[0])
            data['annotations'].append(line)
            data['annotations'].append(ents)
            line = f.readline()
    with open (annotFileName, 'a') as a:
        json.dump(data, a)


def removeLineNum(sent):
    tokens = sent.split()
    return ' '.join(tokens[1:]), tokens[0]

def main(filename, num_sent, templates):
    print('numsent: ', num_sent)
    response = ollama.chat(model='mistral', messages=[
        {
            'role' : 'user',
            'content': f'generate {num_sent} sentences using the following template: {templates[0]}'
        }
    ], options={
                    'temperature' : 0
               })

    content = response['message']['content']
    sentences = content.split('\n')


    with open(filename, 'a') as f:
        for i in sentences:
            sent, number = removeLineNum(i)
            print(f'got number: {number}')
            f.write(sent+'\n')

if __name__ == "__main__":
    filename = 'queries.txt'
    annotfile = 'annotationsTest.json'
    num_sent = 1000
    templates = [
        'show me a {{adjective}} {{fashion noun}} for {{person noun}} for {{occassion noun}}'
    ]
    for i in range(3):
        main(filename, num_sent, templates)
    # generateAnnotations(filename, annotfile)
