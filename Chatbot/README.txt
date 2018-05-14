Andrew Levandowski, Daniel Hernandez, Ehsan Afshinpour
CS 582 - Intro to Speech Processing
Chatbot Setup
------------------------------------------------------
1. Extract zip folder

2. Download or update Python Interpretor 3.6+ recommended (if you don't have)
   - Download at
     https://www.python.org/
		  OR
   - Update using command 'pip install python --upgrade' or 'pip install python -U'
     in cmd

3. Download neccesary modules (all pip commands should be done in CMD after installing Python)
   - TextBlob
     http://textblob.readthedocs.io/en/dev/install.html
                  OR
     'pip install -U textblob'
     'python -m textblob.download_corpora'
   - NLTK module
     https://pypi.org/project/nltk/
                  OR
     'pip install -U nltk'
   - pyttsx3 (for text to speech)
     https://pypi.org/project/pyttsx3/
                  OR
     'pip install pyttsx3'
     'pip install pypiwin32'

4. In the extracted folder first run 'generate_data.py'
   by double clicking. This should create dictionary.json within the folder.

5. Run chatbot.py to use chatbot