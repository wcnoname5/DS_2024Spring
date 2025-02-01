import argparse

class Node():
    #########################
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # It's important and repeat three times
    #########################
    def __init__(self, key):
        self.value = key
        self.left_child = None
        self.right_child = None
    def __repr__(self):
        return str(self.value)

class BS_tree():
    def __init__(self):
        self.root = None
    def inorder(self, output, **kwargs):      # print the in-order traversal of binary search tree
        node = kwargs.get('node', self.root)
        if node == None:
            pass
        else:
            self.inorder(output, node = node.left_child)
            output.write(f'{node.value} ')
            self.inorder(output, node = node.right_child)
            if node == self.root:
                output.write('\n')

    def preorder(self, output, **kwargs):     # print the pre-order traversal of binary search tree
        node = kwargs.get('node', self.root)
        if node == None:
            pass
        else:
            output.write(f'{node.value} ')
            self.preorder(output, node = node.left_child)
            self.preorder(output, node = node.right_child)
            if node == self.root:
                output.write('\n')

    def postorder(self, output, **kwargs):    # print the post-order traversal of binary search tree
        node = kwargs.get('node', self.root)
        if node == None:
            pass
        else:
            self.postorder(output, node = node.left_child)
            self.postorder(output, node = node.right_child)
            output.write(f'{node.value} ')
            if node == self.root:
                output.write('\n')

    def find_max(self, output):     # print the maximum number in binary search tree
        curr = self.root # current node
        last = curr
        # Binary Search
        while curr != None:
            last = curr
            curr = curr.right_child                
        # print(last.value)
        output.write(f'{last.value}\n')
        
    def find_min(self, output):     # print the minimum number in binary search tree
        curr = self.root # current node
        last = curr
        # Binary Search
        while curr != None:
            last = curr
            curr = curr.left_child                
        # print(last.value)
        output.write(f'{last.value}\n')

    def insert(self, key):          # insert one node
        curr = self.root # current node
        if curr == None: # Empty tree
            self.root = Node(key)
        else: # Binary Search
            while curr != None:
                last = curr
                if  key > curr.value:
                    curr = curr.right_child
                else:
                    curr = curr.left_child
            if key > last.value:
                last.right_child = Node(key)
            else:
                last.left_child = Node(key)
        print(f"Insert {key}")

    def delete(self, key):          # delete one node
        find = False
        curr = self.root # current node
        last = curr
        while curr != None:
            if key == curr.value: # key founded
                find = True
                break
            else:
                last = curr
                if  key > curr.value:
                    curr = curr.right_child
                elif key < curr.value:
                    curr = curr.left_child
        if find:
            #maintain BST
            if curr.left_child == None:
                new_node = curr.right_child
            elif curr.right_child == None:
                new_node = curr.left_child
            else: 
                new_node = curr.right_child
                prev_node = new_node
                while new_node.left_child != None:
                    prev_node = new_node
                    new_node = new_node.left_child
                if prev_node.value == new_node.value: # if smallest value is the right child of curr 
                    curr.right_child = new_node.right_child
                else:
                    prev_node.left_child = new_node.right_child
                # replace curr
                new_node.left_child = curr.left_child
                new_node.right_child = curr.right_child
            '''connect last to new_node'''           
            if key > last.value:
                last.right_child = new_node
            elif key < last.value:
                last.left_child = new_node     
            else: # delete root
                self.root = new_node
            print(f'delete {key}')
        else:
            print(f"{key} is not in BST.")

    def level(self, output, **kwargs):        # print the height of binary search tree(leaf = 0)
        node = kwargs.get('node', self.root)
        if node == None:
            return(-1)
        else:
            l = self.level(output, node=node.left_child)
            r = self.level(output, node=node.right_child)
            height = max(l,r)+1
            if node == self.root:
                output.write(f'{height}\n')
            return(height)

    def internalnode(self, output, **kwargs): # print the internal node in binary search tree from the smallest to the largest 
        node = kwargs.get('node', self.root)
        if node == None:
            pass
        elif (node.left_child == None) & (node.right_child == None):
            pass
        else:
            self.internalnode(output, node=node.left_child)
            output.write(f'{node.value} ')
            self.internalnode(output, node=node.right_child)
        if node == self.root:
            output.write('\n')

    def leafnode(self, output, **kwargs):     # print the leafnode in BST from left to right
        node = kwargs.get('node', self.root)
        if node == None:
            pass
        elif (node.left_child == None) & (node.right_child == None):
            output.write(f'{node.value} ')
        else:
            self.leafnode(output, node=node.left_child)
            self.leafnode(output, node=node.right_child)
        if node == self.root:
            output.write('\n')

    def main(self, input_path, output_path):
        #########################
        # DO NOT MODIFY CODES HERE
        # DO NOT MODIFY CODES HERE
        # DO NOT MODIFY CODES HERE
        # It's important and repeat three times
        #########################
        output = open(output_path, 'w', newline='')
        with open(input_path, 'r', newline='') as file_in:
            f = file_in.read().splitlines()
            for lines in f:
                if lines.startswith("insert"):
                    value_list = lines.split(' ')
                    for value in value_list[1:]:
                        self.insert(int(value))
                if lines.startswith('inorder'):
                    self.inorder(output)
                if lines.startswith('preorder'):
                    self.preorder(output)
                if lines.startswith('postorder'):
                    self.postorder(output)
                if lines.startswith('max'):
                    self.find_max(output)
                if lines.startswith('min'):
                    self.find_min(output)
                if lines.startswith('delete'):
                    value_list = lines.split(' ')
                    self.delete(int(value_list[1]))
                if lines.startswith('level'):
                    self.level(output)
                if lines.startswith('internalnode'):
                    self.internalnode(output)
                if lines.startswith('leafnode'):
                    self.leafnode(output)
        output.close()
if __name__ == '__main__' :
    #########################
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # It's important and repeat three times
    #########################
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default = './input_3.txt',help="Input file root.")
    parser.add_argument("--output", type=str, default = './output_3.txt',help="Output file root.")
    args = parser.parse_args()
    
    BS = BS_tree()
    BS.main(args.input, args.output)

    