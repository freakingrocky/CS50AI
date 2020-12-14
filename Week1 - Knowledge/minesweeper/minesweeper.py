import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        
        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # Removes mine from sentence
            self.cells.remove(cell)
            # Decreasing count by 1
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # Removing safe from sentence
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Marking the cell as a move that has been made and safe.
        self.moves_made.add(cell)   # Marking the cell as a move made.
        self.mark_safe(cell)    # Maeking the cell as safe.
        
        # Adding a new sentence to the AI's knowledge base.
        new_sentence = Sentence(self.neighboring_cells(cell), count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)
        
        # Marking additional cells as per AI's knowledge base.
        for sentence in self.knowledge:
            for safe_cell in sentence.known_safes():
                self.mark_safe(safe_cell)
            for mine in sentence.known_mines():
                self.mark_mine(mine)

        # If all 8 mines are found, everything else is safe.
        if len(self.mines) == 8:
            for h in range(self.height):
                for b in range(self.width):
                    if (h, b) in self.moves_made:
                        continue
                    if (h, b) in self.mines:
                        continue
                    if (h, b) in self.safes:
                        continue
                    self.mark_safe((h, b))

        # Drawing new inferences.
        if len(self.mines) != 8:
            sentences = []
            for sentence in self.knowledge:
                if sentence.cells == set():
                    self.knowledge.remove(sentence)
                    continue
                for s in self.knowledge:
                    if s == sentence:
                        continue
                    if len(s.cells) >= len(sentence.cells):
                        continue
                    if sentence.cells.issubset(s.cells):
                        tmp_set = s.cells.difference(sentence.cells)
                        tmp_count = s.count - sentence.count
                        sentences.append(Sentence(tmp_set, tmp_count))

            for sentence in sentences:
                if sentence not in self.knowledge:
                    self.knowledge.append(sentence)

        # Debugging
        print("No. of known mines:", len(self.mines))
        print("No. of known safes:", (len(self.safes) - len(self.moves_made)))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # If there are no safe cells known, return None
        if not self.safes:
            return None
        # Iterating through safe cells.
        for safe in self.safes:
            # Checking if cell is in previously made moves.
            if safe not in self.moves_made:
                # If not a previously made move and safe, return cell.
                return safe
        # All safe cells are previously made moves, returns None.
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Creating an empty list to store possible legal moves.
        possible_moves = []
        # Iterating through the whole board.
        for i in range(self.height):
            for j in range(self.width):
                # If the cell is a mine, continue
                if(i, j) in self.mines:
                    continue
                # If the cell is not a previously made move,
                if (i, j) not in self.moves_made:
                    # Add to the legal moves list.
                    possible_moves.append((i, j))
        # If there are no legal moves, return None.
        if not possible_moves:
            return None
        # Return random move.
        return random.choice(possible_moves)
    
    def neighboring_cells(self, cell):
        """
        Return a set of safe neighboring cells inside the border.
        """
        # Unpacking the set into 2 variables.
        h, b = cell
        # Creating an empty set to store neighbors.
        neighbors = set()
        # Iterating through the cells 1 cell apart.
        for i in range(h-1, h+2):
            for j in range(b-1, b+2):
                # Making sure the cell is in the board.
                if (i >= self.height) or (j >= self.width):
                    continue
                if (i < 0) or (j < 0):
                    continue
                # Making sure it's not the cell itself.
                if (i, j) == (h, b):
                    continue
                # Making sure this move is not already made.
                if (i, j) in self.moves_made:
                    continue
                if (i, j) in self.safes:
                    continue
                # Adding safe neighboring cells into set.
                neighbors.add((i, j))
        # Finally, returning neighbors set.
        return neighbors

