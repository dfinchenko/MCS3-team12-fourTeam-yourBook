from classes import Note, NotesBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct data please"
        except IndexError:
            return "Missing arguments"
        except KeyError:
            return "Not found"
    return inner

@input_error
def add_note(args, book):
    title, description_lines = args[0], args[1:]
    description = ' '.join(description_lines)
    
    note = Note(title, description)
    book.add_note(note)
    return "Note added."

@input_error
def edit_note(args, book):
    title = args[0]
    description_lines = args[1:]
    description = ' '.join(description_lines)

    note = book.find(title)
    if not note:
        return "Note not found."

    note.description = description
    return "Note updated."

@input_error
def show_note(args, book):
    [title] = args
    note = book.find(title)

    if note:
        return f"Title: {note.title}\nDescription: {note.description}"
    return f"No note found with title '{title}'"

@input_error
def search_notes(args, book):
    [term] = args
    if len(term) < 3:
        return "Search term need at least 3 characters."

    results = book.search(term)

    if not results:
        return "No matching notes found."
    
    return '\n'.join([f"Title: {note.title}\nDescription: {note.description}\n---" for note in results])

@input_error
def show_all(book):
    '''
    Відображає всі збережені нотатки
    '''
    if not book.data:
        return "No notes stored."

    return '\n'.join([f"Title: {note.title}\nDescription: {note.description}\n---" for note in book.data.values()])

@input_error
def delete_note(args, book):
    [title] = args
    if book.find(title):
        book.delete(title)
        return "Note deleted."
    else:
        return "Not found."

def hello_command():
    return "How can I help you?"

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    path = "note_book/notes.json"
    book = NotesBook()
    book.load_notes(path)
    print("Welcome to the notes assistant!")

    while True:
        user_input = input("Enter a command (add, edit, show, search, all, delete, exit): ")
        command, *args = parse_input(user_input)
        if command == "hello":
            print(hello_command())
        elif command == "add":
            print(add_note(args, book))
        elif command == "edit":
            print(edit_note(args, book))
        elif command == "show":
            print(show_note(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "delete":
            print(delete_note(args, book))
        elif command == "search":
            print(search_notes(args, book))
        elif command in ["close", "exit"]:
            book.save_notes(path)
            print("Good bye!")
            break
        else:
            print(f"Command '{command}' not recognized")

if __name__ == "__main__":
    main()
