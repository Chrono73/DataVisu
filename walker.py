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
        self.prelim = self.graph.getDoubleProperty('prelim')
        self.modifier = self.graph.getDoubleProperty('modifier')

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

    def firstWalk(self, node, lvl):
        self.levelZeroPtr[lvl] = node
        self.modifier[node] = 0
        if ((not self.hasChild(node)) or (lvl == MaxDepth)):
            if (self.hasLeftSibling(node)):
                self.prelim[node] = self.prelim[self.leftSibling(node)]
                self.prelim[node] += self.SiblingSeparation + 1.0
            else:
                self.prelim[node] = 0
        else:
            leftmost = self.firstChild(node)
            rightmost = self.firstChild(node)
            self.firstWalk(leftmost, lvl+1)
            while (self.hasRightSibling(rightmost)):
                rightmost = rightSibling(rightmost)
                self.firstWalk(rightmost, lvl+1)
            midpoint = (self.prelim[leftmost] + self.prelim[rightmost])/2.0
            if (self.hasLeftSibling(node)):
                self.prelim[node] = self.prelim[self.leftSibling(node)]
                self.prelim[node] += self.SiblingSeparation + 1.0
                self.modifier[node] = self.prelim[node] - midpoint
                self.apportion(node, lvl)
            else:
                self.prelim[node] = midpoint

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
            
    def apportion(self, node, lvl):
        leftmost = self.firstChild(node)
        neighbor = self.leftNeighbor(leftmost)
        compareDepth = 1
        depthToStop = MaxDepth - lvl

        while (not (leftmost == None) and not (neighbor == None) and (compareDepth >= depthToStop)):
            leftModSum = 0
            rightModSum = 0
            ancestorLeftmost = leftmost
            ancestorNeighbor = neighbor
            for i in range(0, compareDepth+1):
                ancestorLeftmost = self.parent(ancestorLeftmost)
                ancestorNeighbor = self.parent(ancestorNeighbor)
                rightModSum += self.modifier(ancestorLeftmost)
                leftModSum += self.modifier(ancestorNeighbor)
            moveDistance = self.prelim[neighbor] + leftModSum + SubtreeSeparation + 1
            moveDistance -= (self.prelim[leftmost] + rightModSum)

            if (moveDistance > 0):
                tempPtr = node
                leftSiblings = 0
                while (not (tempPtr == None) and not (tempPtr == ancestorNeighbor)):
                    leftSiblings += 1
                    tempPtr = self.leftSibling(tempPtr)
                if not (tempPtr == None):
                    portion = moveDistance / leftSiblings
                    tempPtr = node
                    while (tempPtr == ancestorNeighbor):
                        self.prelim[tempPtr] += moveDistance
                        self.modifier[tempPtr] += moveDistance
                        moveDistance -= portion
                        tempPtr = self.leftSibling(tempPtr)
                else:
                    return

            compareDepth += 1
            if not (self.hasChild(leftmost)):
                leftmost = getLeftMost(node, 0, compareDepth)
            else:
                leftmost = self.firstChild(leftmost)

    def positionTree(self, node):
        if (node == None):
            return True
        else:
            '''
            initPrevNodeList()
            firstWalk(node, 0)

            xTopAdjustment = xCoord(node) - prelim[node]
            yTopAdjustment = yCoord(node)

            return secondWalk(node, 0, 0)
            '''

def main(graph):
    print 'Compilation successful.'
    walk = Walker(graph)
    walk.initNodeLevelIds()
