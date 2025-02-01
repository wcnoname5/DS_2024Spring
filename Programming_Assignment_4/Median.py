
##Important! You shouldn't use statistics library! ("import statistics" is not allowed)

import math
class MinHeap: #Please store and implement MinHeap data structure with an array
    def __init__(self):
        self.array = []
        self.size = 0
    def getSize(self):
        return self.size
    def insert(self, item): #insert new item
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
    ### input: a value ###
    ### You need not return or print anything with this function. ###
    
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
    ### You need not return or print anything with this function. ###

    def showMinHeap(self):  #Show MinHeap with array
        return self.array

class MaxHeap: #Please store and implement MinHeap data structure with an array
    def __init__(self):
        self.array = []
        self.size = 0
    def getSize(self):
        return self.size
    def insert(self, item): #insert new item
        self.array.append(item)
        id = self.size
        self.size+=1 # update size
        '''prelocate up'''
        while id>0:
            if id%2 == 1: # current node is left child
               pid = (id-1)//2
            else: pid = (id-2)//2
            
            if self.array[id] > self.array[pid]: 
                tp = self.array[pid]
                self.array[pid] = self.array[id]
                self.array[id] = tp
                id = pid
            else:
                break 
    ### TODO ###
    ### input: a value ###
    ### You need not return or print anything with this function. ###

    def peek(self):    #Find Maximum item
        if self.size == 0:
            return
        else:
            return self.array[0]
    def removeMax(self):   #remove Maximum item
        '''swap and remove max'''
        self.array[0] = self.array[-1]
        self.array.pop()
        self.size-=1
        '''prelocate down'''
        id=0
        while (id*2)+1 < self.size: # at least has left child
            # Go left: curr*2+1, Go right: curr*2+2
            if (id*2)+3 > self.size: # has left child only
                cid = (id*2)+1
            else:  # choose max{left, right} child
                if self.array[(id*2)+1] > self.array[(id*2)+2]:
                    cid = (id*2)+1
                else: cid = (id*2)+2
            if self.array[id] < self.array[cid]: # maintain curr > child
                tp = self.array[cid]
                self.array[cid] = self.array[id]
                self.array[id] = tp
                id = cid
            else:
                break
    ### You need not return or print anything with this function. ###

    def showMaxHeap(self):   #Show MaxHeap with array
        return self.array

class FindMedian: 
    def __init__(self):
        self.largeHalf = MinHeap() # all vlaues >= median
        self.smallHalf = MaxHeap() # all values <= median
        self.size = 0 
        self.med = math.inf # median 

    def AddNewValues(self, NewValues):  # Add NewValues(a list of items) into your data structure
        '''O(logn) for single item'''
        for item in NewValues:    
            if self.size%2==0: # even
                if item >= self.med: 
                    self.largeHalf.insert(item)
                    self.smallHalf.insert(self.largeHalf.peek())
                else:
                    self.smallHalf.insert(item)
                    self.largeHalf.insert(self.smallHalf.peek())
            else: # odd
                if item >= self.med:
                    self.largeHalf.insert(item)
                    self.largeHalf.removeMin()
                    # problems in removeMin
                else:
                    self.smallHalf.insert(item)
                    self.smallHalf.removeMax()
                    pass
            # print(f'l_size:{self.smallHalf.size}, r_size:{self.largeHalf.size}')
            self.size+=1
            self.med = (self.smallHalf.peek() + self.largeHalf.peek())/2
            # print(f'insert({item}), left: {self.smallHalf.showMaxHeap()}, right:{self.largeHalf.showMinHeap()}; Median: {self.med}, size: {self.size}')
 
    def ShowMedian(self):  # Show Median of your data structure
    ### You need not print anything but "return Median". ###
    ### The return value should always be a float number. ###
        '''O(1)'''
        if self.size==0:
            print("The List is Empty")
            return(math.inf) # median not exist in empty list
        else:
            return(self.med)

    def RemoveMedian(self): # Remove median
    ### If there are even number of elements, remove the larger one ###
    ### For example, if array=[1, 2, 3, 5], remove 3 ###
        '''O(logn)'''
        if self.size%2==0: # even
            self.largeHalf.removeMin()
            self.largeHalf.insert(self.smallHalf.peek())
        else: # odd
            self.largeHalf.removeMin()
            self.smallHalf.removeMax()
        self.size-=1
        if self.size==0: # empty
            self.med = math.inf 
        else: 
            self.med = (self.smallHalf.peek() + self.largeHalf.peek())/2 