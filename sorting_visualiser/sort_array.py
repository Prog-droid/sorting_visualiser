import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import floor

class sort_array:
    """
    Class for the array which needs to be sorted.


    """

    def __init__(self, length):
        """
        Initialises 
        """
        self.list = random.sample(range(length), length)
        random.shuffle(self.list)
        #generate random list

        self.length = length
        #length of the list and maximum possible value of the list
        
        self._no_swaps = False
        #is true when no swaps have been made on a full iteration of list

        self._complete_copies = []
        #stores self.list after each step of sorting
        
        self.accesses = []
        #stores which indexes in the array have been accessed

        self.operation = []
        #stores what type of operation

        self.fps = 60
        #upper limit of fps on FuncAnimation

        self._swap_pairs = {}
        #dictionary of frame:array of compared elements pairs
      
        self._accessed_elements = {}
        #dictionary of frame:array of accessed elements pairs

        self.menu()

    def menu(self):
        """
        Asks the user to decide which algorithm they want to sort the array
        """

        valid_input = False
        #is the user's input valid
        
        while valid_input == False:
            #ask the user for an input
            user_input = input("Please enter a number to choose which sorting algorithm to use\n1.\tBubble sort\n2.\tInsertion sort\n3.\tQuicksort\n4.\tRadix sort\n5.\tMerge sort\n\n")
            if len(user_input) > 1:
                continue

            
            if user_input == "1":
                self.bubble_sort()
            elif user_input == "2":
                self.insertion_sort()
            elif user_input == "3":
                self.quicksort()
            elif user_input == "4":
                self.radix_sort()
            elif user_input == "5":
                self.merge_sort()

    def bubble_sort(self):
        """
        Apply bubble sort algorithm to the random array.
    
        Parameters:
            self - object of the sort_array class
        """
       
        sorted_array_index = len(self.list) - 1


        while self._no_swaps == False:
            
            self._no_swaps = True
            
            for i in range(sorted_array_index):
                
                #access and compare two elements in the array
                self._accessed_elements[len(self._complete_copies)] = (i, i + 1)
                if self.list[i] > self.list[i+1]:
                    self.swap(i, i + 1)
                else:
                    self._complete_copies.append(np.copy(self.list))  
                
            sorted_array_index = sorted_array_index - 1
        #draw the graph
        self.plot()

    def insertion_sort(self):
        """
        Apply insertion sort algorithm to the random array.

        Parameters:
        self - object of the sort_array class
        """

        sorted_array_index = 0

        for i in range(len(self.list)):
            for j in range(i, 0, -1):
                #access and compare two elements in the array
                self._accessed_elements[len(self._complete_copies)] = (j, j - 1)        
                if(self.list[j] < self.list[j-1]):
                    self.swap(j, j-1)
                else:
                    self._complete_copies.append(np.copy(self.list))
                    break
                


        self.plot()

    def radix_sort(self):
        """
        Apply radix sort algorithm to sort self.list.

        Parameters:
        self - object of the sort_array class
        """

        base = 10
        #base of the numbers in the array

        temp = [[] for i in range(base)]
        #stores elements of array during count sort

        self._accessed_elements[len(self._complete_copies)] = (len(self.list) - 1, len(self.list) - 1)
        self._complete_copies.append(np.copy(self.list))
        max_value = len(self.list) - 1
        #the greatest value in the array

        max_digits = 0
        #the number of digits the max_value has

        index = 0
        #index of self.list, used to convert temp to self.list

        #empty arrays and single element arrays are already sorted
        if max_value <= 1:
            return

        #find max_digits
        while max_value != 0:
            max_value = (max_value - max_value % base) / base
            max_digits += 1

       
        #iterate through all digits
        for i in range(1, max_digits + 1, 1):
            temp = [[] for i in range(base)]

            #use count sort to sort array by xth significant digit
            for j in range(len(self.list)):
                self._accessed_elements[len(self._complete_copies)] = (j, j)
                self._complete_copies.append(np.copy(self.list))
                temp[self.get_digit(self.list[j], i, base)].append(self.list[j])
            
            index = 0
            
            #convert temp into array of elements
            for j in temp:
                for k in j:        
                    self.swap_value(index, k)
                    index = index + 1

        self.plot()

    def get_digit(self, value, digit, base):

        if value == 0:
            return 0
        answer = 0
        
        for i in range(digit):
            answer = value % base
            value = (value - answer) / base
      
        return int(answer)

    def quicksort(self):
        """
        Calls the quicksort function and then calls plotting function
        
        Parameter:
        self - object of the sort_array class
        """

        self.qsort(0, len(self.list) - 1)
        self.plot()

    def qsort(self, low, high):
        """
        Apply quicksort algorithm to the random array.

        Parameters:
        self - object of the sort_array class
        low - index of the lower bound of array needed to be sorted
        high - index of the upper bound of array needed to be sorted
        """
        if high <= low:
            return

        
        self._accessed_elements[len(self._complete_copies)] = (high, high)
        self._complete_copies.append(np.copy(self.list))
        
        pivot = self.list[high]

        leftmost = low
        #the leftmost element larger than the pivot

        rightmost = high - 1
        #the rightmost element smaller than the pivot

        while leftmost <= rightmost:
            
            #find the solution for leftmost
            for i in range(leftmost, rightmost + 1, 1):
                self._accessed_elements[len(self._complete_copies)] = (i, i)
                self._complete_copies.append(np.copy(self.list))
                if self.list[i] > pivot:
                    leftmost = i
                    break
            
            #if there is no solution for leftmost, pivot is highest, then sort the rest of the array
            else:
                self.qsort(low, high - 1)
                return

 
            #find the solution for rightmost
            for i in range(rightmost, leftmost - 1, -1):
                self._accessed_elements[len(self._complete_copies)] = (i, i)
                self._complete_copies.append(np.copy(self.list))
                if self.list[i] < pivot:
                    rightmost = i
                    break
            
            #if there is no solution for rightmost, pivot is lowest, then move pivot to index 0 and sort the rest of the array  
            else:
                self.swap(leftmost, high)
                self.qsort(low, leftmost - 1)
                self.qsort(leftmost + 1, high)
                return

            if leftmost > rightmost:
                self.swap(leftmost, high)
                self.qsort(low, leftmost - 1)
                self.qsort(leftmost + 1, high)
            else:
                self.swap(leftmost, rightmost)

    def merge_sort(self):
        """
        Calls the merge sort function and then calls plotting function
        
        Parameter:
        self - object of the sort_array class
        """
        
        self._merge_sort(0, len(self.list) - 1)
        self.plot()

    def _merge_sort(self, low, high):
        """
        Apply quicksort algorithm to the random array.

        Parameters:
        self - object of the sort_array class
        low - index of the lower bound of array needed to be sorted
        high - index of the upper bound of array needed to be sorted
        
        """
        
        


        #invalid array boundaries
        if high <= low:
            return
 
        #only call when array boundaries are large enough
        if high - low > 1:
            self._merge_sort(low, floor((high - low)/ 2) + low)
            self._merge_sort(floor((high - low)/ 2) + low + 1 , high)

                
        first_array = [self.list[i] for i in range(low, floor((high - low)/ 2) + low + 1, 1)]
        #first half of the array needed to be sorted
        
        second_array = [self.list[i] for i in range(floor((high - low)/ 2) + low + 1, high + 1, 1)]
        #second half of the array needed to be sorted

        result = []
        #temporarily stores the sorted array


        first_array_index = 0
        #keeps track of the current index of the first half of array

        second_array_index = 0
        #keeps track fo the current index of second half of array

        result_index = 0
        #keeps track of the index of the result


        #two pointers method of sorting
        while len(result) < len(first_array) + len(second_array):

            #if first array has been iterated through append second array to result
            if first_array_index > len(first_array) - 1:
                for i in range(second_array_index, len(second_array), 1):
                    self._accessed_elements[len(self._complete_copies)] = (low + i, low + i)
                    self._complete_copies.append(np.copy(self.list))
                    result.append(second_array[i])
                break

            #if second array has been iterated through append first array to result
            elif second_array_index > len(second_array) - 1:
                for i in range(first_array_index, len(first_array), 1):
                    self._accessed_elements[len(self._complete_copies)] = (low + i, low + i)
                    self._complete_copies.append(np.copy(self.list))
                    result.append(first_array[i])
                break

            #if current element in second array is smaller than current element in first array
            self._accessed_elements[len(self._complete_copies)] = (first_array_index + low, second_array_index + floor((high - low)/ 2) + low + 1)
            self._complete_copies.append(np.copy(self.list))
            if first_array[first_array_index] > second_array[second_array_index]:
                result.append(second_array[second_array_index])
                second_array_index += 1
            else:
                result.append(first_array[first_array_index])
                first_array_index += 1

        
        #copy results into appropriate segment of array
        for i in range(low, high + 1, 1):
            self.swap_value(i, result[result_index])
            result_index += 1


    def swap(self, i, j):
        """
        Swaps two elements in a list according to the index, i and j.

        Parameters:
        self - object of the sort_array class
        i - index of the first element which needs to be swapped
        j - index of the second element which needs to be swapped
        """

        self._complete_copies.append(np.copy(self.list))

        #swap the pair of elements
        self.list[i], self.list[j] = self.list[j], self.list[i]
        self._no_swaps = False
        
        #update _complete_copies and _swap_pairs
        self._swap_pairs[len(self._complete_copies)] = (i, j)
        self._complete_copies.append(np.copy(self.list))
        self._swap_pairs[len(self._complete_copies)] = (i, j)
        self._complete_copies.append(np.copy(self.list))

    def swap_value(self, i, value):
        """
        Swaps two elements in a list according to the index, i and j.

        Parameters:
        self - object of the sort_array class
        i - index of the first element which needs to be swapped
        value - the value to be stored in index i
        """

        self._complete_copies.append(np.copy(self.list))

        #swap the pair of elements
        self.list[i] = value
        self._no_swaps = False
        
        #update _complete_copies and _swap_pairs
        self._swap_pairs[len(self._complete_copies)] = (i, i)
        self._complete_copies.append(np.copy(self.list))
        self._swap_pairs[len(self._complete_copies)] = (i, i)
        self._complete_copies.append(np.copy(self.list))



    def _get_swap_elements(self, index):
        
        x = self._swap_pairs.get(index)
       
        #prevent TypeError
        if x == None:
            x = ()
        
        return x

    def _get_accessed_elements(self, frame):
        """
        Private function which returns an iterable array from _accessed_elements dictionary or an empty array.

        Parameters:
        self - object of the sort_array class
        frame - the current frame in the animation loop 
        """
        x = self._accessed_elements.get(frame)
        
        #prevent TypeError
        if x == None:
            x = ()

        return x
    
    def plot(self):
        """
        Plots the bar graph for array of elements.

        Parameters:
        self - object of the sort_array class
        """
        
        #iterate through the list and highlight 
        for i in range(len(self.list)):
            self._complete_copies.append(self.list)
            self._accessed_elements[len(self._complete_copies)] = [i]
        self._complete_copies.append(self.list)
        self._complete_copies.append(self.list)
        
        #display graph
        fig, ax = plt.subplots(figsize = (16,7))
        
        #bars for the graph
        container = ax.bar(np.arange(0, len(self._complete_copies[0]), 1), self._complete_copies[0], align = 'center')

        def update(frame):
            """
            update function called by FuncAnimation of bar graph.

            Parameters:
            frame - which frame is the animation of the bar graph on
            """

            #update array in bar graph
            for value, rect in zip(self._complete_copies[frame], container.patches):
                rect.set_height(value)
                rect.set_color("#0000FF")
                
            #update accessed elements in bar graph
            for i in self._get_accessed_elements(frame):
                container.patches[i].set_color("#FF0000")

            #update swap elements in bar graph
            for i in self._get_swap_elements(frame):
                container.patches[i].set_color("#00FF00")
           
            return container.patches
        
        #animate/update bar graph
        animation = FuncAnimation(fig, update, frames = range(len(self._complete_copies)), blit = True, repeat = False, interval=(100/self.length**4 * self.fps))

        plt.show()