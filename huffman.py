# DATA STRUCTURES NANODEGREE
## Project 1 - Show me the data satructures
### Question 3 - Huffman Coding

# Author: Mattia Pennacchietti


##### IMPLEMENTATION ######


## UTILITY FUNCTION: Count characters frequencies within a string 

def str_to_freq(string):
    '''
    Input: string
    Output: list of tuples with (character,frequency) in frequency ascending order 
    '''
    out = []
    lst = list(set(list(string)))
    str_to_lst = list(string)
    for char in lst:
        out.append((char, str_to_lst.count(char)))
    return sorted(out, key = lambda char_freq: char_freq[1])


## BINARY TREE CLASS 

class Node(object):
        
    def __init__(self, char = None, freq = None, code = None):
        self.char = char
        self.freq = freq
        self.code = code
        self.left = None
        self.right = None
        
    def set_value(self,value):
        self.char = value
        
    def get_value(self):
        return self.char
        
    def set_left_child(self,node):
        self.left = node
        
    def set_right_child(self, node):
        self.right = node
        
    def get_left_child(self):
        return self.left
    
    def get_right_child(self):
        return self.right
    
    
class Tree():
    def __init__(self,value=None):
        self.root = Node(value)
        self.leaves_num = None
        self.depth = None
        
    def get_root(self):
        return self.root


def tree_find_code(tree, char):
    
    init_code = ''
    out = ''
    
    def traverse(node, char, code):
        
        if node.code:
            code += node.code

        # Check if I am at the end of a branch
        if not(node.left) and not(node.right):
            if node.get_value() == char:
                nonlocal out
                out = code
                return 
            else:
                return 

        # traverse left subtree
        traverse(node.get_left_child(), char, code)
        # traverse right subtree
        traverse(node.get_right_child(), char, code)
        
        return out

    return traverse(tree.get_root(), char, init_code)


def tree_find_leaves(tree):
    
    init_code = ''
    out = {}
    
    def traverse(node, code):
        
        if node.code:
            code += node.code

        # Check if I am at the end of a branch
        if not(node.left) and not(node.right):
            nonlocal out
            out[code] = node.char
            return 
       
        # traverse left subtree
        traverse(node.get_left_child(),code)
        # traverse right subtree
        traverse(node.get_right_child(),code)
        
        return out

    return traverse(tree.get_root(), init_code)

	
## ENCODING FUNCTION 

def huffman_encoding(data):
    
    '''
    Input: string
    Output: Huffman tree and encoded data
    '''
    
    char_freq = str_to_freq(data)
    tree = []
    huf_tree = Tree()
    char_code = dict()
    encoded = ''
    
    while len(char_freq) > 1:
        
        # Check whether left leaf is node or tuple
        if type(char_freq[0]) == tuple:
            left = Node(char_freq[0][0],char_freq[0][1],'0')
        elif type(char_freq[0]) == Node:
            left = char_freq[0]
            left.code = '0'

        # Check whether right leaf is node or tuple
        if type(char_freq[1]) == tuple:
            right = Node(char_freq[1][0],char_freq[1][1],'1')    
        elif type(char_freq[1]) == Node:
            right = char_freq[1]
            right.code = '1'

        tmp_root = Node(left.char+right.char, left.freq+right.freq)
        tmp_root.left = left
        tmp_root.right = right

        if type(char_freq[0]) == Node or type(char_freq[1]) == Node:
            huf_tree.root = tmp_root

        # Delete left and right leaves from the list of tuples, and append the new node
        char_freq = char_freq[2:]
        char_freq.append(tmp_root)

        # Re-sort the list of tuples to keep ascending order
        char_freq = sorted(char_freq, key = lambda freq: freq[1] if type(freq) == tuple else freq.freq)
        #print(char_freq)
        
    # Find the code for each character
    for char in set(list(data)):
        code = tree_find_code(huf_tree,char)
        char_code[char] = code
    
    encoded = [char_code[character] for character in data]
    
    return ''.join(encoded), huf_tree


## DENCODING FUNCTION 

def huffman_decoding(encoded_data,tree):
    
    '''
    Input:  Compressed data, Huffman tree return by the encoding function
    Output: decoded data
    '''
    
    dict_codes = tree_find_leaves(tree)
    input_data = ''
    
    cur = ''
    for character in encoded_data:
        cur += character
        if cur in list(dict_codes.keys()):
            input_data += dict_codes[cur]
            cur = ''
        
    return input_data


## TESTING

import unittest
import sys

# We will test whether the encoding mechanism works
# and whether the data is actually compressed
class HuffmanTreeTest(unittest.TestCase):


	def setUp(self) -> None:
		self.test_sentences = ['Hello World', 'The book is on the table', 'What a great sentence!']
		self.encoded_data = None
		self.decoded_data = None
		self.tree = None


	def test_decoding(self):
		for sentence in self.test_sentences:
			self.encoded_data, self.tree = huffman_encoding(sentence)
			self.decoded_data = huffman_decoding(self.encoded_data, self.tree)
			self.assertEqual(self.decoded_data, sentence)

	def test_compression(self):
		for sentence in self.test_sentences:
			self.encoded_data, self.tree = huffman_encoding(sentence)
			self.decoded_data = huffman_decoding(self.encoded_data, self.tree)
			self.assertTrue(sys.getsizeof(int(self.encoded_data)) <\
							sys.getsizeof(self.decoded_data))


if __name__ == '__main__':
	unittest.main()

