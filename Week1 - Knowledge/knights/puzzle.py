from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Rules:                          Rules Logic:
#   Either a knight or a knave.     And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
#   Knight's sentences are true.    Implication(AKnight, And(sentence logic))
#   Knave's sentences are false.    Implication(AKnave, Not(And(sentence logic))

# Puzzle 0
# A says "I am both a knight and a knave."
# Sentence Logic: And(AKnight, AKnave)
knowledge0 = And(
    # Game Rules
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # A's possibilities
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# Sentence Logic: And(AKnave, BKnave)
# B says nothing.
knowledge1 = And(
    # Game Rules
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A's possibilities
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# Sentence Logic: Or(And(AKnave, BKnave), And(AKnight, BKnight))  OR Biconditional(AKnight, BKnight)
# B says "We are of different kinds."
# Sentence Logic: Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))  OR  Biconditional(AKnight, BKnave)
knowledge2 = And(
    # Game Rules
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A's possibilities
    Implication(AKnight, Biconditional(AKnight, BKnight)),
    Implication(AKnave, Not(Biconditional(AKnight, BKnight))),
    # B's possibilities
    Implication(BKnight, Biconditional(AKnight, BKnave)),
    Implication(BKnave, Not(Biconditional(AKnight, BKnave)))

    #                   OR  
    # Game Rules +
    # Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # Implication(BKnight, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# Sentence Logic: Or(AKnight, AKnave)
# B says "A said 'I am a knave'."
# Sentence Logic: Implication(AKnight, AKnave)
# B says "C is a knave."
# Sentence Logic: (CKnave)
# C says "A is a knight."
# Sentence Logic: (AKnight)
knowledge3 = And(
    # Game Rules
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # A's possibilities
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # B's possibilities
    Implication(BKnight, And(CKnight, Implication(AKnight, AKnave))),
    Implication(BKnave, Not(And(Implication(AKnight, AKnight), CKnave))),
    # C's possibilities
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
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
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
