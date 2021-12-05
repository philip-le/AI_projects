import itertools
import random
import copy


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

    def __subset__(self, other):
        if len(self.cells) > 0: 
            return self.cells.issubset(other.cells)
        else:
            return False

    def create_new_sentence(self, other):
        """If the first sentence is a proper subset of second sentence, then create a new one"""
        if (len(other.cells) > len(self.cells)) & (len(self.cells) > 0) & (self.cells.issubset(other.cells) & (other.count >= self.count)):
            return Sentence(other.cells - self.cells, other.count - self.count)

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (len(self.cells) == self.count) & (self.count != 0):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (self.count == 0) & (len(self.cells) > 0):
            return self.cells
        else:
            return set()


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if (cell in self.cells) & (self.count >= 1):
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
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
            if (len(sentence.cells) > 0) & (cell in sentence.cells):
                for ncell in sentence.known_mines():
                    self.mines.add(ncell)


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if (len(sentence.cells) > 0) & (cell in sentence.cells):
                for ncell in sentence.known_safes():
                    self.safes.add(ncell)

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
        self.moves_made.add(cell)
        self.mark_safe(cell)

        #3
        cells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.safes and (i, j) not in self.moves_made:
                        if (i, j) not in self.mines: 
                            cells.add((i,j))
                        else:
                            count -= 1
        

        new_sentence = Sentence(cells, count)
        print(f"Original: {new_sentence}")        
        current_knowledge = self.knowledge.copy()

        self.knowledge.append(new_sentence)

        sentence_know_mines = new_sentence.known_mines().copy()
        sentence_know_safes = new_sentence.known_safes().copy()

        for acell in sentence_know_mines:
            self.mark_mine(acell)

        for acell in sentence_know_safes:
            self.mark_safe(acell)


        for other_sentence in current_knowledge:
            if new_sentence.__subset__(other_sentence) & (not new_sentence.__eq__(other_sentence)):
                another_sentence = new_sentence.create_new_sentence(other_sentence)
                if (another_sentence not in self.knowledge) & (len(another_sentence.cells)>0):
                    print(f"BInfer: {another_sentence}")
                    self.knowledge.append(another_sentence)

                    another_sentence_know_mines = another_sentence.known_mines().copy()
                    another_sentence_know_safes = another_sentence.known_safes().copy()

                    for acell in another_sentence_know_mines:
                        self.mark_mine(acell)
                    for acell in another_sentence_know_safes:
                        self.mark_safe(acell)


            elif other_sentence.__subset__(new_sentence) & (not other_sentence.__eq__(new_sentence)):
                another_sentence = other_sentence.create_new_sentence(new_sentence)
                if (another_sentence not in self.knowledge) & (len(another_sentence.cells)>0):
                    print(f"SInfer: {another_sentence}")
                    self.knowledge.append(another_sentence)
                    
                    another_sentence_know_mines = another_sentence.known_mines().copy()
                    another_sentence_know_safes = another_sentence.known_safes().copy()

                    for acell in another_sentence_know_mines:
                        self.mark_mine(acell)
                    for acell in another_sentence_know_safes:
                        self.mark_safe(acell)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made - self.mines
        print(f"Current set of predicted mines: {self.mines}")
        print(f"Current set of next safe moves: {safe_moves}")
        if len(safe_moves) > 0:
            safe_one = random.sample(safe_moves, 1)[0]
            safe_moves.remove(safe_one)
            return safe_one
        else:
            return None




    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = set((i,j) for i in range(self.height) for j in range(self.width)) - self.moves_made - self.mines
        if len(random_moves) > 0:
            safe_one = random.sample(random_moves, 1)[0]
            random_moves.remove(safe_one)
            return safe_one
        else:
            return None

    
    def getFlags(self):
        return self.mines
