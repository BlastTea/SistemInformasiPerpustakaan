import os
import pandas
import csv

def read_books_data():
    data = []
    with open('books.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def update_stock(books):
    with open('books.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, ['isbn','title','book_author','year_of_publication','publisher','stock'])
        
        writer.writeheader()
        writer.writerows(books)


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

bookTrie = Trie()

books = read_books_data()

for key in [book['title'] for book in books]:
    bookTrie.insert(key)

df = pandas.DataFrame(books)

page = 1

while True:
    os.system('cls')
    print(df.iloc[25 * (page - 1):25 * page])
    print('-' * 40)
    print('1. Halaman sebelumnya')
    print('2. Halaman selanjutnya')
    print('3. Pinjam buku')
    print('0. Exit')
    choice = int(input('Pilihan Anda : '))

    if (choice == 1):
        if (page > 1):
            page -= 1
    elif (choice == 2):
        page += 1
    elif (choice == 3):
        autocompleteResults = bookTrie.autocomplete(input("Mau pinjam buku apa? : "))
        if (len(autocompleteResults) == 0):
            input('Buku tidak ditemukan')
            continue
        print('-' * 40)
        for i in range(len(autocompleteResults)):
            print(f'{i + 1} {autocompleteResults[i]}')
        print('-' * 40)
        autocompleteChoice = int(input('Pilihan Anda : '))
        book = list(filter(lambda e: e['title'] == autocompleteResults[autocompleteChoice - 1], books))[0]
        print(f'isbn         : {book["isbn"]}')
        print(f'Judul        : {book["title"]}')
        print(f'Penulis      : {book["book_author"]}')
        print(f'Tahun terbit : {book["year_of_publication"]}')
        print(f'Penerbit     : {book["publisher"]}')
        print(f'Stok         : {book["stock"]}')
        print('-' * 40)
        isBorrowingBook = input(f'Pinjam buku "{book["title"]}"? (y/t) : ') == 'y'
        if isBorrowingBook is not True:
            continue
        amount = int(input('Jumlah buku yang akan dipinjam : '))
        stock = int(book['stock'])
        if stock - amount < 0:
            input('Stok sedang kosong!')
            continue
        book['stock'] = stock - amount
        index = books.index(book)
        books[index] = book
        update_stock(books)
    else:
        break


