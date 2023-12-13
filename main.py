import wikipediaapi
import pyttsx3
import speech_recognition as sr

def getData(data, engine):
    engine.say("Summary: " + data.summary)
    engine.runAndWait()

def print_sections(sections, engine):
    engine.say("Sections:")
    engine.runAndWait()
    for i, s in enumerate(sections, 1):
        engine.say(f"{i}. {s.title}")
    engine.runAndWait()

def print_full_text(full_text, engine):
    engine.say("Full Text: " + full_text)
    engine.runAndWait()

def search_query(query, wiki_wiki, engine):
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
                getData(page_py, engine)
            elif choice == '2':
                engine.say("You chose option 2: View Sections")
                engine.runAndWait()
                print_sections(page_py.sections, engine)
            elif choice == '3':
                engine.say("You chose option 3: View Full Text")
                engine.runAndWait()
                print_full_text(page_py.text, engine)
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

def run_command(command, wiki_wiki, engine):
    engine.say(f"You said: {command}")
    engine.runAndWait()
    search_query(command, wiki_wiki, engine)

def main():
    wiki_wiki = wikipediaapi.Wikipedia('AI_Assistant', 'en')  # Wikipedia API instance
    recognizerAudio = sr.Recognizer()  # SpeechRecognition instance
    engine = pyttsx3.init()  # Initialize the engine voice
    engine.setProperty('rate', 165)  # Set rate property
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
                    engine.say(f"Hello there! Welcome, I am Mike, your AI Personal Assistant. Please, tell me what you need:")
                    engine.runAndWait()

                    with sr.Microphone() as source_command:
                        recognizerAudio.adjust_for_ambient_noise(source_command)
                        audioCall_command = recognizerAudio.listen(source_command)

                        try:
                            command = recognizerAudio.recognize_google(audioCall_command)
                            command = command.lower()
                            run_command(command, wiki_wiki, engine)
                        except sr.UnknownValueError:
                            engine.say("Could not understand the audio, try again")
                            engine.runAndWait()
                        except sr.RequestError as e:
                            engine.say(f"Error: {e}")
                            engine.runAndWait()
                    break  # Break the loop after processing a command

            except sr.UnknownValueError:
                engine.say("Could not understand the audio, try again")
                engine.runAndWait()
            except sr.RequestError as e:
                engine.say(f"Error: {e}")
                engine.runAndWait()

if __name__ == "__main__":
    main()
