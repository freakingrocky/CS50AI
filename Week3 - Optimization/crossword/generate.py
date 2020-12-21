import sys

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        # Iterating through all crossword variables
        for variable in self.domains.keys():
            # Iterating through all of the variable's domains
            for domain in self.domains[variable].copy():
                # If the legnth of the domain is not the legnth of variable
                if variable.length != len(domain):
                    # Remove that domain
                    self.domains[variable].remove(domain)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """ 
        # Getting the overlaps
        i, j = self.crossword.overlaps[x, y]
        # Iterating through the domains of x variable
        for x_domain in self.domains[x].copy():
            # Iterating through the domains of y variable
            for y_domain in self.domains[y]:

                # If the overlap has same value for the domain
                if x_domain[i] == y_domain[j]:
                    # No change is needed, return False
                    return False
            # If the overlap has different value for the domain, remove it
            self.domains[x].remove(x_domain)
        # If it gets here, changes were made, return True
        return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """ 
        # Initializing a queue of variables
        queue = [] if arcs is None else arcs

        # If queue is empty, populate the queue with all arcs in the problem
        if not arcs:
            # Iterating through all variables in the problem
            for variable in self.crossword.variables:
                # Iterating through all the variable's neighbors
                for neighbor in self.crossword.neighbors(variable):
                    # If the variable, neighbor pair is not in the queue
                    if not (variable, neighbor) in queue:
                        # Add them to the queue
                        queue.append((variable, neighbor))

        # Keep iterating until queue is not empty
        while queue:
            # Removing the first element from queue, queue is FIFO
            x, y = queue.pop(0)
            # If a revision was made to make x arc consistent with y
            if self.revise(x, y):
                # Adding all of x's neighbors in queue to ensure consistency after revision
                for neighbor in self.crossword.neighbors(x) - {y}:
                    queue.append((neighbor, x))

        # Iterating through the domains
        for value in self.domains.values():
            # If any domain is empty
            if not len(value):
                return False

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """ 
        # If all variables in crossword are assigned,
        # The legnth of the assignment and variables would be the same.
        if len(assignment) == len(self.crossword.variables):
            return True
        # If assignment is not complete, return False
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """ 
        # Iterating through all the variables in assignment
        for variable in assignment.keys():
            # Getting the domain of variable
            word = assignment[variable]
            # Iterating through all the variables in assignment again
            for var in assignment.keys():
                # Getting the domain of var
                w = assignment[var]
                # If var and variable are same, continue
                if var == variable:
                    continue

                # Get the overlaps, if None, continue
                try:
                    (i, j) = self.crossword.overlaps[variable, var]
                except TypeError:
                    continue

                # If the overlap does not match, return False
                if word[i] != w[j]:
                    return False

        # If the overlap matches, return True
        return True

    def order_domain_values(self, var, assignment):
        """ 
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Crearting a dictionary to store constraints set by domain
        constraining = {}
        # Iterating through the domain of variable
        for word in self.domains[var]:
            # Setting intial constraints set by domain to 0
            constraining[word] = 0
            # Checking constraints set by domain
            # Iterating through the neighbors except variables already assigned
            for neighbor in (self.crossword.neighbors(var) - set(assignment)):
                # Getting the overlap
                i, j = self.crossword.overlaps[var, neighbor]
                # Iterating through the domain of the nrighbors
                for w in self.domains[neighbor]:
                    # Checking if the overlap has different values for each domain
                    if word[i] != w[j]:
                        # If the overlap does not match, add the constraints set by the domain
                        constraining[word] += 1

        # Returning a sorted list
        return sorted(constraining.keys(), key=constraining.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Crearting a dictionary to store the no. of domains in the variable
        unassigned_variables = {}

        # Iterating through all the variables
        for variable in self.crossword.variables:
            # Only adding the variables not already assigned
            if variable not in assignment:
                # Adding the variable, their domain and the no. of neighbors they have
                unassigned_variables[variable] = [len(self.domains[variable]),
                                                  len(self.crossword.neighbors(variable))]

        # Initializing a dictionary to store the unassigned_variables sorted by their neighbor count
        unassigned_variables_sorted = {}

        # Populating the unassigned variable sorted dictionary in correct order
        for i in sorted(unassigned_variables,
                        key=lambda var: unassigned_variables[var][1],
                        reverse=True):
            unassigned_variables_sorted[i] = unassigned_variables[i]

        # The min function returns the first encountered minimum value
        # In here, the min function sorts only on the basis of the no. of domains
        # The first value encountered will be the one with highest degree thanks to the
        # Sorted dictionary
        # Return the variable according to given specifications
        return min(unassigned_variables_sorted,
                   key=lambda var: unassigned_variables_sorted[var][0])

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base Case, if assignment is complete, problem is solved
        if self.assignment_complete(assignment):
            # Return that assignment
            return assignment
        
        # Simply get an unassinged variable
        var = self.select_unassigned_variable(assignment)
        # Iterate through the domain of that variable
        for value in self.order_domain_values(var, assignment):
            # Creating a copy of assignment
            tmp = assignment.copy()
            # Updating the copy of assignment with the value selected
            tmp[var] = value
            # If the updated assignment is consistent
            if self.consistent(tmp):
                # Call the function again until we get a complete assignment
                result = self.backtrack(tmp)
                # If the result is not None
                if result is not None:
                    # Return the result
                    return result

        # If the function reaches here, that means ther is no solution
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
