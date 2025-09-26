import sys
import random

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """ 
        for var in self.crossword.variables:
            for wd in self.domains[var].copy():
                if var.length != len(wd):
                    self.domains[var].remove(wd) 

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        has_revised = False
        overlap = self.crossword.overlaps[(x,y)] 
        if overlap != None:  
            i,j  = overlap
            for wd1 in self.domains[x].copy():
                if not any(wd1[i] == wd2[j] for wd2 in self.domains[y]):
                    self.domains[x].remove(wd1)
                    has_revised = True
        return has_revised        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
  
        if arcs == None:      
            arcs = []
            for v1 in  self.crossword.variables:
                for v2 in self.crossword.variables:
                    if v1 != v2 and self.crossword.overlaps[(v1,v2)]:
                        arcs.append((v1, v2)) 
        while arcs:
            (x,y) = arcs[0]
            arcs = arcs[1:] 
            # if no domains left no solution
            if self.revise(x, y):                
                if len(self.domains[x]) == 0:
                    return False  
                for v1 in  self.crossword.variables:
                    if v1 != x and v1 != y and self.crossword.overlaps[(v1, x)]:
                        arcs.append((v1, x)) 
        return True    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """ 
        if assignment:       
            return assignment.keys() == self.crossword.variables and all(v != None for v in assignment.values()) 
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """ 
        for v in assignment: 
            if v.length != len(assignment[v]):
                return False
            
        if len(set(assignment.values())) != len(assignment.values()):
            return False
        
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2: 
                    overlap = self.crossword.overlaps[(v1, v2)]
                    if overlap:
                        i, j = overlap
                        if assignment[v1][i] != assignment[v2][j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbours = self.crossword.neighbors(var).difference(assignment.keys())
        domain_values = self.domains[var]
        output = []
        
        for wd1 in domain_values:
            no_of_words_eleminate = 0
            for neighbour in neighbours: 
                overlap = self.crossword.overlaps[(var, neighbour)]
                if overlap : 
                    i, j = overlap
                    for wd2 in self.domains[neighbour]:
                        if wd1[i] != wd2[j]:
                            no_of_words_eleminate +=1
            output.append((wd1 , no_of_words_eleminate))

        return [ v[0] for v in sorted(output, key=lambda word: word[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """ 
        unassigned_variables =  [ v for v in self.crossword.variables.difference(assignment)]
        min_no_of_words = min(len(self.domains[v]) for v in unassigned_variables) 

        variables_with_min_no_of_words = [v  for v in unassigned_variables if len(self.domains[v])  == min_no_of_words]
        if len (variables_with_min_no_of_words)==1 :
            return variables_with_min_no_of_words[0]
        
        max_degree = max(len(self.crossword.neighbors(v)) for v in variables_with_min_no_of_words)
        degree_vars = [v for v in variables_with_min_no_of_words if len(self.crossword.neighbors(v)) == max_degree]

        # If tie, return any
        return random.choice(degree_vars)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):    
            return assignment
        
        unassigned_variable = self.select_unassigned_variable(assignment) 
        for wd in self.order_domain_values(unassigned_variable, assignment):
            assignment[unassigned_variable] = wd
            if self.consistent(assignment):
                backtracked_assignment = self.backtrack(assignment)
                if backtracked_assignment is not None:
                    return backtracked_assignment           
        
        return None
    
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
