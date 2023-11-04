from classes import Record
from datetime import datetime, timedelta
import calendar
from collections import defaultdict
from collections import UserDict
import json
import os


class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def search_contacts(self, search_string):
        search_string = search_string.lower()
        matching_records = []
        for record in self.data.values():
            if (
                record.name and search_string in record.name.value.lower()
                or (record.birthday and search_string in record.birthday.value.strftime("%d.%m.%Y"))
            ):
                matching_records.append(record)

            if record.phones:
                for phone in record.phones:
                    if search_string in phone.value:
                        matching_records.append(record)

            if record.email and search_string in record.email.value:
                matching_records.append(record)

            if record.address and search_string in record.address.value:
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
