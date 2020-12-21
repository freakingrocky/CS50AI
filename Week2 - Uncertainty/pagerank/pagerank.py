import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename), encoding="utf-8") as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initializing a dictionary to store probability of pages
    probabilities = {}

    # If there are no links in the page.
    # Final probability becomes 1/no. of pages
    if not corpus[page]:
        for p in corpus:
            probabilities[p] = 1/len(corpus)
        return probabilities

    # Calculate the dampening probability of each page
    damping_probability = ((1 - damping_factor)/len(corpus.keys()))

    # Setting the initial probability of randomly choosing any page in corpus.
    for p in corpus:
        probabilities[p] = damping_probability

    # Updating probabilities according to links in page
    for links in corpus[page]:
        probabilities[links] += ((1 - damping_probability)/len(corpus[page]))

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initializing a dictionary to store sample probability of each page.
    samples = dict().fromkeys(list(corpus), 0)

    # Choosing first page at random
    sample = random.choice(list(corpus))
    samples[sample] += 1

    # Gathering n samples
    for i in range(n - 1):
        probabilities = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(probabilities.keys()),
                                weights=probabilities.values(), k=1)[0]
        samples[sample] += 1

    # Normalizing samples sum to 1, preserving the ratio
    normalizing_factor = 1/sum(samples.values())
    for page in samples:
        samples[page] *= normalizing_factor

    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initializing a dictionary to store probability of pages
    probabilities = {}

    # Assigning each page probability of 1/N.
    for p in corpus:
        probabilities[p] = 1/len(corpus)

    # A variable as the base state for the while loop.
    stop = False

    # Iterating an solving formula.
    while not stop:
        tmp = dict(probabilities)
        # Getting all the pages that link to it.
        for page in probabilities:
            # Creating an empty list to store pages that link to it.
            pages = []
            # Iterating through all the pages in the corpus.
            for p in corpus:
                # If the page contains a link to the current page
                if page in corpus[p]:
                    pages.append(p)

            # Calculating the part one of the equation.
            part_one = ((1 - damping_factor)/len(corpus))

            # Since the second part is a summation,
            # i.e. iteratively adding the second part of the formula.
            part_two = 0  # Initializing a variable to store the summation.
            for p in pages:
                part_two += tmp[p]/len(corpus[p])

            # Updating the probability of the page.
            probabilities[page] = part_one + (part_two * damping_factor)

            # If the change is less than 0.001
            if abs(probabilities[page] - tmp[page]) < 0.001:
                # Stop the loop. Base state satisfied.
                stop = True

    # Normalizing Values.
    normalizing_factor = 1/sum(probabilities.values())
    for page in probabilities:
        probabilities[page] *= normalizing_factor

    return probabilities


if __name__ == "__main__":
    main()
