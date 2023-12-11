import wikipediaapi
choice = 0

def getData(data):
    print("\nSummary:", data.summary)

def print_sections(sections):
    print("\nSections:")
    for i, s in enumerate(sections, 1):
        print(f"{i}. {s.title}")
        
def print_fullText(fullText):
    print("\nFull Text:", fullText)

def main():
    wiki_wiki = wikipediaapi.Wikipedia('AI_Assitant', 'en')
    query = input("I want to search: ")

    page_py = wiki_wiki.page(query)
    if page_py.exists():
        while True:
            print("\nOptions:")
            print("1. View Summary")
            print("2. View Sections")
            print("3. View Full Text")
            print("4. Exit")
            
            choice = input("Enter your choice (1/2/3/4): ")
            
            if choice == '1':
                getData(page_py)
            elif choice == '2':
                print_sections(page_py.sections)
            elif choice == '3':
                print_fullText(page_py.text)
                break
            elif choice == '4':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    else:
        print('Page not found')

if __name__ == "__main__":
    main()