from classes import Record, AddressBook


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

    return "Contact added."


@input_error
def change_contact(args, book):
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

    contact_details = [str(record) for record in book.data.values()]

    separator = '-' * 10
    return f'\n{separator}\n'.join(contact_details)

@input_error
def add_address(args, book):
    if len(args) < 2:
        return "Missing arguments for adding address. Please provide a name and an address."

    name, address = args[0], ' '.join(args[1:])
    record = book.find(name)
    if record:
        record.add_address(address)
        return "Address added."
    else:
        return "Contact not found."

@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "Email added."
    else:
        return "Contact not found."
    
@input_error
def search_contact(args, book):
    search_string = args[0]
    matching_records = book.search(search_string)
    if matching_records:
        result = []
        for record in matching_records:
            info = f"Name: {record.name.value}"
            if record.phones:
                phones_info = "; ".join(phone.value for phone in record.phones)
                info += f"\nPhones: {phones_info}"
            if record.emails:
                emails_info = "; ".join(email.value for email in record.emails)
                info += f"\nEmails: {emails_info}"
            if record.birthday:
                info += f"\nBirthday: {record.birthday.value.strftime('%d.%m.%Y')}"
            result.append(info)

        return "".join(result)

@input_error
def change_address(args, book):
    if len(args) < 2:
        return "Missing arguments for changing address. Please provide a name and an address."

    name, address = args[0], ' '.join(args[1:])
    record = book.find(name)
    if record:
        record.address.value = address
        return "Address changed."
    else:
        return "Contact not found."

@input_error
def change_email(args, book):
    name, new_email = args
    record = book.find(name)
    if record:
        result = record.edit_email(new_email)
        return result
    else:
        return "Contact not found."


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added."
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    [name] = args
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime('%d.%m.%Y')
    else:
        return "No birthday found for this contact."


@input_error
def change_birthday(args, book):
    name, new_birthday = args
    record = book.find(name)
    if record:
        result = record.edit_birthday(new_birthday)
        return result
    else:
        return "Contact not found."


@input_error
def show_birthdays_in_x_days(args, book):
    '''
    Виводить список контактів з днями народження через вказану кількість днів
    '''
    try:
        days = int(args[0])
        if days < 0:
            return "Please provide a positive number of days."
    except ValueError:
        return "Invalid number of days."

    birthdays_in_x_days = book.get_birthdays_in_x_days(days)
    if not birthdays_in_x_days:
        return f"No birthdays in {days} days."

    response = []
    for day, names_and_dates in birthdays_in_x_days.items():
        birthday_strings = [
            f'{name} ({date.strftime("%d.%m.%Y")})' for name, date in names_and_dates]
        day_birthdays = ', '.join(birthday_strings)
        response.append(f"{day}: {day_birthdays}")

    return "\n".join(response)


def hello_command():
    return "How can I help you?"

@input_error
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

def test_address_book_commands():
    path = "address_book/address_book.json"
    book = AddressBook()
    book.load_address_book(path)
    print("Welcome to the address book assistant testing!")

    test_cases = [
        ("hello", "How can I help you?"),
        ("add John 1234567890", "Contact added."),
        ("add Alice 9876543210", "Contact added."),
        ("phone John", "1234567890"),
        ("all", "Name: John\nPhones: 1234567890\n---\nName: Alice Smith\nPhones: 9876543210"),
        ("change-phone John 9999999999", "Contact updated."),
        ("search Alice", "Name: Alice\nPhones: 9876543210"),
        ("delete John", "Contact deleted."),
        ("add-address Alice 123 Main St", "Address added."),
        ("add-email Alice alice@example.com", "Email added."),
        ("change-address Alice 456 Elm St", "Address changed."),
        ("change-email Alice newemail@example.com", "Email changed."),
        ("add-birthday Alice 15.07.1990", "Birthday added."),
        ("show-birthday Alice", "15.07.1990"),
        ("birthdays-in-x-days 30", "No birthdays in 30 days."),
        ("exit", "Good bye!"),
    ]

    for command, expected_output in test_cases:
        user_input = command
        command, *args = parse_input(user_input)
        result = None

        if command == "hello":
            result = hello_command()
        elif command == "add":
            result = add_contact(args, book)
        elif command == "change-phone":
            result = change_contact(args, book)
        elif command == "phone":
            result = show_phone(args, book)
        elif command == "all":
            result = show_all(book)
        elif command == "delete":
            result = delete_contact(args, book)
        elif command == "search":
            result = search_contact(args, book)
        elif command == "add-address":
            result = add_address(args, book)
        elif command == "add-email":
            result = add_email(args, book)
        elif command == "change-address":
            result = change_address(args, book)
        elif command == "change-email":
            result = change_email(args, book)
        elif command == "add-birthday":
            result = add_birthday(args, book)
        elif command == "show-birthday":
            result = show_birthday(args, book)
        elif command == "birthdays-in-x-days":
            result = show_birthdays_in_x_days(args, book)
        elif command in ["close", "exit"]:
            book.save_address_book(path)
            result = "Good bye!"

        if result == expected_output:
            print(f"Test Passed: '{command}' - Expected: '{expected_output}'")
        else:
            print(f"Test Failed: '{command}' - Expected: '{expected_output}', Actual: '{result}'")


def main():
    '''
    Головна функція, де знаходиться логіка бота
    '''
    path = "address_book/address_book.json"
    book = AddressBook()
    book.load_address_book(path)
    print("Welcome to the assistant bot!")

    while True:
        # Отримання команди від користувача
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)  # Парсинг команди

        # Перевірка команд та відповідна дія
        if command == "hello":
            print(hello_command())
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change-phone":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "change-birthday":
            print(change_birthday(args, book))
        elif command == "birthdays-in-x-days":
            print(show_birthdays_in_x_days(args, book))
        elif command == "search":
            print(search_contact(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "change-address":
            print(change_address(args, book))
        elif command == "change-email":
            print(change_email(args, book))
        elif command in ["close", "exit"]:
            book.save_address_book(path)
            print("Good bye!")
            break  # Вихід
        else:
            print(f"Command '{command}' not recognized")


# Точка входу
if __name__ == "__main__":
    main()
