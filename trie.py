class Node:
    def __init__(self, value = 1):
        self.value = value
        self.pointers = {}

    def set_pointer(self, key, node):
        self.pointers[key] = node 

class Trie:
    def __init__(self):
        self.root = Node()
        #self.next_value = 1

    def add_word(self, word):
        node = self.root
        char_index = 0
        #while there is a pointer from the current node
        # under the current character. go down the trie
        while char_index < len(word)  and  word[char_index] in node.pointers:
            node = node.pointers[word[char_index]]
            char_index +=1
            node.value +=1
        # if we didn't make it through the entrie word
        while char_index < len(word):
        # make new nodes and hook them to previous ones
            new_node = Node()
            node.set_pointer(word[char_index], new_node)
            node = node.pointers[word[char_index]]
            char_index += 1
            


    def find_words(self, word):
        node = self.root
        char_index = 0
        while char_index < len(word) and word[char_index] in node.pointers:
            node = node.pointers[word[char_index]]
            char_index +=1
        if char_index != len(word):
            return 0
        else:
            return node.value


if __name__ == "__main__":
    trie = Trie()
    trie.add_word("hackerrank")
    trie.add_word("hack")
    print(trie.find_words("hac"))
    print(trie.find_words("hak"))



'''
    def find_values(self, node):
        current_value = 0
        more_value = 0
        for letter in node.pointers:
            if node.pointers[letter].value is not None:
                current_value += 1
            more_value += self.find_values(node.pointers[letter])
        return more_value + current_value 
'''