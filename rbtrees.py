class Node:
    def __init__(self, val, color = 'B'):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent != None:
          return self.parent.parent

    def summary(self):
        if self.val is None:
            return self.color + ":"

        return self.color + ":" + str(self.val)

    def delete(self, val):
        """
        Recurses if val != self.val

        Finds min if left exists, or max if
        right exists, and replaces current value
        with that

        Else, deletes current node, handles balance,
        and returns the deleted node.
        """

        if self.val is None:
            # deleting key that doesn't exist
            return None

        if val < self.val:
            self.left.delete(val)
        elif val > self.val:
            self.right.delete(val)
        else:
            if self.left.val is not None:
                deleted = self.left.deleteMax()
                self.val = deleted.val
                return deleted
            elif self.right.val is not None:
                deleted = self.right.deleteMin()
                self.val = deleted.val
                return deleted
            else:
                return self.deleteEnd()

    def find(self, val):
        if self.val is None:
            return None
        elif val < self.val:
            return self.left.find(val)
        elif val > self.val:
            return self.right.find(val)
        else:
            return self

    def deleteEnd(self):
        """
        Assumes this node has a value and two black leaf children.

        self.left takes this node's place after deletion.
        self.right is assumed to be discarded later.

        If this is a non-trivial delete, then we call rebalanceBegin
        on the replacement node before returning.
        """
        c = self.left if self.left.val is not None else self.right

        if self.parent is None:
            return self

        c.parent = self.parent
        if self.parent.left == self:
            self.parent.left = c
        else:
            self.parent.right = c

        if self.color == 'R':
            return self

        if c.color == 'R':
            c.color = 'B'
            return self

        c.rebalanceBegin()
        return self

    def deleteMax(self):
        if self.right.val is not None:
            return self.right.deleteMax()
        else:
            return self.deleteEnd()

    def deleteMin(self):
        if self.left.val is not None:
            return self.left.deleteMin()
        else:
            return self.deleteEnd()

    def uncle(self):
        g = self.grandparent()
        if g != None and g.left == self.parent:
            return g.right
        else:
            return g.left

    def insert(self, val):
        if self.val is None:
            self.val = val
            self.color = 'R'
            self.left = Node(None)
            self.left.parent = self
            self.right = Node(None)
            self.right.parent = self
            self.rebalanceForConsecutiveRedsBegin()
            return

        # No double inserts?
        # if val == self.val:
        #   return

        if val < self.val:
            self.left.insert(val)
        else:
            self.right.insert(val)

    def rebalanceForConsecutiveRedsBegin(self):
        """
           Assumes self is red. Parent may or
           may not be red.

           May recurse on grandparent.
        """
        if self.parent == None:
            self.color = 'B'
            return

        if self.parent.color == 'B':
            return

        g = self.grandparent()
        u = self.uncle()

        if g is None:
            self.parent.color = 'B'
            return

        if u != None and u.color == 'R':
            u.color = 'B'
            self.parent.color = 'B'
            g.color = 'R'
            g.rebalanceForConsecutiveRedsBegin()
            return

        if self.parent.left == self and \
           g.right == self.parent:
            self.parent.rotateRight()
            self.right.reblanceForConsecutiveRedsFinish()
            return
        elif self.parent.right == self and \
           g.left == self.parent:
            self.parent.rotateLeft()
            self.left.reblanceForConsecutiveRedsFinish()
            return

        self.reblanceForConsecutiveRedsFinish()

    def reblanceForConsecutiveRedsFinish(self):
        """
           Assumes grandparent exists

           Assumes parent and self are red

           Assumes self is left of parent and parent is left grandparent
           or, self is right of parent and parent is right of grandparent

           Does not recurse.
        """
        g = self.grandparent()

        g.color = 'R'
        self.parent.color = 'B'
        if self.parent.left == self:
            g.rotateRight()
        else:
            g.rotateLeft()

    def sibling(self):
        if self.parent == None: raise "Calling sibling on root node"
        if(self.parent.left == self): return self.parent.right;
        if(self.parent.right == self): return self.parent.left;

    def rotateLeft(self):
        oldRight = self.right

        self.right = oldRight.left
        self.right.parent = self

        oldRight.left = self
        oldRight.parent = self.parent
        self.parent = oldRight

        if oldRight.parent is not None:
            if oldRight.parent.left == self:
                oldRight.parent.left = oldRight
            elif oldRight.parent.right == self:
                oldRight.parent.right = oldRight

    def rotateRight(self):
        oldLeft = self.left

        self.left = oldLeft.right
        self.left.parent = self

        oldLeft.right = self
        oldLeft.parent = self.parent
        self.parent = oldLeft

        if oldLeft.parent is not None:
            if oldLeft.parent.left == self:
                oldLeft.parent.left = oldLeft
            elif oldLeft.parent.right == self:
                oldLeft.parent.right= oldLeft

    def rebalanceBegin(self):
        """
           May tail-recurse upwards in the tree by calling
               self.parent.rebalanceBegin()

           May confine balance to a specific subtree by calling any of:
               self.left.rebalanceFinish()
               self.right.rebalanceFinish()
               self.rebalanceFinish()
        """
        if self.parent == None:
            return

        s = self.sibling()
        if s.color == 'R':
            s.color = 'B'
            self.parent.color = 'R'
            if self.parent.left == self:
                self.parent.rotateLeft()
                self.rebalanceFinish()
            else:
                self.parent.rotateRight()
                self.rebalanceFinish()
            return

        # All black? This side of the tree is really dense.
        # We need to contemplate a rotation toward
        # the other side. We recurse upward.
        if self.parent.color == 'B' and \
           s.color == 'B' and \
           s.left.color == 'B' and \
           s.right.color == 'B':
            s.color = 'R'
            self.parent.rebalanceBegin()
            return

        self.rebalanceFinish()

    def rebalanceFinish(self):
        """
           Assumes that paths that go through self have one less black
           node than paths that go through sibling, and this needs to
           be fixed.

           Ensures that imbalances are fixed without examining any
           nodes higher than self.parent.

           Does not recurse.
        """
        s = self.sibling()
        if self.parent.color == 'R' and \
           s.color == 'B' and \
           s.left.color == 'B' and \
           s.right.color == 'B':
            self.parent.color = 'B'
            s.color = 'R'
            return

        if self.parent.left == self and \
           s.color == 'B' and \
           s.left.color == 'R' and \
           s.right.color == 'B':
            s.left.color = 'B'
            s.color = 'R'
            s.rotateRight()
        elif self.parent.right == self and \
           s.color == 'B' and \
           s.right.color == 'R' and \
           s.left.color == 'B':
            s.right.color = 'B'
            s.color = 'R'
            s.rotateLeft()

        s = self.sibling()
        if self.parent.left == self and \
           s.color == 'B' and \
           s.right.color == 'R':
            s.color = self.parent.color
            s.right.color = 'B'
            self.parent.color = 'B'
            self.parent.rotateLeft()
        elif self.parent.right == self and \
           s.color == 'B' and \
           s.left.color == 'R':
            s.color = self.parent.color
            s.left.color = 'B'
            self.parent.color = 'B'
            self.parent.rotateRight()

    def __str__(self):
        """
        Copied from BST implementation from MIT online
        courseware - not mine.
        http://ocw.mit.edu/OcwWeb/Electrical-Engineering-and-Computer-Science/6-006Spring-2008/CourseHome/index.htm
        """
        def recurse(node):
            if node is None: return [], 0, 0
            label = node.summary()
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
               node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self) [0])

class RedBlackTree:
    def __init__(self):
        self.root = None

    def randInit(self, n, max):
        """
        Returns list of elements that were inserted.
        """
        self.root = None
        for i in xrange(0, n):
            self.insert(random.randint(0,max))

    def delete(self, val):
        if self.root is None:
            return

        deleted = self.root.delete(val)
        if deleted == self.root:
            self.root = None
            return
        else:
            self.checkIfRootRotated()

    def find(self, val):
        if self.root is None:
            return None

        return self.root.find( val )

    def __str__(self):
        if self.root is None:
            return "<empty tree>"

        return str(self.root)

    def insert(self, val):
        if self.root == None:
            self.root = Node(val)
            self.root.left = Node(None)
            self.root.left.parent = self.root
            self.root.right = Node(None)
            self.root.right.parent = self.root
            return

        self.root.insert( val )
        self.checkIfRootRotated()

    def checkIfRootRotated(self):
        while self.root.parent is not None:
            self.root = self.root.parent


#######################################################
## Console interface
#######################################################

import sys, random, time, os

def performance_test():
    for n in xrange(1,15): # 1..14 inclusive
      nodes = 2**n

      if os.name == 'nt':
          timer = time.clock
      else:
          timer = time.time

      begin = timer()
      t = RedBlackTree()
      t.randInit( nodes, 30000 )
      runtime = timer() - begin
      print "n: %d, logb2: %d, runtime: %s (s)" % (nodes, n, runtime)

def main():
    """
    This whole thing is a hack.
    """
    t = RedBlackTree()

    if len( sys.argv ) == 1:
        print "Give one positive integer, or several integers. Inserts and random deletes will occur for explicit inputs."
        return

    if len( sys.argv ) == 2:
        toInsert = t.randInit( int( sys.argv[1] ), 100 )
        print t
        return

    toInsert = []
    for i in sys.argv[1:]:
        toInsert.append( int(i) )

    for n in toInsert:
        t.insert( n )
        print
        print t

    random.shuffle(toInsert)
    for n in toInsert:
        t.delete(n)
        print
        print t

if __name__ == '__main__':
    #performance_test()
    main()