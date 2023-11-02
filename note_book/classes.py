from collections import UserDict
import json
import os

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
    
    def search(self, term):
        matches = []
        for note in self.data.values():
            if term.lower() in note.title.value.lower() or term.lower() in note.description.value.lower():
                matches.append(note)
        return matches

    def delete(self, title):
        if title in self.data:
            del self.data[title]

    def load_notes(self, filename):
        if not os.path.isfile(filename):
            self.data = {}
            return

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for key, note_data in data.items():
                note = Note(note_data['title'], note_data['description'])
                self.add_note(note)

    def save_notes(self, filename):
        data = {key: {'title': note.title.value, 'description': note.description.value} for key, note in self.data.items()}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)