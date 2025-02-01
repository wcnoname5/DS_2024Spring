import math
import json
import time
import argparse

# --- TODO START --- #
# You can define any class or function
# You can import any python standard library : https://docs.python.org/3/library/
# However, you are not allowed to import any libraries other than python standard library, (such as numpy)
# --- TODO END --- #

class MinHeap: 
    def __init__(self) -> None:
        self.array = []
        self.size = 0
        pass
    def insert(self, item):
        self.array.append(item)
        id = self.size
        self.size+=1 
        '''prelocate up'''
        while id>0:
            if id%2 == 1: # current node is left child
               pid = (id-1)//2
            else: pid = (id-2)//2
            
            if self.array[id] < self.array[pid]: #curr < parent 
                tp = self.array[pid]
                self.array[pid] = self.array[id]
                self.array[id] = tp
                id = pid
            else:
                break

    def peek(self):  #Find Minimum item
        if self.size == 0:
            return
        else:
            return self.array[0]
    
    def removeMin(self):
        '''swap and remove min'''
        self.array[0] = self.array[-1]
        self.array.pop()
        self.size-=1
        '''prelocate down'''
        id=0
        while (id*2)+1 < self.size: # at least has left child 
            # Go left: curr*2+1, Go right: curr*2+2
            if (id*2)+3 > self.size: # has left child only
                cid = (id*2)+1
            else: # choose min{left, right} child
                if self.array[(id*2)+1] < self.array[(id*2)+2]:
                    cid = (id*2)+1
                else: cid = (id*2)+2
            if self.array[id] > self.array[cid]: # maintain curr < child
                tp = self.array[cid]
                self.array[cid] = self.array[id]
                self.array[id] = tp
                id = cid
            else:
                break 

    def showMinHeap(self):  #Show MinHeap with array
        return self.array  

def findContMaxSubarray(array, k): # Too Slow! (O(n^2*logk))
    minH = MinHeap() 
    for start in range(len(array)):
        curr_sum = 0
        for end in range(start, len(array)):
            curr_sum += array[end]
            if minH.size < k:
                minH.insert(curr_sum)
            elif minH.peek() < curr_sum: # max k items
                minH.insert(curr_sum)
                minH.removeMin()
            else:pass
    ans = minH.showMinHeap()
    ans.sort(reverse=True)
    return(ans)

def solution(json_input):
    '''O(nk log n)'''
    # --- TODO START --- #
    array = json_input['array']
    k = json_input['topk'] 
    json_sum = findContMaxSubarray(array, k)
    # --- TODO END --- #
    return json_sum

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='input_1.json')
    parser.add_argument('--output', default='output_1.json')
    args = parser.parse_args()
    json_input = json.load(open(args.input, "r"))
    t1 = time.time()
    json_output = solution(json_input)
    t2 = time.time()
    print(json_output)
    json.dump(json_output, open(args.output, "w"))
    print("runtime of %s : %s" % (args.input, t2 - t1))

