import wikipediaapi
import pyttsx3

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

def main():
    wiki_wiki = wikipediaapi.Wikipedia('AI_Assitant', 'en')
    engine = pyttsx3.init()
    engine.say(f"Hello there!! Welcome, I am your Cobby, your AI Personal Assitant, please, type your search below")
    engine.runAndWait()
    query = input("I want to search: ")
    engine.say(f"Searching {query}, this may take a few seconds")
    engine.runAndWait()

    page_py = wiki_wiki.page(query)
    if page_py.exists():
        engine.say(f"Select an option, to exit the application type number 4")
        while True:
            print("\nOptions:")
            print("1. View Summary")
            print("2. View Sections")
            print("3. View Full Text")
            print("4. Exit")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == '1':
                engine.say("You chose option 1: View Summary")
                getData(page_py, engine)
            elif choice == '2':
                engine.say("You chose option 2: View Sections")
                print_sections(page_py.sections, engine)
            elif choice == '3':
                engine.say("You chose option 3: View Full Text")
                print_full_text(page_py.text, engine)
                break
            elif choice == '4':
                engine.say("Goodbye")
                print("Exiting the program. Goodbye!")
                break
            else:
                engine.say("Invalid choice. Please enter 1, 2, 3, or 4.")
                engine.runAndWait()

    else:
        engine.say("Page not found")
        engine.runAndWait()

if __name__ == "__main__":
    main()
