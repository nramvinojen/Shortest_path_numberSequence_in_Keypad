# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 08:53:35 2020

author: Ramvinojen
email : nramvinojen@gmail.com
"""

import math
import numpy as np


class Node:
    """
    define a class node, which can store 
    1. the distance from initial position
    2. the left and right finger position 
    3. the path history to reach the node,
        this comes in handy when the tree is too big
    4. left and right pointers
    
    """
    def __init__(self, data):
        self.value = float(data) # refers to the distance travelled to reach this node
        self.LeftPos = -2
        self.RightPos = -1
        self.left = None
        self.right = None
        self.path = ""

"""
1 2 3
4 5 6
7 8 9
* 0 #

Assuming * is index (0, 0) this comes in handy when the 4*3 pannel has to be extended
keypadPos tuple has the numbers in the coseponding index eg keypos[0] gives position(row and col index) of key 0, i.e (0,1)
similary for all other numbers
the * is in index '-2' and # is in index '-1', this allows us to scale easily
"""
class Keypad :
    
   
    def __init__(self):
        #initial setting
        self.debug = -1 # set -1 to ignore all print statements, set 0, 1 for enabling print statements to debug
        self.LeftIdx = -2 
        self.RightIdx = -1
        self.KeypadStr = ('0'    ,   '1' ,   '2' ,    '3',    '4',    '5',    '6',    '7',    '8',    '9',    '*',   '#')
        self.KeypadPos = ([(0, 1), (3, 0), (3, 1), (3, 2), (2, 0), (2, 1), (2, 2), (1, 0), (1, 1), (1, 2), (0, 0), (0, 2) ])
        self.OutputBuffer = ([("Tot Dist as float", "fin left position char ", "fin right pos char", "Full Path")])
        self.RecursionCounter = 0
     
    def resetRecursionCounter(self):
        self.RecursionCounter = 0
        
    def resetOutputBuffer(self):
        self.OutputBuffer = ([("Tot Dist as float", "fin left position char ", "fin right pos char", "Full Path")])        
    
    def resetLeftRightIdx(self):
        """
        sets the left and right finger to initial position * and #
        """
        self.LeftIdx = -2 
        self.RightIdx = -1
    
    def CalcDist(self, OldPos, NewPos):
        """
        calculate the distance, eucledian distanc is implemented
        
        OldPos: tuple, holds the current left, right position as described in KeypadPos ,eg: for number 9, (1,2)
        NewPos : tuple, hold the future left, right position as described in KeypadPos ,eg: for number *, (0,0)
        
        return dist : float, the distance to move from old postion to new position
        """
        dist = math.sqrt( (NewPos[0]-OldPos[0])**2 + (NewPos[1]-OldPos[1])**2  )
        return dist

    def compute_baseline_path(self, InputString):
        """
        computes the shortest path just considering the immediate next number in the sequence
        also the algorithm favours left, incase of equal dist for moving left and right
        
        InputString : the number sequence, string , "5679", does not check for errors
        
        return Result tuple containing distance and the stpe by step postion of left and right 
                eg :(6.60555127546399, [('*', '#'), ('*', '1'), ('*', '3'), ('*', '3'), ('7', '3')])    
        """
        FullDistance = 0
        DirectionHist =[ (self.KeypadStr[self.LeftIdx], self.KeypadStr[self.RightIdx]) ] #stores the keypad position step by step eg: [('*','#'), ('1','#')]
        
        if self.debug == 1:
            print("---------compute_baseline_path--------")
            print(DirectionHist)
        
        for CharIter in range (0, len(InputString)):
            if self.debug == 1:
                print(InputString[CharIter])
            NewPos = self.KeypadPos[ int( InputString[CharIter] ) ]
            RightPos = self.KeypadPos[self.RightIdx]
            LeftPos = self.KeypadPos[self.LeftIdx]
            
            if self.debug == 1:
                print("[left, right ] dist")
            leftDist = self.CalcDist(LeftPos, NewPos)
            RightDist = self.CalcDist(RightPos, NewPos)
            
            if self.debug == 1:
                print( [leftDist, RightDist]   )
            if   RightDist < leftDist  : #preference for left
                if self.debug == 1:
                    print('right')
                self.RightIdx = int( InputString[CharIter] )
                FullDistance = FullDistance + RightDist #update the distance
            else:
                if self.debug == 1:
                    print('Left')       
                self.LeftIdx = int( InputString[CharIter] )
                FullDistance = FullDistance + leftDist
                
            DirectionHist.append( ( self.KeypadStr[self.LeftIdx], self.KeypadStr[self.RightIdx] ) ) #update the new finger position
            if self.debug == 1:
                print(FullDistance)
                print(DirectionHist)
        
        #formating the result as expected in the rwquirement
        #after we end the for loop (go through all the number in the given sequence)
        #append the total distance with the position history
        Result = (FullDistance, DirectionHist)  
        if self.debug == 1:
            print(Result)
        self.resetLeftRightIdx()#reset the finger position, optinially this function can be called in the main
        if self.debug == 1:
            print("---------end of compute_baseline_path--------")
        return(Result)

    def Maketree(self, dist, root, i, n, Lp, Rp, path, BaseDist, InputString ):
        """
        creates a binary tree, each node represents a positon of the fingers after a particular move
        the left child is the result of left finger being used and similary right 
        example for sequence "24" the tree is as follow
                                        0
             (left 2, right #)                  (left *, right 2)
       (4, #)                 (2, 4)     (4, 2)                   (*,4)
       each level represent the movement for the next digit in the given sequence
       
       dist : float, the distance of the current node, for root its 0
       root : root value for the subsequent nodes
       i : int, to identify the leaf and level, iteration
       n : total number of nodes for the tree
       Lp: int, hold the current left finger position, it stores the id for each key as described in KeypadPos, keypadstr
       Rp: int, hold the current right finger position, it stores the id for each key as described in KeypadPos, keypadstr
       Path : str, hold the current path traveled to reach the particular node, eg : "LLRRL"
       BaseDist : float, the baseline value, the distance traveled to finish the sequenc should be lowe than this value
                   used to curtail unnecessar tree branches
       InputString : string, the input sequence numbers, eg : "4566"   
         
       return root : returns to root value 
        """
        self.RecursionCounter = self.RecursionCounter +1
        if i < n:
            level = 0
            newpath = ''
            
            if i > 0:
                dist =  root.value + dist
                level = math.floor( math.log(i+1,2))
                newpath = root.path + path
            if self.debug == 1:
                print("------level----", level)
                print("node distance", dist)
            
            temp = Node(dist)
            temp.LeftPos = Lp
            temp.RightPos = Rp
            temp.path = newpath
            
            root = temp
            
            if 2**(level+1) -1 == n:
                return root
            
            LDist = self.CalcDist(self.KeypadPos[Lp], self.KeypadPos[int(InputString[level])])        
            RDist = self.CalcDist(self.KeypadPos[Rp], self.KeypadPos[int(InputString[level])])
            if self.debug == 1:
                print("Left distance", LDist)
                print("right distance", RDist)
    
            if BaseDist >= dist + LDist :
                root.left = self.Maketree(LDist, root, 2*i+1, n, int(InputString[level]), Rp, 'L' , BaseDist, InputString)
            if BaseDist >= dist + RDist :
                root.right = self.Maketree(RDist, root, 2*i+2, n, Lp, int(InputString[level]), 'R', BaseDist, InputString)
        return root

    def returnGivenLevel(self, root , level): 
        """
        collect all the nodes for given level in the tree in the OutputBuffer 
        recursively traverse to the selected level
        
        root : the root value of the tree
        level : the level of tree you want to be returned, int, eg :3, does not check for error
        """   
        if root is None: 
            return
        if level == 1: 
           self.OutputBuffer.append((root.value, self.KeypadStr[root.LeftPos], self.KeypadStr[root.RightPos], root.path ))
        elif level > 1 : 
            self.returnGivenLevel(root.left , level-1) 
            self.returnGivenLevel(root.right , level-1) 

    def computeDistfromPath(self, InputString, PathString):
        """
        computes the distance and the path for a given string a specific left right pattern
        returns 
        
        InputString : the number sequence, string , "5679", does not check for errors
        PathString : the left right pattern, string , eg : "LLRRL", anything other than 'R' is considered 'left', even lower case
        
        return Result : tuple containing distance and the stpe by step postion of left and right 
                eg :(6.60555127546399, [('*', '#'), ('*', '1'), ('*', '3'), ('*', '3'), ('7', '3')])
        
        """
        
        FullDistance = 0
        DirectionHist =[ (self.KeypadStr[self.LeftIdx], self.KeypadStr[self.RightIdx]) ]
        
        if self.debug == 1:
            print("--------------computeDistfromPath-----------------")
            print(DirectionHist)
        
        for CharIter in range (0, len(InputString)):
            if self.debug == 1:
                print(InputString[CharIter])
            NewPos = self.KeypadPos[ int( InputString[CharIter] ) ]
            RightPos = self.KeypadPos[self.RightIdx]
            LeftPos = self.KeypadPos[self.LeftIdx]
            
            if self.debug == 1:
                print("[left, right ] dist")
            leftDist = self.CalcDist(LeftPos, NewPos)
            RightDist = self.CalcDist(RightPos, NewPos)
            
            if self.debug == 1:
                print( [leftDist, RightDist]   )
            if   PathString[CharIter] == 'R'  : #anything other than 'R' is considered 'left', even lower case
                if self.debug == 1:
                    print('right')
                self.RightIdx = int( InputString[CharIter] )
                FullDistance = FullDistance + RightDist
            else:
                if self.debug == 1:
                    print('Left')       
                self.LeftIdx = int( InputString[CharIter] )
                FullDistance = FullDistance + leftDist
                
            DirectionHist.append( ( self.KeypadStr[self.LeftIdx], self.KeypadStr[self.RightIdx] ) )
            if self.debug == 1:
                print(FullDistance)
                print(DirectionHist)
        
        Result = (FullDistance, DirectionHist)  
        if self.debug == 1:
            print(Result)
            print("--------------end computeDistfromPath-----------------")
        self.resetLeftRightIdx()
        return(Result)



    def compute_laziest_path(self, InputString):
        """
        computes the shortest path considering all possible patterns to type the numbers in the sequence
        also the algorithm uses a controlled binary tree
        
        InputString : the number sequence, string , "5679", does not check for errors
        
        return Result tuple containing distance and the stpe by step postion of left and right 
                eg :(6.60555127546399, [('*', '#'), ('*', '1'), ('*', '3'), ('*', '3'), ('7', '3')])    
        """ 
        if self.debug == 0:
            print("\n \nsimple path and dist calculator-------------------------------")
        BaseResult = self.compute_baseline_path(InputString)
        if self.debug == 0:
            print(BaseResult)
        BaseDist = BaseResult[0]
        
        if self.debug == 0:
            print("\n \nBuild binary tree, stop unwanted branches from growing--------")
        seqLen = len(InputString)
        NumNodes = 2**(seqLen+1) -1
        NumLeaves  = 2**(seqLen)
        if self.debug == 0:
            print("seqence length :",seqLen)
            print("Expected Num of Nodes",NumNodes, ", Expected Num of Leaves",NumLeaves  )
        root = None
        root = self.Maketree(0, root, 0, NumNodes, -2, -1, '', BaseDist, InputString )
        if self.debug == 0:
            print("Num nodes actually built :", self.RecursionCounter)
        self.resetRecursionCounter()
    
        if self.debug == 1:
            #use helper function for debugging
            print("\n\nTree Inorder---------------")
            self.printLevelOrder(root,seqLen+1 )
            
            print("\n\nLeaves---------------")
            self.printGivenLevel(root,  len(InputString)+1)
        
        if self.debug == 0:
            print("\n\n Retrive the leaf nodes ----------------------------------------")
        self.returnGivenLevel(root , len(InputString)+1)
        if self.debug == 0:
            print(self.OutputBuffer)
        TempResult = self.OutputBuffer
        self.resetOutputBuffer() 
        if self.debug == 0:
            print("Number of leaves actually built :", len(TempResult)-1 )
        
        if self.debug == 0:
            print("\n\nSelect the min value ------------------------------------------")
        index_min = 0
        dist = np.zeros(len(TempResult) )
        for leaf in range(1, len(TempResult) ) :
            dist[leaf] = TempResult[leaf][0]
            index_min = np.argmin(dist[1:])+1
        if self.debug == 0:
            print("Baseline dist :" , BaseDist, "\nDist from tree method : ", TempResult[index_min][0] )
        
        if self.debug == 0:
            print("\n\nReturn the result in the requested format ---------------------")
        Result = self.computeDistfromPath(InputString, TempResult[index_min][3])
            
             
        return(Result)
           
    """
    Helper Functions
    """       
    def LeftandRightPosIdx(self):
        """
        return [int, int], returns the index position based on the keypadStr format eg: [-2, 4]
        """
        print(self.LeftIdx)
        return([self.LeftIdx, self.RightIdx])
    
    def printLevelOrder(self, root, h): 
        """
        prints all the node of the treee
        implemented as iteratively printing all the levels
        """
        for i in range(1, h+1): 
            self.printGivenLevel(root, i) 
           
    def printGivenLevel(self, root , level): 
        """
        prints all the nodes for given level in the tree
        recursively traverse to the selected level
        """
        if root is None: 
            return
        if level == 1: 
            print( "Node val %.3f"  %(root.value), "------- Lp", self.KeypadStr[root.LeftPos], "------- Rp",  self.KeypadStr[root.RightPos], "------ path", root.path) 
        elif level > 1 : 
            self.printGivenLevel(root.left , level-1) 
            self.printGivenLevel(root.right , level-1) 
