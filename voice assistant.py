import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
from textblob import TextBlob  


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = None
    try:
        with sr.Microphone() as source:
            print("Listening...")
            talk("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
    except Exception as e:
        print(f"An error occurred: {e}")
    return command

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  

def run_assistant():
    command = take_command()
    if command:
        if 'quit' in command:
            return "quit"
        if 'assistant' in command:
            command = command.replace('assistant', '').strip()

        print(f"Recognized command: {command}")  

     
        sentiment_score = analyze_sentiment(command)
        
       
        print(f"Sentiment score: {sentiment_score}")  

      
        if sentiment_score > 0:
            talk("I'm glad to hear that!")
        elif sentiment_score < 0:
            talk("I'm sorry to hear that.")
        else:
            talk("I see. Let's continue.")  

        if 'play' in command:
            song = command.replace('play', '').strip()
            talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            talk(f'Current time is {time}')
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'open google' in command:
            talk("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'search' in command:
            query = command.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")

    return command


if __name__ == "__main__":
    print("Voice Assistant is ready. Type 'quit' to exit.")
    
    while True:
        result = run_assistant()
        if result == "quit":
            break
