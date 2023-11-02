from classes import Record, AddressBook
import json

def input_error(func):
    '''
    Обробка винятків
    '''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) in ["Phone number must be 10 digits long", "Birthday must be in the format DD.MM.YYYY"]:
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
    '''
    Додає новий контакт до словника контактів
    '''
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

    return "Contact added."

@input_error
def change_contact(args, book):
    '''
    Оновлює номер телефону існуючого контакту
    '''
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)
        return f"Contact updated."
    else:
        return "Not found."

@input_error
def show_phone(args, book):
    '''
    Відображає номер телефону контакту
    '''
    [name] = args
    record = book.find(name)
    if record:
        return ', '.join(map(str, record.phones))
    else:
        return f"Not found."

@input_error
def show_all(book):
    '''
    Відображає всі збережені контакти
    '''
    if not book.data:
        return "No contacts stored."

    return '\n'.join([f"{record.name}: {', '.join(map(str, record.phones))}" for record in book.data.values()])
    
@input_error
def add_birthday(args, book):
    '''
    Додає дату дня народження до контакту
    '''
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    '''
    Відображає дату дня народження по контакту
    '''
    [name] = args
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    else:
        return "No birthday found for this contact."

@input_error
def show_birthdays_next_week(book):
    '''
    Відображає дні народження на наступному тижні
    '''
    birthdays_next_week = book.get_birthdays_per_week()
    if not birthdays_next_week:
        return "No birthdays next week."

    response = []
    for day, names in birthdays_next_week.items():
        response.append(f"{day}: {', '.join(names)}")

    return "\n".join(response)

def hello_command():
    return "How can I help you?"
    
def parse_input(user_input):
    '''
    Обробляє введені дані, розділяючи рядок на команду та аргументи
    '''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def search_contact(args, book):
    search_string = args[0]
    matching_records = book.search(search_string)
    if matching_records:
        return "\n".join(str(record) for record in matching_records)
    else:
        return "No matching contacts found."

@input_error
def delete_contact(args, book):
    name = args[0]
    if name in book.data:
        book.delete_record(name)
        return "Contact deleted."
    else:
        return "Contact not found."
    
def load_address_book(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            book = AddressBook()
            for name, record_data in data.items():
                record = Record(name)
                for phone in record_data.get('phones', []):
                    record.add_phone(phone)
                birthday = record_data.get('birthday')
                if birthday:
                    record.add_birthday(birthday)
                book.add_record(record)
            return book
    except (FileNotFoundError, EOFError, json.JSONDecodeError):
        return AddressBook()

def save_address_book(book, filename):
    data = {}
    for name, record in book.data.items():
        data[name] = {
            'phones': [phone.value for phone in record.phones],
        }
        # Save birthday if present
        if record.birthday:
            data[name]['birthday'] = record.birthday.value.strftime('%d.%m.%Y')
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def main():
    '''
    Головна функція, де знаходиться логіка бота
    '''
    path = "address_book/address_book.json"
    book = load_address_book(path)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")  # Отримання команди від користувача
        command, *args = parse_input(user_input)  # Парсинг команди

        # Перевірка команд та відповідна дія
        if command == "hello":
            print(hello_command())
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(show_birthdays_next_week(book))
        elif command == "search":
            print(search_contact(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command in ["close", "exit"]:
            save_address_book(book, path)
            print("Good bye!")
            break  # Вихід
        else:
            print(f"Command '{command}' not recognized")

# Точка входу
if __name__ == "__main__":
    main()
