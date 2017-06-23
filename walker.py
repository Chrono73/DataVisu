'''
Created on june 9th 2011

@author: Locqueville Martin
'''

from tulip import *
import math

class Walker(object):

    def __init__(self, graph):
        '''
        Constructor
        '''
        self.graph = graph
        n = self.graph.getNodes()
        self.root = n.next()
        
        self.graph.getIntegerProperty('levelIndex')

        self.levelZeroPtr = list()
        self.xTopAdjustment = 0
        self.yTopAdjustment = 0

        self.LevelSeparation = 2
        self.MaxDepth = self.graph['viewMetric'].getNodeMax()
        self.SiblingSeparation = 1
        self.SubtreeSeparation = 5

        # Assigne a chaque node l'index de sa position sur sa ligne.
    def initNodeLevelIds(self):
        levelCounter = list()
        for i in range(0, int(self.graph['viewMetric'][self.root])+1):
            levelCounter.append(0)
        nodes = self.graph.getNodes()
        for n in nodes:
            self.graph['levelIndex'][n] = levelCounter[self.level(n)]
            levelCounter[self.level(n)] += 1
    
        # Renvoie la index-ieme node du niveau lvl du graphe
    def getNthNodeAtLevel(self, lvl, index):
        nodes = self.graph.getNodes()
        for n in nodes:
            if ((self.level(n) == lvl) and (self.graph['levelIndex'][n] == index)):
                return n
        return None

        # Renvoie le parent de la node actuelle.
    def parent(self, node):
        try:
            res = self.graph.getInNodes(node).next()
        except:
            res = None
        return res

        # Renvoie le niveau de la node actuelle
    def level(self, node):
        level = 0
        current = node
        while not (self.parent(current)==None):
            current = self.parent(current)
            level += 1
        return level

        # Verifie si la node possede un enfant (si c'est une feuille)
    def hasChild(self, node):
        try:
            self.graph.getOutNodes(node).next()
            return True
        except StopIteration:
            return False

        # Renvoie le premier enfant de la node
    def firstChild(self, node):
        try:
            return self.graph.getOutNodes(node).next()
        except StopIteration:
            return None

        # Verifie si la node possede un voisin de gauche
    def hasLeftSibling(self, node):
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

        # Renvoie le voisin de gauche de la node
    def leftSibling(self, node):
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

        # Verifie si la node possede un voisin de droite
    def hasRightSibling(self, node):
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

        # Renvoie le voisin de droite de la node
    def rightSibling(self, node):
        parent = self.parent(node)
        siblingList = self.graph.getOutNodes(parent)
        try:
            while (true):
                current = siblingList.next()
                if (node == current):
                    return siblingList.next()
        except StopIteration:
            return None

        # Renvoie la coordonnee x de la node
    def xCoord(self, node):
        return self.graph['viewLayout'][node].getX()

        # Renvoie la coordonnee y de la node
    def yCoord(self, node):
        return self.graph['viewLayout'][node].getY()

        # Permet de definir la coordonnee x preliminaire de la node
    def prelim(self, node, val):
        self.graph['prelim'][node] = val

        # Permet de definir le modificateur de la node
    def modifier(self, node, val):
        self.graph['modifier'][node] = val

        # Renvoie la node devant etre disposee a gauche de la node en parametre
    def leftNeighbor(self, node):
        return self.getNthNodeAtLevel(self.level(node), self.graph['levelIndex'][node]-1)
            

    def initPrevNodeList(self):
        for i in range(0, self.graph['viewMetric'][root]):
            self.levelZeroPtr.append(None)

    '''
        GetPrevNodeAtLevel and SetPrevNodeAtLevel are just the regular getter and setter
        for this list.
        CheckExtentsRange is useless in the context of Tulip
    '''

    def getLeftMost(self, node, level, depth):
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

    def positionTree(self, node):
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
    walk = Walker(graph)
    walk.initNodeLevelIds()
