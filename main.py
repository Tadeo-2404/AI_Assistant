import wikipediaapi
import pyttsx3
import speech_recognition as sr
import requests, json
import time
import os
from dotenv import load_dotenv

wiki_wiki = wikipediaapi.Wikipedia('AI_Assistant', 'en')  # Wikipedia API instance
recognizerAudio = sr.Recognizer()  # SpeechRecognition instance
engine = pyttsx3.init()  # Initialize the engine voice
engine.setProperty('rate', 165)  # Set rate property
load_dotenv()

def type_text(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def get_device_city():
    try:
        # Make a request to the ipinfo.io API
        response = requests.get('https://ipinfo.io')
        data = response.json()

        # Extract city information
        city = data.get('city', 'Unknown')
        
        return city
    except Exception as e:
        print(f"Error: {e}")
        return None

def getWeather(): 
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    device_city = get_device_city()
    complete_url = base_url + "appid=" + api_key + "&q=" + device_city
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        type_text(f'\nTemperature in {device_city} is: {round(temp-273.15, 2)}c')
        engine.say(f'Temperature in {device_city} is: {round(temp-273.15, 2)}c')
        engine.runAndWait()
        type_text(f'\nDescription: {desc}')
        engine.say(f'Description: {desc}')
        engine.runAndWait()
    else:
        type_text('\nError fetching weather data')
        engine.say('Error fetching weather data')
        engine.runAndWait()

def getData(data):
    engine.say("\nSummary: " + data.summary)
    engine.runAndWait()

def print_sections(sections):
    engine.say("\nSections:")
    engine.runAndWait()
    for i, s in enumerate(sections, 1):
        engine.say(f"{i}. {s.title}")
    engine.runAndWait()

def print_full_text(full_text):
    engine.say("Full Text: " + full_text)
    engine.runAndWait()

def search_query(query):
    engine.say(f"Searching {query}, this may take a few seconds")
    engine.runAndWait()
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        engine.say(f"Select an option, to exit the application type number 4")
        engine.runAndWait()
        while True:
            print("\nOptions:")
            print("1. View Summary")
            print("2. View Sections")
            print("3. View Full Text")
            print("4. Exit")

            engine.say("Enter your choice 1, 2, 3, or 4; type 4 for exit")
            engine.runAndWait()
            choice = input("Enter your choice 1, 2, 3, or 4; type 4 for exit: ")

            if choice == '1':
                engine.say("You chose option 1: View Summary")
                engine.runAndWait()
                getData(page_py)
            elif choice == '2':
                engine.say("You chose option 2: View Sections")
                engine.runAndWait()
                print_sections(page_py.sections)
            elif choice == '3':
                engine.say("You chose option 3: View Full Text")
                engine.runAndWait()
                print_full_text(page_py.text)
                break
            elif choice == '4':
                engine.say("Exiting the program. Goodbye!")
                engine.runAndWait()
                break
            else:
                engine.say("Invalid choice. Please enter 1, 2, 3, or 4.")
                engine.runAndWait()
    else:
        engine.say("Page not found")
        engine.runAndWait()

def run_command(command):
    type_text(f"\nYou said: {command}")
    engine.say(f"You said: {command}")
    engine.runAndWait()
    
    if "search definition" in command:
        search_query(command, wiki_wiki, engine)
    elif "get weather" in command:
        getWeather()
    elif "exit" in command:
        exit()
    else:
        type_text("\nI am sorry, your instruction is not available")
        engine.say("I am sorry, your instruction is not available")
        engine.runAndWait()

def main():
    print('Say "OK Mike" to start...')

    while True:
        with sr.Microphone() as source:
            recognizerAudio.adjust_for_ambient_noise(source)
            audioCall = recognizerAudio.listen(source)

            try:
                text = recognizerAudio.recognize_google(audioCall)
                text = text.lower()
                print(text)

                if text == "okay mike":
                    type_text("Hello there! Welcome, I am Mike, your AI Personal Assistant.")
                    engine.say(f"Hello there! Welcome, I am Mike, your AI Personal Assistant.")
                    engine.runAndWait()
                    type_text(f"\nSelect an option from the list:")
                    engine.say(f"Select an option from the list:")
                    engine.runAndWait()
                    type_text(f"\n- Search definition")
                    engine.say(f"- Search definition")
                    engine.runAndWait()
                    type_text(f"\n- Get Weather")
                    engine.say(f"- Get Weather")
                    engine.runAndWait()
                    type_text(f"\n- Exit")
                    engine.say(f"- Exit")
                    engine.runAndWait()

                    with sr.Microphone() as source_command:
                        recognizerAudio.adjust_for_ambient_noise(source_command)
                        audioCall_command = recognizerAudio.listen(source_command)

                        try:
                            command = recognizerAudio.recognize_google(audioCall_command)
                            command = command.lower()
                            run_command(command)
                        except sr.UnknownValueError:
                            type_text("Could not understand the audio, try again")
                            engine.say("Could not understand the audio, try again")
                            engine.runAndWait()
                        except sr.RequestError as e:
                            engine.say(f"Error: {e}")
                            engine.runAndWait()
                    break  # Break the loop after processing a command

            except sr.UnknownValueError:
                type_text("Could not understand the audio, try again")
                engine.say("Could not understand the audio, try again")
                engine.runAndWait()
            except sr.RequestError as e:
                engine.say(f"Error: {e}")
                engine.runAndWait()

if __name__ == "__main__":
    main()
