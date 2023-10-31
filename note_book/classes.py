from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Title(Field):
    def __init__(self, title):
        super().__init__(title)

class Description(Field):
    def __init__(self, description):
        super().__init__(description)

class Note:
    def __init__(self, title, description):
        self.title = Title(title)
        self.description = Description(description)

    def __str__(self):
        return f"Note title: {self.title.value}, Description: {self.description.value}"

class NotesBook(UserDict):
    def add_note(self, note):
        if isinstance(note, Note):
            self.data[note.title.value] = note

    def find(self, title):
        return self.data.get(title)

    def delete(self, title):
        if title in self.data:
            del self.data[title]