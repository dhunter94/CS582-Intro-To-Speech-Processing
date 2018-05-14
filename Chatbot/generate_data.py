'''
Names: Andrew Levandowski, Daniel Hernandez, Ehsan Afshinpour
Class: CS 582 - Intro to Speech Processing
Des: This program is intended to make a dictionary JSON file that constructs a Markov Chain of word sequences.

References:
0612 TV, director. Markov Chains - Make a Chatting AI! YouTube, YouTube, 23 Aug. 2016, www.youtube.com/watch?v=L97yQMT0jn8.

Daly, Liza. “Chatbot Fundamentals.” Chatbot Fundamentals: An Interactive Guide to Writing Bots in Python, apps.worldwritable.com/tutorials/chatbot/.
'''

import json         # Needed to make a JSON file
import os.path      # Check to see if file exists already
import datetime     # For logging/timing purposes

dictName = "dictionary.json"    # JSON file name
fileName = "movie_lines.txt"    # Movie script corpus name


def main():
    dictionary = loadDictionary()
    parsedFile = parseText()
    dictionary = learn(dictionary, parsedFile)
    updateFile(dictionary)

''' 
Creation of dictionary file. Open for reading.
'''
def loadDictionary():
    # Create JSON file if doesn't exist
    if not os.path.exists(dictName):
        file = open(dictName, "w")
        json.dump({}, file)
        file.close()

    # Open JSON file
    file = open(dictName, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary

'''
Parse movie corpus to get lines of dialogue
'''
def parseText():
    textLines = []

    with open(fileName, 'r') as text:
        print('Parsing Text File: {0}'.format(datetime.datetime.now()))
        for line in text:
            l = line.split('+++$+++ ', 7)[4]
            textLines.append(l)
        print('\tSuccessful: {0}\n'.format(datetime.datetime.now()))
        cleaned_text = clean_up_text(textLines)
    return cleaned_text


'''
Remove unnecessary punctuation
'''
def clean_up_text(textfile):
    cleaned_text = []

    print('Clean-up of Text: {0}'.format(datetime.datetime.now()))
    for line in textfile:
        l = line.replace('\n', '').replace('.', '').replace('...', '').replace('!', '').replace('?', '')\
            .replace('-- ', '').replace('<u>', '').replace('</u>', '').replace('---', '').replace('- ', '') \
            .replace('--', '').replace(' --', ''). replace('  ', ' ').replace('<i>', '').replace('</i>', '') \
            .replace('\t', ' ').replace('<U>', '').replace('</U>', '').replace('_', '').replace(',', '')
        cleaned_text.append(l)
    print('\tSuccessful: {0}\n'.format(datetime.datetime.now()))
    return cleaned_text


'''
Creation of Markov Chain/dictionary
'''
def learn(dict, input):
    print('Learning/Tokenizing: {0}'.format(datetime.datetime.now()))
    for lines in input:
        tokens = list(filter(None, lines.split(' ')))

        for i in range(0, len(tokens)-1):
            currentWord = tokens[i]
            nextWord = tokens[i+1]

            #Key not in dictionary create it and add its value
            if currentWord not in dict:
                dict[currentWord] = { nextWord : 1}
            else:
                allNextWords = dict[currentWord]

                #If value not found within key, add it
                if nextWord not in allNextWords:
                    dict[currentWord][nextWord] = 1
                #If key and value found, increment its frequency
                else:
                    dict[currentWord][nextWord] = dict[currentWord][nextWord] + 1
    print('\tSuccessful: {0}\n'.format(datetime.datetime.now()))
    return dict

'''
Update dictionary file with key/value pairs
'''
def updateFile(dict):
    print('Writing to JSON File: {0}'.format(datetime.datetime.now()))
    file = open(dictName, "w")
    json.dump(dict, file)
    file.close()
    print('\tSuccessful: {0}'.format(datetime.datetime.now()))


main()
