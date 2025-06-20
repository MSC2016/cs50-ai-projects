import itertools
import random

DEBUG = False


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

                # Update count if cell is within game bounds and is a mine
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
        # if the count is > 0 and count equals the number of cells
        # then they are all mines
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if the count is 0 then all the cells are safe
        if self.count == 0:
            return self.cells.copy()
        return set()
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if the cell exists in this sentence, and there are mines 
        # remove the cell, and decrease the count
        if cell in self.cells and self.count > 0:
            self.count -= 1
            self.cells.remove(cell)
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # remove the safe cell if it is part of the sentence
        if cell in self.cells:
            self.cells.remove(cell)
        # raise NotImplementedError


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
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # 3) add a new sentence to the AI's knowledge base
        # get all neighbour for a given cell
        neighbours = self.get_valid_neighbours(cell)
        # remove known safes
        neighbours -= self.safes
        # remove known mines
        for mine in self.mines:
            if mine in neighbours:
                neighbours.remove(mine)
                count -= 1
        # append the new sentence to the knowledge base
        self.knowledge.append(Sentence(neighbours, count))
        #  4) mark any additional cells as safe or as mines
        if count == 0:
            for neighbor in neighbours:
                self.mark_safe(neighbor)
        # 5) add any new sentences to the AI's knowledge base
        self.inference_new_knowledge()

        for sentence in self.knowledge:
            print('sentence', sentence)

        if DEBUG:
            print('safes', self.safes)
            print('mines', self.mines)

            if len(self.mines) == 8:
                print('FOUND THEM ALL', end='')
            print('-'*50)
        # raise NotImplementedError

    def inference_new_knowledge(self):
        '''
        Test all sentences in relation to each other, searching for subsets
        if a subset is found, it creates a new sentence adds it to
        self.knowldge
        '''
        while True:
            # variable to store new sentences
            new_sentences = []

            # search subsets to infer new sentences
            for s1, s2 in itertools.combinations(self.knowledge, 2):
                # check if s1 is a subset of s2, and if the sentences are different
                if s1.cells.issubset(s2.cells) and s1.cells != s2.cells:
                    # if they are, get the difference in cells and count
                    diff = s2.cells - s1.cells
                    count = s2.count - s1.count
                    # create a new sentence made of the difference between the 2 sentences being tested
                    new_sentence = Sentence(diff, count)
                # same as the previous if statement, but this time checking if s2 is a subset of s1
                elif s2.cells.issubset(s1.cells) and s2.cells != s1.cells:
                    diff = s1.cells - s2.cells
                    count = s1.count - s2.count
                    new_sentence = Sentence(diff, count)
                else:
                    continue
                # if the new sentence is really new, and not already in self,knowledge and new_sentences, add it to self.knowledge
                if new_sentence.cells and new_sentence not in self.knowledge and new_sentence not in new_sentences:
                    new_sentences.append(new_sentence)

            # if there are no new sentences, mark safes and mark mines with update_safes_n_mines()
            # remove duplicates by calling remove_duplicates(), and break out of the loop
            if not new_sentences:
                self.update_safes_n_mines()
                break

            # add new_sentences to self.knowledge, update safes and mines, and remove duplicates
            self.knowledge.extend(new_sentences)
            self.update_safes_n_mines()

    def update_safes_n_mines(self):
        '''
        updates the known mines and known safes, using mark_mine()
        and mark_safe() functions, and remove sentences with empty
        sets from self.knowledge
        '''
        # refference all sentences in self.knowledge, and foe each sentence
        # if the count is equal to the number of mines, mark all cells in
        # the sentence as mines, if the count is zero, mark all cells in the
        # sentence as safe
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:
                for cell in sentence.cells.copy():
                    self.mark_mine(cell)
            if sentence.count == 0:
                for cell in sentence.cells.copy():
                    self.mark_safe(cell)

        # create an empty list
        unique = []
        # iterate trough all sentences in self.knowledge
        for s in self.knowledge:
            # if current sentence's cells and count are not equal to any other
            # sentence's cells and count already in unique, or if it isd in fact
            # a new sentence, add it to unique
            if not any(s.cells == u.cells and s.count == u.count for u in unique):
                unique.append(s)
        # make self.knowledge equal to unique, for all sentences that contain cells
        # or in other words, remove sentences with empty sets of cells
        self.knowledge = [s for s in unique if s.cells]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # get list of safe moves
        possible_moves = list(self.safes - self.moves_made)
        # if there are safe moves that can be made, randomly return one of them
        if possible_moves:
            return random.choice(possible_moves)
        return None
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # create an ampty list to hold possible moves
        possible_moves = []
        # iterate trough all positions in the board, if the position
        # is not a mine, or a move that has been made, add it to the
        # list, randomly select one of them and return it.
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.append((i, j))
        if possible_moves:
            return random.choice(possible_moves)
        return None
        # raise NotImplementedError

    def get_valid_neighbours(self, cell):
        """
        Returns a list of all neighbours for given cell.

        """
        # iterate trough all the neighbours of a given cell
        # and if the position is not out of bounds, add it 
        # to the valid neighbours set, and return the set
        i, j = cell
        valid_neighbours = set()
        for line in range(i - 1, i + 2):
            for col in range(j - 1, j + 2):
                # ignore the cell passed to this function
                if line == i and col == j:
                    continue
                # ignore values below 0 (out of bounds)
                elif line < 0 or col < 0:
                    continue
                # ignore values above height and width (out of bounds)
                elif line >= self.height or col >= self.width:
                    continue
                else:
                    # add what remains to the valid neighbours set
                    valid_neighbours.add((line, col))
        return valid_neighbours
