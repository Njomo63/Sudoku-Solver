import numpy as np

class ConstraintsMatrix:
    """A class that will create a constraint possibilities matrix for a given 9*9 sudoku puzzle."""
    def createconstraints(self):
        """Creates and returns a dictionary that will contain possibilities as keys and constraints as values."""
        get_constraints = {}    #dictionary that will contain constraints
        for r in range(9):
            box_i = r//3
            
            for c in range(9):
                box_j = c//3
                b = (box_i * 3) + box_j
                
                for v in range(1, 10):
                    get_constraints[((r,c),v)] = [
                        ("Cell", (r,c)),
                        ("Row", (r, v)),
                        ("Column", (c, v)),
                        ("Box", (b, v))
                        ]
        
        return get_constraints

    def remove_poss(self, possibility):
        """Removes constraints that are no longer valid as well as possibilities."""
        for c in self.poss[possibility]:   #loop through each constraint for a possibility
            for other_pos in self.constraints[c]: #loop through each possibility of the constraint
                for other_c in self.poss[other_pos]: #loop through each constraint of the new possibility
                    if other_c != c:         #if the new constraint doesn't match the initial constraint
                        self.constraints[other_c].remove(other_pos)  #remove the new possibility from the constraint set
            del self.constraints[c]         #delete the initial constraint
    
    def __init__(self, values):
        self.values = values           #the incomplete sudoku puzzle in form of a nested list
        #will contain each constraint as a key and a set for values
        self.constraints = {
            c: set() for c in (
                [("Cell", (r, c)) for r in range(9) for c in range(9)] +

                # Every row must contain each value, (row, val)
                [("Row", (r, v)) for r in range(9) for v in range(1, 10)] +

                # Every column must contain each value, (column, val)
                [("Column", (c, v)) for c in range(9) for v in range(1, 10)] +

                # Every block must contain each value, (block, val)
                [("Box", (b, v)) for b in range(9) for v in range(1, 10)]
            )
        }

        self.poss = self.createconstraints()  #dictionary that has possibilities as keys 

        for pos, const in self.poss.items():    #looping through the dictionary
            for c in const:                     #looping through each constraint
                self.constraints[c].add(pos)    #add the possibility to each constraint set

        for (r,c), value in np.ndenumerate(self.values):
            if value != '.':                             #check for non-empty cells in the sudoku puzzle
                self.remove_poss(((r,c),int(value)))     #remove the invalid possibilities from the constraint set
        
        constraints = self.constraints.keys()
        self.possibilities = []                     #list that will contain possibilities of the constraints
        for pos in self.constraints.values():       #loop through the possibilities of the constraints
            for p in pos:                           #for each possibility
                if p not in self.possibilities:     #iif p not in the possibilities list
                    self.possibilities.append(p)    #add it to the list 

        #constraint matrix that contains 1 if constraint belongs to a possibility else 0
        #think of the possibilities as rows and the constraints as columns
        self.matrix = [[1 if const in self.poss[pos] else 0 for const in constraints] for pos in self.possibilities]

    def get_matrix(self):
        """Returns the constraint possibility matrix."""
        return self.matrix
    
    def get_poss(self):
        """Returns the possibilities list."""
        return self.possibilities


class Node:
    """Represents the cells in the constraint possibilities matrix that have a 1."""
    def __init__(self, number, location, headspacer=None, tailspacer=None):
        self.num = number            #number that identifies the node
        self.location = location     #location of the node in the constraints matrix (i,j)
        self.headspacer = headspacer #headspacer that opens the row the node belongs to
        self.tailspacer = tailspacer #tailspacer that closes off the row the node belongs to
        
    def deattach(self):
        """Deattach the node vertically."""
        self.up.down = self.down
        self.down.up = self.up
    
    def attach(self):
        """Attach the node vertically."""
        self.down.up = self.up.down = self

    def get_x(self):
        """Get the tuple with the i & j location of the node."""
        return self.location[0]
        
    def __str__(self):
        return '{}'.format(self.num)
    
class Head:
    """Represents the columns of the constraint possibilities matrix. 
    Which are the constraints."""
    def __init__(self, col): 
        self.col = col
    
    def deattach(self):
        """Deattach the node horizontally."""
        self.left.right = self.right
        self.right.left = self.left
        
    def attach(self):
        """Attach the node horizontally."""
        self.right.left = self.left.right = self
        
    def __str__(self):
        return '{}'.format(self.col)
    
#------------------------------------------------------------------------------
    
class SparseMatrix:
    """Represent cells in a sparse matrix with 1's using nodes.
    Represent rows and columns using doubly linked lists.
    """
    def createLeftRightLinks(self, heads):
        """Circularly link cells in a row."""
        n = len(heads)
        for j in range(n):
            heads[j].right = heads[(j + 1) % n]
            heads[j].left = heads[(j - 1 + n) % n]
    
    def createUpDownLinks(self, scols):
        """Circularly link cells in a column."""
        for scol in scols:
            n = len(scol)
            for i in range(n):
                scol[i].down = scol[(i + 1) % n]
                scol[i].up = scol[(i - 1 + n) % n]
                scol[i].head = scol[0]
                
    def createSpacers(self, srow):
        """Create the headspacers and tailspacers that open and close rows."""
        n = len(srow)
        for i in range(n):
            srow[i].headspacer = self.spacer
            srow[i].tailspacer = self.nexts
                
            
    def __init__(self, mat):
        self.mat = mat            #the sparse matrix representing constraints and possibilities
        nrows = len(self.mat)     #number of rows
        ncols = len(self.mat[0])  #number of columns
        
        srows = [[] for _ in range(nrows)] #each list represents a row 
        heads = [Head(j) for j in range(1,ncols+1)] #contains column head objects
        scols = [[head] for head in heads] 
        self.spacer = len(heads) + 1 
        self.nexts = self.spacer + 1
        self.my_dict = {}         #dictionary that contains node number as key and node as value    
        
        #Head of the column heads
        self.head = Head(0)  #Head sentinel
        heads = [self.head] + heads  #Add the head sentinel to the heads list
        
        self.createLeftRightLinks(heads) #circularly linking the column heads
        
        #Populate srow and scol with nodes that reprecent cells in the matrix that have a 1
        for i in range(nrows):
            for j in range(ncols):
                if mat[i][j] == 1:
                    node = Node(self.nexts, (i,j))
                    self.my_dict[self.nexts] = node
                    self.nexts += 1
                    scols[j].append(node) #populate each column list with a node 
                    srows[i].append(node) #populate each row list with a node
            self.createSpacers(srows[i]) #Create head and tail spacers for each node
          
            self.spacer = self.nexts
            self.nexts = self.spacer + 1
                    
        # self.createSpacers(srows) #Create head and tail spacers for each node
        self.createUpDownLinks(scols) #Circularly link each column
        
    def get_matrix(self):
        """Get the head sentinel."""
        return self.head
    
    def get_dict(self):
        """Get the dicitonary that contains node numbers and nodes."""
        return self.my_dict
    
#------------------------------------------------------------------------------

class NodeIterator:
    """Iterate through nodes."""
    def __init__(self, node):
        self.curr = self.start = node
        
    def __iter__(self):
        return self
    
    def __next__(self):
        _next = self.move(self.curr)
        if _next == self.start: #if we get back to the beginning during iteration
            raise StopIteration
        else:
            self.curr = _next #update the current node to the next one
            return _next
        
    def move(self):
        raise NotImplementedError()
        
    
class DownIterator(NodeIterator):
    """Iterate downwards in a column."""
    def move(self, node):
        return node.down
    
class UpIterator(NodeIterator):
    """Iterate upwards in a column."""
    def move(self, node):
        return node.up
    
#------------------------------------------------------------------------------

class DancingLinks:
    """Implement the algorithm X."""
    def cover(self, col):
        """Cover a column."""
        col.deattach()
        for row in DownIterator(col):        #loop downwards in a column
            for number in range(row.headspacer + 1, row.tailspacer): #check for other nodes in the row
                if number == row.num:
                    continue                   #don't deattach the initial node
                self.my_dict[number].deattach()   #deattach the node
                
                
    def uncover(self, col):
        """Uncover a column."""
        for row in UpIterator(col):           #loop upwards in a column
            for number in range(row.tailspacer - 1, row.headspacer, -1):  #check for nodes in the row
                if number == row.num:
                    continue
                self.my_dict[number].attach()     #attach the node
        col.attach()
    
    def backtrack(self):
        """Cover each column recursively."""
        col = self.head.right               # cover the first uncovered item
        if col == self.head:                # no column left
            return True
        if col.down == col:                 # no rows left to cover a column
            return False
        
        self.cover(col)
        
        for row in DownIterator(col):
            """Loop through each row and attempt to get a solution."""
            for cell in range(row.num + 1, row.tailspacer): #iterate through the columns on the right that have a cell to the right 
                self.cover(self.my_dict[cell].head) #cover the column 
                
            if self.backtrack(): #check if a solution has been found recursively
                self.solution.append(row)  #append the row to the solution list
                return True
            
            for cell in range(row.tailspacer-1, row.num, -1): 
                self.uncover(self.my_dict[cell].head) #if not found a solution uncover the column
                
        self.uncover(col)
       
        return False  #if no solution found return False
    
    def __init__(self, head, my_dict):
        self.head = head  #sparse constraint matrix that is represented as a doubly linked list
        self.my_dict = my_dict
        self.solution = []  #list that will contain nodes representing solutions 
        
    def get_solution(self):
        """Call the backtrack function and if a solution has been found append it to the solution list."""
        if self.backtrack():
            return self.solution
        print('No solution found.')


class Sudoku:
    """Solves a sudoku puzzle and returns the solved puzzle."""
    def __init__(self, puzzle):
        self.puzzle = puzzle
        a = ConstraintsMatrix(self.puzzle)  #create the constraints possibilities matrix
        self.matrix = a.get_matrix()  #constraints possibilities matrix
        self.possibilities = a.get_poss() #possibilities list

    def solve(self):
        """Solve and return the puzzle."""
        possibilities = self.possibilities
        sm = SparseMatrix(self.matrix)
        dance = DancingLinks(sm.get_matrix(), sm.get_dict())
        for node in dance.get_solution():
            i, j = possibilities[node.get_x()][0][0], possibilities[node.get_x()][0][1]
            self.puzzle[i][j] = str(possibilities[node.get_x()][1])
        return self.puzzle

             

if __name__ == '__main__':
    board = [["5","3",".",".","7",".",".",".","."],
             ["6",".",".","1","9","5",".",".","."],
             [".","9","8",".",".",".",".","6","."],
             ["8",".",".",".","6",".",".",".","3"],
             ["4",".",".","8",".","3",".",".","1"],
             ["7",".",".",".","2",".",".",".","6"],
             [".","6",".",".",".",".","2","8","."],
             [".",".",".","4","1","9",".",".","5"],
             [".",".",".",".","8",".",".","7","9"]]
    b = Sudoku(board)
    print(b.solve())