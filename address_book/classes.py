from datetime import datetime, timedelta
import calendar
from collections import defaultdict
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Phone number must be 10 digits long")
        
        super().__init__(phone)


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
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


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

    def get_birthdays_per_week(self):
        '''
        Дні народження на наступному тижні
        '''
        today = datetime.today().date()
        week_ahead = today + timedelta(days=7)
        birthdays = defaultdict(list)

        for name, record in self.data.items():
            if record.birthday:  # день народження
                birthday_date = record.birthday.value.date()  # отримуємо об'єкт date

                # Створюємо об'єкт datetime дня народження цього року
                birthday_this_year = birthday_date.replace(year=today.year)

                # Якщо день народження вже був цього року, тоді перевіряємо наступний рік
                if birthday_this_year < today:
                    birthday_this_year = birthday_date.replace(year=today.year + 1)

                # Чи день народження наступного тижня
                if today <= birthday_this_year <= week_ahead:
                    day_of_week = birthday_this_year.weekday()
                    day_name = calendar.day_name[day_of_week]

                    # Якщо припадає на вихідні, тоді переносимо на понеділок
                    if day_of_week in [5, 6]:
                        day_name = 'Monday'

                    birthdays[day_name].append(record.name.value)
        
        return birthdays
    