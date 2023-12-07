import csv
from pathlib import Path

def read_books_data():
    filename = 'books'
    filepath = Path('databases') / f'{filename}.csv'
    fields = []
    data = []

    if not filepath.exists():
        return []

    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        fields = header
        for row in reader:
            data.append(dict(zip(fields, row)))

    return data

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

for key in [book['title'] for book in read_books_data()]:
    bookTrie.insert(key)

print(f'hasil : {bookTrie.autocomplete("Cla")}')