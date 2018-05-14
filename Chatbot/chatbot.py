'''
Names: Andrew Levandowski, Daniel Hernandez, Ehsan Afshinpour
Class: CS 582 - Intro to Speech Processing
Des: This program is the main file for the chatbot. Using Markov Chain dictionary to create sentences.

References:
0612 TV, director. Markov Chains - Make a Chatting AI! YouTube, YouTube, 23 Aug. 2016, www.youtube.com/watch?v=L97yQMT0jn8.

Daly, Liza. “Chatbot Fundamentals.” Chatbot Fundamentals: An Interactive Guide to Writing Bots in Python, apps.worldwritable.com/tutorials/chatbot/.
'''

import json
import random
import nltk
import os.path
import sys
import pyttsx3		# Used for tts

from textblob import TextBlob	# Needed for TextBlob

# Set up tts
engine = pyttsx3.init()
engine.setProperty('rate', 140)

dictName = 'dictionary.json'

# Preset input
GREETING_KEYWORDS = ('hello', 'hi', 'hey', 'sup', "what's up", 'howdy', 'good morning', 'greetings', 'good afternoon' \
    'good evening', 'wassup', 'yo', 'hiya')

# Preset responses
GREETING_RESP = ('hello', 'YO', "how's it going?", 'hi, how are you?', '*waves*', '*nods*', "how you doin'")

DEFAULT_RESP = ('Yeah, totally', 'I like pie', 'You right!')

def main():
    print('=========\n' +
          '|| BOT ||\n' +
          '===================================')
    print('|| Enter \'!exit\' to stop program.||\n' +
          '===================================\n')
    while True:
        result = ""
        found = False

        sentence = input('>> ')
        if sentence == '!exit':
            exit(1)
        else:
            clean_sentence = clean_text(sentence)
			# Log to keep record of what has been said
            new_training_data = open("chat_log.txt", "a")
            new_training_data.write('user: ' + clean_sentence + '\n')
            parsed = TextBlob(clean_sentence)
            pronoun, noun, adjective, verb = find_part_of_speech(parsed)
            greeting = check_for_greeting(parsed)
			
			# Found default greeting
            if greeting is not None:
                print(greeting)
                new_training_data.write('Bot: ' + greeting + ".\n")
                new_training_data.close()
                engine.say(greeting)
                engine.runAndWait()
                continue
            else:
                dictionary = loadDictionary()
				# Choose best possible word to search through chain
                startWord = chooseWord(pronoun, noun, adjective, verb)
                result = startWord
				# Restrict sentence to 4-6 words
                length = random.randint(4,6)
                for key in dictionary:
                    if startWord == key:
                        found = True
						 
                if found:
                    for i in range(0, length):
						# Construct sentence
                        newWord = getNextWord(startWord, dictionary)
                        result = result + " " + newWord
                        startWord = newWord
						
				# If starting word isn't found in the dictionary use another default response
                else:
                    resp = random.choice(DEFAULT_RESP)
                    print(resp)
                    new_training_data.write('Bot: ' + resp + "\n")
                    new_training_data.close()
                    engine.say(resp)
                    engine.runAndWait()
                    continue
					
				# If pronoun and verb found use opposite of that pronoun and verb
                if pronoun:
                    if verb:
                        if noun:
                            result = pronoun + " " + verb[0] + " " + result
                        else:
                            result = pronoun + " " + result
				
				# Bot response
                print(result.lower().capitalize() + ".")
                new_training_data.write('Bot: ' + result.lower().capitalize() + ".\n")
                new_training_data.close()
                engine.say(result)
                engine.runAndWait()
                continue

'''
Corrects certain words to be put in TextBlob
'''
def clean_text(sent):
    cleaned = []
    words = sent.split(' ')

    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        if w == 'im':
            w = "I'm"
        if w == 'cant':
            w = "can't"
        if w == 'wouldnt':
            w = "would'nt"
        if w == 'couldnt':
            w = "couldn't"
        if w == 'wont':
            w = "won't"
        if w == 'aint':
            w = "ain't"
        if w == 'arent':
            w = "aren't"
        if w == 'isnt':
            w = "isn't"
        if w == 'wasnt':
            w = "wasn't"
        if w == 'werent':
            w = "weren't"
        if w == 'dont':
            w = "don't"
        if w == 'didnt':
            w = "didn't"
        if w == 'arent':
            w = "aren't"
        if w == 'doesnt':
            w = "doesn't"
        cleaned.append(w)

    return ' '.join(cleaned)

'''
Finds the pronouns, nouns, adjectives, and verbs within a sentence
'''
def find_part_of_speech(parsed):
        pronoun = None
        nouns = []
        adjectives = []
        verbs = []

        for sent in parsed.sentences:
            p = find_pronoun(sent)
            n = find_noun(sent,nouns)
            a = find_adjective(sent, adjectives)
            v = find_verb(sent, verbs)

            pronoun = p
            nouns = n
            adjectives = a
            verbs = v

        return pronoun, nouns, adjectives, verbs

'''
Pronouns
'''
def find_pronoun(sent):
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            pronoun = 'You'
        elif part_of_speech == 'PRP':
            pronoun = word

    return pronoun


'''
Nouns
'''
def find_noun(sent, nouns):
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'NN' or part_of_speech == 'NNS' or part_of_speech == 'NNP' or part_of_speech == 'NNPS':
            nouns.append(word)

    return nouns

'''
Adjectives
'''
def find_adjective(sent, adj):
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'JJ' or part_of_speech == 'JJR' or part_of_speech == 'JJS':
            adj.append(word)

    return adj


'''
Verbs
'''
def find_verb(sent, verbs):
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'VB' or part_of_speech == 'VBD' or part_of_speech == 'VBG' or part_of_speech == 'VBN' or\
                part_of_speech == 'VBP' or part_of_speech == 'VBZ':
            verbs.append(word)

    return verbs

'''
Default greeting messages
'''
def check_for_greeting(sent):
    for word in  sent.sentences:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESP)
    return None


def loadDictionary():
    if not os.path.exists(dictName):
        sys.exit("Error: dictionary not found")

    file = open(dictName, "r")
    dictionary = json.load(file)
    file.close()
    return dictionary

'''
Returns what word to search through our Markov Chain
'''
def chooseWord(p, n, a, v):
    if p:
        if v:
            if n:
                if len(n) > 1:
                    num = random.randint(0, len(n) - 1)
                    return n[num]
                else:
                    return n[0]
            else:
                if len(v) > 1:
                    num = random.randint(0, len(v) - 1)
                    return v[num]
                else:
                    return v[0]
    elif n:
        if len(n) > 1:
            num = random.randint(0, len(n)-1)
            return n[num]
        else:
            return n[0]
    elif a:
        if len(a) > 1:
            num = random.randint(0, len(a) - 1)
            return a[num]
        else:
            return a[0]

    return None

'''
Returns the most likely word following the key (word) given
'''
def getNextWord(word, dict):
    THRESHOLD = .4			 # Needed to check if word frequency is 40% or higher than highest freq
    candidates = dict[word]  # Possible word candidates 
    candidatesNormalized = []  # Candidates to randomly pick from
    highestFreq = 0            # Highest frequency within key/value group

	#Find highest freq in group
    for w in candidates:
        if candidates[w] > highestFreq:
            highestFreq = candidates[w]

    for w in candidates:
        freq = candidates[w]
		# Discard lower than threshold choices
        if (freq/highestFreq) <= THRESHOLD:
            continue
        else:
			# Place possible choice in array to be randomly selected
            for i in range(0, freq):
                candidatesNormalized.append(w)

    rnd = random.randint(0, len(candidatesNormalized)-1)
    return candidatesNormalized[rnd]


main()
