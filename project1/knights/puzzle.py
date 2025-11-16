from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# general knowledge / rules of the game to be added to every knowledge base
general_knowledge = And(
    # a is either a knight or a knave
    Or(AKnight, AKnave),
    # but not both
    Not(And(AKnight, AKnave)),
    # b is either a knight or a knave
    Or(BKnight, BKnave),
    # but not both
    Not(And(BKnight, BKnave)),
    # c is either a knight or a knave
    Or(CKnight, CKnave),
    # but not both
    Not(And(CKnight, CKnave)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
A_statement = And(AKnight, AKnave)
knowledge0 = And(
    general_knowledge,
    # "I am both a knight and a knave." from a knight's perspective who always tells thge truth
    Implication(AKnight, A_statement),
    # "I am both a knight and a knave." from a knave's perspective who always lies
    Implication(AKnave, Not(A_statement)),
)

# Puzzle 1
# A says "We are both knaves."
A_statement = And(AKnave, BKnave)
# B says nothing.
B_statement = None

knowledge1 = And(
    general_knowledge,
    # A says "We are both knaves." from a knight's perspective who always tells the truth
    Implication(AKnight, A_statement),
    # A says "We are both knaves." from a knave's perspective who always lies
    Implication(AKnave, Not(A_statement)),
)

# Puzzle 2
# A says "We are the same kind."
A_statement = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
B_statement = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    general_knowledge,
    # A says "We are the same kind." from a knight's perspective
    Implication(AKnight, A_statement),
    # A says "We are the same kind." from a knave's perspective
    Implication(AKnave, Not(A_statement)),

    # B says "We are of different kinds." from a knight's perspective
    Implication(BKnight, B_statement),
    # B says "We are of different kinds." from a knave's perspective
    Implication(BKnave, Not(B_statement)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
A_statement = Or(AKnight, AKnave)

# B says "A said 'I am a knave'."
# B says "C is a knave."
B_statement = And(
    AKnave,
    CKnave,
)

# C says "A is a knight."
C_statement = Implication(CKnight, AKnight)

knowledge3 = And(
    # TODO
    general_knowledge,
    # A says either "I am a knight." or "I am a knave." from a knight's perspective
    Implication(AKnight, A_statement),
    # A says either "I am a knight." or "I am a knave." from a knight's perspective
    Implication(AKnave, Not(A_statement)),

    # B says "A said 'I am a knave'." if B is a knight and a is a knight
    Implication(BKnight, B_statement),
    # B says "A said 'I am a knave'." if B is a knight and a is a knave
    Implication(BKnave, Not(B_statement)),

    # C says "A is a knight." If C is a knight
    Implication(CKnight, C_statement),
    # C says "A is a knight." If C is a knave
    Implication(CKnave, Not(C_statement)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        # print(knowledge.formula())
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
