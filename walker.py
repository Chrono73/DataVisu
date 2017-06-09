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
        self.LevelSeparation = 2
        self.MaxDepth = math.inf
        self.SiblingSeparation = 1
        self.SubtreeSeparation = 5

    def parent(node):
        try:
            return self.graph.getInNodes(node).next()
            break
        except StopIteration:
            return None

    def firstChild(node):
        try:
            return self.graph.getOutNodes(node).next()
            break
        except StopIteration:
            return Node

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
                break
            except StopIteration:
                return None
            break
        except StopIteration:
            return None

    def rightSibling(node):
        parent = self.parent(node)
        siblingList = self.graph.getOutNodes(parent)
        try:
            while (true):
                current = siblingList.next()
                if (node == current):
                    return siblingList.next()
            break
        except StopIteration:
            return None
