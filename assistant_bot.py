import sys
sys.path.append('classes')
from classes import Record, Note
from address_book import AddressBook
from note_book import NotesBook

def input_error(func):
    '''
    Обробка винятків
    '''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) in ["Phone number must be 10 digits long", "Birthday must be in the format DD.MM.YYYY", "Email is not valid"]:
                return str(e)
            else:
                return "Give me correct data please"
        except AttributeError as e:
            if "NoneType" in str(e):
                return "Attribute 'value' is missing"
        except IndexError:
            return "Missing arguments"
        except KeyError:
            return "Not found"
    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

    return "\nContact added.\n"


@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        result = record.change_phone(record.phones[0].value, phone)
        if result:
            return "\nContact updated.\n"
        else:
            return "\nPhone not found.\n"
    else:
        return "\nContact not found.\n"


@input_error
def show_phone(args, book):
    '''
    Відображає номер телефону контакту
    '''
    [name] = args
    record = book.find(name)
    if record:
        return '\n' + ', '.join(map(str, record.phones)) + '\n'
    else:
        return "\nNot found.\n"


@input_error
def show_all_contacts(book):
    '''
    Відображає всі збережені контакти
    '''
    if not book.data:
        return "\nNo contacts stored.\n"

    contact_details = [str(record) for record in book.data.values()]

    return '\n' + f'\n\n'.join(contact_details) + '\n'


@input_error
def add_address(args, book):
    if len(args) < 2:
        return "Missing arguments for adding address. Please provide a name and an address."

    name, address = args[0], ' '.join(args[1:])
    record = book.find(name)
    if record:
        record.add_address(address)
        return "\nAddress added.\n"
    else:
        return "\nContact not found.\n"
    

@input_error
def show_address(args, book):
    [name] = args
    record = book.find(name)
    if record and record.address:
        return '\n' + record.address.value + '\n'
    else:
        return "\nNo contact or address found.\n"


@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "\nEmail added.\n"
    else:
        return "\nContact not found.\n"
    

@input_error
def show_email(args, book):
    [name] = args
    record = book.find(name)
    if record and record.email:
        return '\n' + record.email.value + '\n'
    else:
        return "\nNo contact or email found.\n"


@input_error
def change_address(args, book):
    if len(args) < 2:
        return "\nMissing arguments for changing address. Please provide a name and an address.\n"

    name, address = args[0], ' '.join(args[1:])
    record = book.find(name)
    if record:
        record.address.value = address
        result = record.change_address(address)
        return '\n' + result + '\n'
    else:
        return "\nContact not found.\n"


@input_error
def change_email(args, book):
    name, new_email = args
    record = book.find(name)
    if record:
        result = record.change_email(new_email)
        return '\n' + result + '\n'
    else:
        return "\nContact not found.\n"


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "\nBirthday added.\n"
    else:
        return "\nContact not found.\n"


@input_error
def show_birthday(args, book):
    [name] = args
    record = book.find(name)
    if record and record.birthday:
        return '\n' + record.birthday.value.strftime('%d.%m.%Y') + '\n'
    else:
        return "\nNo birthday found for this contact.\n"


@input_error
def change_birthday(args, book):
    name, new_birthday = args
    record = book.find(name)
    if record:
        result = record.change_birthday(new_birthday)
        return  '\n' + result + '\n'
    else:
        return "\nContact not found.\n"


@input_error
def show_birthdays_in_x_days(args, book):
    '''
    Виводить список контактів з днями народження через вказану кількість днів
    '''
    try:
        days = int(args[0])
        if days < 0:
            return "\nPlease provide a positive number of days.\n"
    except ValueError:
        return "\nInvalid number of days.\n"

    birthdays_in_x_days = book.get_birthdays_in_x_days(days)
    if not birthdays_in_x_days:
        return f"\nNo birthdays in {days} days.\n"

    response = []
    for day, names_and_dates in birthdays_in_x_days.items():
        birthday_strings = [
            f'{name} ({date.strftime("%d.%m.%Y")})' for name, date in names_and_dates]
        day_birthdays = ', '.join(birthday_strings)
        response.append(f"{day}: {day_birthdays}")

    return "\n" + "\n".join(response) + "\n"


@input_error
def search_contacts(args, book):
    search_string = args[0]
    matching_records = book.search_contacts(search_string)
    
    if matching_records:
        result = []
        for record in matching_records:
            info = f"Name: {record.name.value}"
            if record.phones:
                phones_info = "; ".join(phone.value for phone in record.phones)
                info += f"\nPhones: {phones_info}"
            if record.email:
                info += f"\nEmail: {record.email.value}"
            if record.address:
                info += f"\nAddress: {record.address.value}"
            if record.birthday:
                info += f"\nBirthday: {record.birthday.value.strftime('%d.%m.%Y')}"
            result.append(info)
        
        return "\n" + "\n\n".join(result) + '\n'
    else:
        return "\nNo matching contacts found.\n"


@input_error
def delete_contact(args, book):
    name = args[0]
    if name in book.data:
        book.delete_record(name)
        return "\nContact deleted.\n"
    else:
        return "\nContact not found.\n"


@input_error
def add_note(args, notebook):
    title, description_lines = args[0], args[1:]
    description = ' '.join(description_lines)
    note = Note(title, description)
    notebook.add_note(note)
    return "\nNote added.\n"


@input_error
def change_note(args, notebook):
    title = args[0]
    description_lines = args[1:]
    description = ' '.join(description_lines)

    note = notebook.find(title)
    if not note:
        return "\nNote not found.\n"

    result = note.change_note(description)
    return  '\n' + result + '\n'


@input_error
def show_note(args, notebook):
    [title] = args
    note = notebook.find(title)

    if note:
        return f"\nTitle: {note.title}\nDescription: {note.description}\n"
    return "\nNo note found.\n"


@input_error
def search_notes(args, notebook):
    [term] = args
    if len(term) < 3:
        return f"\nSearch term need at least 3 characters.\n"

    results = notebook.search(term)

    if not results:
        return "\nNo matching notes found.\n"
    
    return '\n' + '\n'.join([f"Title: {note.title}\nDescription: {note.description}\n" for note in results]) + '\n'


@input_error
def show_all_notes(notebook):
    '''
    Відображає всі збережені нотатки
    '''
    if not notebook.data:
        return "\nNo notes stored.\n"

    return '\n' + f'\n'.join([f"Title: {note.title}\nDescription: {note.description}\n" for note in notebook.data.values()])  + '\n'


@input_error
def delete_note(args, notebook):
    [title] = args
    if notebook.find(title):
        notebook.delete(title)
        return "\nNote deleted.\n"
    else:
        return "\nNot found.\n"


def hello_command():
    return "\nHow can I help you?\n"


@input_error
def parse_input(user_input):
    '''
    Обробляє введені дані, розділяючи рядок на команду та аргументи
    '''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def test_commands():
    address_book_path = "test_address_book.json"
    book = AddressBook()
    book.load_address_book(address_book_path)

    note_book_path = "test_note_book.json"
    notebook = NotesBook()
    notebook.load_notes(note_book_path)

    commands = [
        "hello",
        "add-contact John 1234567890",
        "change-phone John 9876543210",
        "show-phone John",
        "all-contacts",
        "add-birthday John 01.01.1990",
        "show-birthday John",
        "change-birthday John 02.02.1991",
        "birthdays-in-x-days 30",
        "search-contacts John",
        "delete-contact John",
        "add-address John 123 Main St",
        "show-address John",
        "add-email John john@example.com",
        "show-email John",
        "change-address John 456 Elm St",
        "change-email John john.new@example.com",
        "add-note Meeting Discuss project details",
        "change-note Meeting Discuss project updated details",
        "show-note Meeting",
        "all-notes",
        "search-notes project",
        "exit"
    ]

    for command in commands:
        print(f"Testing command: {command}")
        command, *args = parse_input(command)
        if command == "exit":
            book.save_address_book(address_book_path)
            notebook.save_notes(note_book_path)
            print(f"\nGood bye!\n")
            break
        elif command == "hello":
            print(hello_command())
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "change-phone":
            print(change_contact(args, book))
        elif command == "show-phone":
            print(show_phone(args, book))
        elif command == "all-contacts":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "change-birthday":
            print(change_birthday(args, book))
        elif command == "birthdays-in-x-days":
            print(show_birthdays_in_x_days(args, book))
        elif command == "search-contacts":
            print(search_contacts(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "show-address":
            print(show_address(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "show-email":
            print(show_email(args, book))
        elif command == "change-address":
            print(change_address(args, book))
        elif command == "change-email":
            print(change_email(args, book))
        elif command == "add-note":
            print(add_note(args, notebook))
        elif command == "change-note":
            print(change_note(args, notebook))
        elif command == "show-note":
            print(show_note(args, notebook))
        elif command == "all-notes":
            print(show_all_notes(notebook))
        elif command == "search-notes":
            print(search_notes(args, notebook))


def main():
    '''
    Головна функція, де знаходиться логіка бота
    '''
    address_book_path = "address_book.json"
    book = AddressBook()
    book.load_address_book(address_book_path)

    note_book_path = "note_book.json"
    notebook = NotesBook()
    notebook.load_notes(note_book_path)

    print(f"\nWelcome to the assistant bot!\n")

    while True:
        # Отримання команди від користувача
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)  # Парсинг команди

        # Перевірка команд та відповідна дія
        # addressbook commands
        if command == "hello":
            print(hello_command())
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "change-phone":
            print(change_contact(args, book))
        elif command == "show-phone":
            print(show_phone(args, book))
        elif command == "all-contacts":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "change-birthday":
            print(change_birthday(args, book))
        elif command == "birthdays-in-x-days":
            print(show_birthdays_in_x_days(args, book))
        elif command == "search-contacts":
            print(search_contacts(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "show-address":
            print(show_address(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "show-email":
            print(show_email(args, book))
        elif command == "change-address":
            print(change_address(args, book))
        elif command == "change-email":
            print(change_email(args, book))
        # notebook commands
        elif command == "add-note":
            print(add_note(args, notebook))
        elif command == "change-note":
            print(change_note(args, notebook))
        elif command == "show-note":
            print(show_note(args, notebook))
        elif command == "all-notes":
            print(show_all_notes(notebook))
        elif command == "delete-note":
            print(delete_note(args, notebook))
        elif command == "search-notes":
            print(search_notes(args, notebook))
        elif command in ["close", "exit"]:
            book.save_address_book(address_book_path)
            notebook.save_notes(note_book_path)
            print(f"\nGood bye!\n")
            break  # Вихід
        else:
            print(f"Command not recognized")


# Точка входу
if __name__ == "__main__":
    main()
