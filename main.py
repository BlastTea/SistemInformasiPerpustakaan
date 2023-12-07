import os
import json
import csv
from pathlib import Path

class SharedPreferences:
    def __init__(self, filename='shared_preferences.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=2)

    def get(self, key, default=None):
        key_without_prefix = key.replace('library.', '')
        return self.data.get(key_without_prefix, default)

    def set(self, key, value):
        full_key = f'library.{key}'
        self.data[full_key] = value
        self.save_data()

class Model:
    def __init__(self, filename):
        self.filename = filename
        self.fields = []
        self.data = []

    def load_data(self):
        filepath = Path('databases') / f'{self.filename}.csv'
        if not filepath.exists():
            return

        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.fields = header
            for row in reader:
                self.data.append(row)

    def save_data(self):
        filepath = Path('databases') / f'{self.filename}.csv'
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.fields)
            writer.writerows(self.data)

    def create(self, data):
        self.load_data()
        self.data.append(data)
        self.save_data()

    def read(self) -> list[dict]:
        self.load_data()
        records = []
        for row in self.data:
            record = dict(zip(self.fields, row))
            records.append(record)
        return records

    def update(self, identifier, updated_data):
        self.load_data()
        index = self.get_index_by_identifier(identifier)
        if index != -1:
            self.data[index] = updated_data
            self.save_data()

    def delete(self, identifier):
        self.load_data()
        index = self.get_index_by_identifier(identifier)
        if index != -1:
            del self.data[index]
            self.save_data()

    def get_index_by_identifier(self, identifier):
        index = -1
        for i, row in enumerate(self.data):
            if row[0] == identifier:
                index = i
                break
        return index

class DbHelper:
    def __init__(self):
        self.books_model = Model('books')
        self.members_model = Model('members')
        self.loans_model = Model('loans')
        self.shared_prefs = SharedPreferences()

    def get_next_id(self, key):
        last_id = self.shared_prefs.get(key, 0)
        next_id = last_id + 1
        self.shared_prefs.set(key, next_id)
        return next_id

    def add_book(self, title, writer, publisher, publication_year):
        next_id = self.get_next_id('library.last_books_id')
        book_data = [str(next_id), title, writer, publisher, str(publication_year)]
        self.books_model.create(book_data)

    def add_member(self, name, address, phone_number):
        next_id = self.get_next_id('library.last_members_id')
        member_data = [str(next_id), name, address, phone_number]
        self.members_model.create(member_data)

    def add_loan(self, id_member, id_book, loan_date, return_date):
        next_id = self.get_next_id('library.last_loans_id')
        loan_data = [str(next_id), str(id_member), str(id_book), loan_date, return_date]
        self.loans_model.create(loan_data)

    def get_books(self):
        return self.books_model.read()

    def get_members(self):
        return self.members_model.read()

    def get_loans(self):
        return self.loans_model.read()

    def update_book(self, id_book, updated_data):
        self.books_model.update(str(id_book), updated_data)

    def update_member(self, id_member, updated_data):
        self.members_model.update(str(id_member), updated_data)

    def update_loan(self, id_loan, updated_data):
        self.loans_model.update(str(id_loan), updated_data)

    def delete_book(self, id_book):
        self.books_model.delete(str(id_book))

    def delete_member(self, id_member):
        self.members_model.delete(str(id_member))

    def delete_loan(self, id_loan):
        self.loans_model.delete(str(id_loan))

class TrieNode:
    def __init__(self):
        self.children = [None]*256

        self.isEndWord = False

class Trie:
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
        return TrieNode()
    
    def _charToIndex(self, ch):
        return ord(ch)
    
    def insert(self, key):
        pCrawl = self.root

        for level in range(len(key)):
            index = self._charToIndex(key[level])

            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()

            pCrawl = pCrawl.children[index]
        
        pCrawl.isEndWord = True

    def search(self, key):
        pCrawl = self.root

        for level in range(len(key)):
            index = self._charToIndex(key[level])

            if not pCrawl.children[index]:
                return False
            
            pCrawl = pCrawl.children[index]

        return pCrawl.isEndWord
    
    def autocomplete(self, prefix):
        suggestions = []
        pCrawl = self.root

        for level in range(len(prefix)):
            index = self._charToIndex(prefix[level])

            if not pCrawl.children[index]:
                return suggestions

            pCrawl = pCrawl.children[index]

        self._collect_suggestions(pCrawl, prefix, suggestions)
        return suggestions

    def _collect_suggestions(self, node, prefix, suggestions):
        if node.isEndWord:
            suggestions.append(prefix)

        for i in range(256):
            if node.children[i]:
                self._collect_suggestions(node.children[i], prefix + chr(i), suggestions)

dbHelper = DbHelper()
books = dbHelper.get_books()
    
keys = [book['title'] for book in books]
output = ['Not present in the trie', 'Present in the trie']

trie = Trie()

for key in keys:
    trie.insert(key)

for key in ['Laskar Pelangi', 'Halo']:
    print(f'{key} = {output[trie.search(key)]}')

print(f'Laskar : {trie.autocomplete("Laskar")}')
