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
            raise ValueError("Email is not valid")
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


class Title(Field):
    def __init__(self, title):
        super().__init__(title)


class Description(Field):
    def __init__(self, description):
        super().__init__(description)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.address = None
        self.email = None
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def edit_phone(self, old_number, new_number):
        phone = Phone(new_number)
        phone = self.find_phone(old_number)
        if phone:
            phone.value = new_number
            return True
        return False

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, new_email):
        if self.email:
            try:
                new_email = Email(new_email)
                self.email.value = new_email.value
                return "Email changed."
            except ValueError as e:
                return str(e)
        return "Email not found."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_birthday(self, new_birthday):
        try:
            new_birthday = Birthday(new_birthday)
            self.birthday = new_birthday
            return "Birthday changed."
        except ValueError as e:
            return str(e)

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
    

class Note:
    def __init__(self, title, description):
        self.title = Title(title)
        self.description = Description(description)
    
    def __str__(self):
        details = [f"Note title: {self.title.value}, Description: {self.description.value}"]
    
        return '\n'.join(details)