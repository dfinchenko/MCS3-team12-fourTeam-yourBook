from datetime import datetime, timedelta
import calendar
from collections import defaultdict
from collections import UserDict
import json
import os
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Address(Field):
    def __init__(self, address):
        super().__init__(address)


class Email(Field):
    def __init__(self, email):
        # Регулярний вираз для парсингу email
        pattern = r'[a-zA-Z][a-zA-Z0-9_.]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,}'
        if not re.findall(pattern, email):
            raise ValueError("Email is not validation")
        super().__init__(email)


class Phone(Field):
    def __init__(self, phone):
        cleaned_number = re.sub(r'[^0-9]', '', phone)
        if not (len(cleaned_number) == 10 and cleaned_number.isdigit()):
            raise ValueError("Phone number must be 10 digits long")

        super().__init__(cleaned_number)


class Birthday(Field):
    def __init__(self, birthday):
        try:
            date = datetime.strptime(birthday, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Birthday must be in the format DD.MM.YYYY")

        super().__init__(date)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.address = None
        self.email = None
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone_number):
        '''
        Додавання телефонів
        '''
        phone = Phone(phone_number)
        self.phones.append(phone)

    def edit_phone(self, old_number, new_number):
        '''
        Редагування телефонів
        '''
        phone = Phone(new_number)
        phone = self.find_phone(old_number)
        if phone:
            phone.value = new_number
            return True
        return False

    def find_phone(self, phone_number):
        '''
        Пошук телефону
        '''
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def search(self, search_string):
        search_string = search_string.lower()
        matching_records = []
        for record in self.data.values():
            if (
                search_string in record.name.value.lower()
                or search_string in record.birthday.value.strftime("%d.%m.%Y")
                or any(search_string in phone.value for phone in record.phones)
                or any(search_string in email.value for email in record.emails)
            ):
                matching_records.append(record)
        return matching_records

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        details = [f"Contact name: {self.name.value}"]
        if self.phones:
            details.append(f"Phones: {', '.join(map(str, self.phones))}")
        if self.address:
            details.append(f"Address: {self.address.value}")
        if self.email:
            details.append(f"Email: {self.email.value}")
        if self.birthday:
            details.append(
                f"Birthday: {self.birthday.value.strftime('%d.%m.%Y')}")
        return '\n'.join(details)


class AddressBook(UserDict):
    def add_record(self, record):
        '''
        Додавання записів
        '''
        if isinstance(record, Record):
            self.data[record.name.value] = record

    def find(self, name):
        '''
        Пошук записів за іменем
        '''
        return self.data.get(name)

    def search(self, search_string):
        search_string = search_string.lower()
        matching_records = []
        for record in self.data.values():
            if (
                search_string in record.name.value.lower()
                or search_string in record.birthday.value.strftime("%d.%m.%Y")
                or any(search_string in phone.value for phone in record.phones)
            ):
                matching_records.append(record)
        return matching_records

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_in_x_days(self, days):
        today = datetime.today().date()
        target_date = today + timedelta(days=days)
        birthdays = defaultdict(list)

        for name, record in self.data.items():
            if record.birthday:  # день народження
                birthday_date = record.birthday.value.date()  # отримуємо об'єкт date

                # Створюємо об'єкт datetime дня народження цього року
                birthday_this_year = birthday_date.replace(year=today.year)

                # Якщо день народження вже був цього року, тоді перевіряємо наступний рік
                if birthday_this_year < today:
                    birthday_this_year = birthday_date.replace(
                        year=today.year + 1)

                # Чи день народження через x днів
                if today <= birthday_this_year <= target_date:
                    day_of_week = birthday_this_year.weekday()
                    day_name = calendar.day_name[day_of_week]

                    # Якщо припадає на вихідні, тоді переносимо на понеділок
                    if day_of_week in [5, 6]:
                        day_name = 'Monday'

                    birthdays[day_name].append(
                        (record.name.value, birthday_this_year))

        return birthdays

    def load_address_book(self, path):
        if not os.path.isfile(path):
            self.data = {}
            return

        with open(path, 'r', encoding='utf-8') as file:
            records_list = json.load(file)

            for record_dict in records_list:
                name = record_dict['name']
                address = record_dict.get('address')
                email = record_dict.get('email')
                birthday = record_dict.get('birthday')
                phones = record_dict.get('phones', [])

                record = Record(name, birthday=birthday)
                if address:
                    record.add_address(address)
                if email:
                    record.add_email(email)
                for phone_number in phones:
                    record.add_phone(phone_number)

                self.add_record(record)

    def save_address_book(self, filename):
        '''
        Зберігання адресної книги в файл
        '''
        with open(filename, 'w') as file:
            records_list = []
            for record in self.data.values():
                record_dict = {
                    'name': record.name.value,
                    'phones': [phone.value for phone in record.phones],
                    'birthday': record.birthday.value.strftime('%d.%m.%Y') if record.birthday else None,
                    'address': record.address.value if record.address else None,
                    'email': record.email.value if record.email else None,
                }
                records_list.append(record_dict)

            json.dump(records_list, file, ensure_ascii=False)
