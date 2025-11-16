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
        # unpack domains and iterate trough each entry
        for cross_word, possible_Words in self.domains.items():
            # get the length of each word
            target_length = cross_word.length
            # create a filtered set of node-consistent possible words for each cross word
            filtered = {word for word in possible_Words if len(word) == target_length}
            # and overwrite domain values with the new set
            self.domains[cross_word] = filtered

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # initialize return value to False
        revised = False

        # get overlap x,y
        overlap = self.crossword.overlaps[x, y]

        # if there is an overlap
        if overlap:

            # unpack the overlap into i, j
            i, j = overlap

            # initialize a set of words to remove
            words_to_remove = set()

            # for every x word
            for x_word in self.domains[x]:

                # initialize match found to false
                match_found = False

                # iterate trough every y word to see if there is match at the overlap position
                for y_word in self.domains[y]:
                    if x_word[i] == y_word[j]:
                        # set match to true if a match is found
                        match_found = True
                
                # if no matches are found, add the word to the set of words to remove from x
                if not match_found:
                    words_to_remove.add(x_word)

            # if there are words to remove, remove them and set revised to true
            if words_to_remove:
                self.domains[x] -= words_to_remove
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # if arcs == None
        if arcs is None:
            # initialize arcs to an empty set
            arcs = set()
            for var in self.domains:
                for neighbour in self.crossword.neighbors(var):
                    # iterate trough every neighbour in every variable in domains
                    # creating tuples of varible/neighbour pairs, and add them to the set
                    arcs.add((var, neighbour))

        # Iterate trough every arc, revise it and add new arcs if needed
        while arcs:
            x, y = arcs.pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x):
                        if z != x:
                            arcs.add((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # iterate trough all variables
        # return False if any variable is not in assignment, or its value is None
        for variable in self.crossword.variables:
            if variable not in assignment or assignment[variable] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # return false if there are duplicates in the words list
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False
        
        # return false if word length doesnt match the 
        for variable, word in assignment.items():
            print(variable, word)
            if len(word) != variable.length:
                return False
        

        # Check for conflicts at overlaps
        for variable in assignment:
            for other_variable in assignment:
                if variable == other_variable:
                    continue

                # If they overlap, check if the characters match
                overlap = self.crossword.overlaps.get((variable, other_variable))
                if overlap:
                    i, j = overlap
                    if assignment[variable][i] != assignment[other_variable][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Store tuples of (value, number of conflicts)
        value_conflicts = []

        for value in self.domains[var]:
            conflicts = 0
            for neighbor in self.crossword.neighbors(var):
                # Only consider unassigned neighbors
                if neighbor in assignment:
                    continue

                # If the neighbor overlaps with var, check potential conflicts
                overlap = self.crossword.overlaps.get((var, neighbor))
                if overlap:
                    i, j = overlap
                    # Count conflict if neighbor has values that would be inconsistent
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            conflicts += 1

            value_conflicts.append((value, conflicts))

        # Sort values by number of conflicts (fewest conflicts first)
        value_conflicts.sort(key=lambda x: x[1])

        # Return only the values, ordered by LCV
        return [val for val, _ in value_conflicts]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # create a local copy of all unassigned variables
        unassigned = [v for v in self.crossword.variables if v not in assignment]

        # discard all unassigned variables who's domain is larger than the smallest domain found
        smallest_domain = min(len(self.domains[var]) for var in unassigned)
        unassigned = [var for var in unassigned if len(self.domains[var]) == smallest_domain]

        # discard all unassigned variables that don't have the highest degree
        if len(unassigned) > 1:
            highest_degree = max(len(self.crossword.neighbors(var)) for var in unassigned)
            unassigned = [var for var in unassigned if len(self.crossword.neighbors(var)) == highest_degree]
        
        # return one of the remaining
        return random.choice(unassigned)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # return true if all variables are assigned
        if self.assignment_complete(assignment):
            return assignment

        # get an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # recursively call backtrack t ifill all the varibles
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)

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