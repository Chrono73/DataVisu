'''
Created on june 9th 2011

@author: Locqueville Martin
'''

from tulip import *
import math

class Walker():

    def __init__(self, graph):
        '''
        Constructor
        '''
        self.graph = graph

        self.levelZeroPtr = list()
        self.xTopAdjustment = 0
        self.yTopAdjustment = 0

        self.LevelSeparation = 2
        self.MaxDepth = math.inf
        self.SiblingSeparation = 1
        self.SubtreeSeparation = 5

    def parent(node):
        try:
            return self.graph.getInNodes(node).next()
        except StopIteration:
            return None

    def hasChild(node):
        try:
            self.graph.getOutNodes(node).next()
            return True
        except StopIteration:
            return False

    def firstChild(node):
        try:
            return self.graph.getOutNodes(node).next()
        except StopIteration:
            return None

    def hasLeftSibling(node):
        parent = self.parent(node)
        siblingList = self.graph.getOutNodes(parent)
        try:
            current = siblingList.next()
            try:
                while (true):
                    sibling = current
                    current = siblingList.next()
                    if (node == current):
                        return True
            except StopIteration:
                return False
        except StopIteration:
            return False

    def leftSibling(node):
        parent = self.parent(node)
        siblingList = self.graph.getOutNodes(parent)
        try:
            current = siblingList.next()
            try:
                while (true):
                    sibling = current
                    current = siblingList.next()
                    if (node == current):
                        return sibling
            except StopIteration:
                return None
        except StopIteration:
            return None

    def hasRightSibling(node):
        parent = self.parent(node)
        siblingList = self.graph.getOutNodes(parent)
        try:
            while (true):
                current = siblingList.next()
                if (node == current):
                    try:
                        current = siblingList.next()
                        return True
                    except StopIteration:
                        return False
        except StopIteration:
            return False

    def rightSibling(node):
        parent = self.parent(node)
        siblingList = self.graph.getOutNodes(parent)
        try:
            while (true):
                current = siblingList.next()
                if (node == current):
                    return siblingList.next()
        except StopIteration:
            return None

    def xCoord(node):
        return self.graph['viewLayout'][node].getX()

    def yCoord(node):
        return self.graph['viewLayout'][node].getY()

    '''
    def prelim(node):
        return self.graph['prelim'][node]

    def modifier(node):
        return self.graph['modifier'][node]
    '''
    def prelim(node, val):
        self.graph['prelim'][node] = val

    def modifier(node, val):
        self.graph['modifier'][node] = val

    '''
    def leftNeighbor(node):
        return
    '''

    def initPrevNodeList():
        for i in range(0, self.graph['viewMetric'].getNodeMax()):
            self.levelZeroPtr.append(None)

    '''
        GetPrevNodeAtLevel and SetPrevNodeAtLevel are just the regular getter and setter
        for this list.
        CheckExtentsRange is useless in the context of Tulip
    '''

    def getLeftMost(node, level, depth):
        if (level >= depth):
            return node
        elif (self.graph['viewMetric'][node]==0):
            return None
        else:
            rightmost = self.firstChild(node)
            leftmost = self.getLeftMost(rightmost, level+1, depth)
            while ((leftmost == None) and (self.hasRightSibling(rightmost))):
                rightmost = rightSibling(rightmost)
                leftmost = self.getLeftMost(rightmost, level+1, depth)
            return leftmost

    def positionTree(node):
        if (node == None):
            return True
        else:
            '''
            initPrevNodeList()
            firstWalk(node, 0)

            xTopAdjustment = xCoord(node) - prelim(node)
            yTopAdjustment = yCoord(node)

            return secondWalk(node, 0, 0)
            '''

def main(graph):
    print 'Compilation successful.'
