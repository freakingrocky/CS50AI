import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP | S PP S

NP -> N | Det N | Adj NP | NP P NP | P NP | NP Adv | Det AdjP N | P Det N
AdjP -> Adj | Adj Adj | Adj Adj Adj
PP -> P NP | P
VP -> V | V NP | Adv VP | VP Adv | Adv V NP | VP NP Adv | VP P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Getting a list of lowercase words/characters from sentence
    words = nltk.word_tokenize(sentence.lower())
    # Iterating through the unique words in the list
    for word in set(words):
        # If the word does not contain at least one alphabet
        if not any(char.isalpha() for char in word):
            # Remove all occurances of that word
            while word in words:
                words.remove(word)
    # Return the list of words
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Initializing an empty list to store the noun phrase chunks
    chunks = []
    # Iterating through all the subtrees in the tree
    for subtree in tree.subtrees():
        # If the the subtree is a noun phrase
        if subtree.label() == "NP" and check_nested_np(subtree):
            # Append the subtree
            chunks.append(subtree)
    # Return the list of all noun phrase chunks in the sentence tree
    return chunks


def check_nested_np(tree):
    """
    Helper function for np_chunk
    
    Checks for np chunks inside of tree
    """
    np = 0
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            np += 1
        if np > 1:
            return False
    return True

if __name__ == "__main__":
    main()
