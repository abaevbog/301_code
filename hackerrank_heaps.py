import math
import os
import random
import re
import sys


class heap:
    def __init__(self):
        self.HEAP = []

    def has_left_child(self,index):
        return index*2 + 1 <= len(self.HEAP)
    def has_right_child(self,index):
        return index*2 + 2 <= len(self.HEAP)
    def get_parent(self,index):
        return self.HEAP[int((index-1)/2)]
    def get_parents_index(self,index):
        return int((index-1)/2)
    def get_right_child(self,index):
        return index*2+2
    def get_left_child(self,index):
        return index*2+1
    def set_parent(self,index,val):
        self.HEAP[int((index-1)/2)] = val

    def loop_condition(self,current_index):
        raise Exception('This is never called')

    def loop_condition_remove(self,current_index):
        raise Exception("This is never called")


    def add_to_heap(self,new_number):
        self.HEAP.append(new_number)
        current_index = len(self.HEAP)-1
        # while the parent is greater than the child
        # swap parent and the child
        while self.loop_condition(current_index):
            free_value = self.get_parent(current_index)
            self.set_parent(current_index,self.HEAP[current_index])
            self.HEAP[current_index] = free_value
            current_index = self.get_parents_index(current_index)

    def heapify(self, current_index):
        raise Exception("This is never called")

    def remove_from_heap(self):
        result = self.HEAP[0]
        # put last el-t on top
        self.HEAP[0] = self.HEAP[len(self.HEAP)-1]
        # decrement the list
        self.HEAP = self.HEAP[:len(self.HEAP)-1]
        current_index = 0
        # fix the heap
        self.heapify(current_index)
        return result





class min_heap(heap):
    def __init__(self):
        super().__init__()
        self.HEAP = []

    def loop_condition(self,current_index):
        if current_index > 0:
            return self.get_parent(current_index) > self.HEAP[current_index]
        else:
            False
    #min-heapify
    def heapify(self, current_index):
        l = self.get_left_child(current_index)
        r = self.get_right_child(current_index)
        if l < len(self.HEAP) and self.HEAP[l] < self.HEAP[current_index]:
            smallest = l
        else:
            smallest = current_index
        if r < len(self.HEAP) and self.HEAP[r] < self.HEAP[smallest]:
            smallest = r
        if smallest != current_index:
            var = self.HEAP[current_index]
            self.HEAP[current_index] = self.HEAP[smallest]
            self.HEAP[smallest] = var
            self.heapify(smallest)


class max_heap(heap):
    def __init__(self):
        super().__init__()
        self.HEAP = []

    def loop_condition(self,current_index):
        if current_index > 0:
            return self.get_parent(current_index) < self.HEAP[current_index]
        else:
            False

    def heapify(self, current_index):
        l = self.get_left_child(current_index)
        r = self.get_right_child(current_index)
        if l < len(self.HEAP) and self.HEAP[l] > self.HEAP[current_index]:
            largest = l
        else:
            largest = current_index
        if r < len(self.HEAP) and self.HEAP[r] > self.HEAP[largest]:
            largest = r
        if largest != current_index:
            var = self.HEAP[current_index]
            self.HEAP[current_index] = self.HEAP[largest]
            self.HEAP[largest] = var
            self.heapify(largest)

class running_median_toolKit():
    def __init__(self):
        self.max_heap = max_heap() #less or equal to the median
        self.min_heap = min_heap() #greater than or equal to the median
        self.median = None

    def update_median(self):
        if len(self.max_heap.HEAP) > len(self.min_heap.HEAP):
            self.median = self.max_heap.HEAP[0]
        elif len(self.min_heap.HEAP) > len(self.max_heap.HEAP):
            self.median = self.min_heap.HEAP[0]
        else:
            self.median = (self.min_heap.HEAP[0] + self.max_heap.HEAP[0])/2

    def add(self, element):

        if self.median is None or element >= self.median:
            self.min_heap.add_to_heap(element)
        else:
            self.max_heap.add_to_heap(element)
        self.rebalance_if_needed()
        self.update_median()


    def rebalance_if_needed(self):
        # if max heap too big
        if len(self.max_heap.HEAP) - len(self.min_heap.HEAP) > 1:
            element = self.max_heap.remove_from_heap()
            self.min_heap.add_to_heap(element)
        # if min heap too big
        elif len(self.min_heap.HEAP) - len(self.max_heap.HEAP) > 1:
            element = self.min_heap.remove_from_heap()
            self.max_heap.add_to_heap(element)           

    def give_median(self):
        return str(self.median)

if __name__ == '__main__':
    test = running_median_toolKit()

    for i in range(0,20,2):
        print("adding " + str(i))
        test.add(i)
        print("max heap ")
        print(test.max_heap.HEAP)
        print("min heap ")
        print(test.min_heap.HEAP)
        print("median " + test.give_median())
        print("-------------------")

