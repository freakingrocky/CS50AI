import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def person_genes(person, one_gene, two_genes):
    """Return the no. of genes in a person."""
    if person in one_gene:
        return 1
    if person in two_genes:
        return 2
    return 0


# Lookup table for gene probability.
lookup_table = {
    '1': {'1': [0.5, 0.5],
          '0': [PROBS["mutation"], 1 - PROBS["mutation"]],
          '2': [1 - PROBS["mutation"], PROBS["mutation"]]},

    '2': {'1': 0.5, '0': PROBS["mutation"], '2': 1 - PROBS["mutation"]},

    '0': {'1': 0.5, '0': 1 - PROBS["mutation"], '2': PROBS["mutation"]}
}


def calculate_gene_probability(person_gene_count, father_gene_count, mother_gene_count):
    """Return the gene probability."""
    # Gets the lookup table for required operation.
    lookup = lookup_table[str(person_gene_count)]
    # If the person_gene_count is 1, the formula is a bit different.
    if person_gene_count == 1:
        father_probability = lookup[str(father_gene_count)]
        mother_probability = lookup[str(mother_gene_count)]

        return (father_probability[0] * mother_probability[1] + father_probability[1] * mother_probability[0])

    # If the person_gene_count is 0 or 2,it is a simple multiplication.
    father_probability = lookup[str(father_gene_count)]
    mother_probability = lookup[str(mother_gene_count)]

    return (father_probability * mother_probability)


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Variable to keep the product of each event's probability.
    joint_probability = 1

    for person in people:
        # Getting father and mother of the person
        father = people[person]["father"]
        mother = people[person]["mother"]

        # Getting gene count in father and mother
        father_gene_count = person_genes(father, one_gene, two_genes)
        mother_gene_count = person_genes(mother, one_gene, two_genes)
        person_gene_count = person_genes(person, one_gene, two_genes)

        # If father and mother are None, simply using provided unconditional probabilities.
        if father is None and mother is None:
            c = person_genes(person, one_gene, two_genes)
            joint_probability *= (PROBS["gene"][c] * PROBS["trait"][c][person in have_trait])
            continue

        # Calculating probability that the person has 1 gene
        gene_probability = calculate_gene_probability(person_gene_count, father_gene_count, mother_gene_count)

        # Calculating probability of trait
        trait_probability = PROBS["trait"][person_gene_count][person in have_trait]

        # Probability of event.
        joint_probability *= (trait_probability * gene_probability)

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        person_gene_count = person_genes(person, one_gene, two_genes)

        probabilities[person]["gene"][person_gene_count] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    """
    Logic behind normaization:

    x * 1/x = 1
    Here, x is the sum of all probabilities.
    1/x becomes the normalizing_constant.
    We multiply this normailizing_constant with the individual probabilities.
    This preserves the ratio and their sum becomes 1.
    """
    for person in probabilities:
        gene_probabilities_sum = sum(probabilities[person]["gene"].values())
        normalizing_constant = 1/gene_probabilities_sum
        for gene, probability in probabilities[person]["gene"].items():
            # gene values are range(0,3) and probability is the item of the dictionary.
            probabilities[person]["gene"][gene] = probability * normalizing_constant

        trait_probabilities_sum = sum(probabilities[person]["trait"].values())
        normalizing_constant = 1/trait_probabilities_sum
        for trait, probability in probabilities[person]["trait"].items():
            # trait values are True and False and probability is the item of the dictionary.
            probabilities[person]["trait"][trait] = probability * normalizing_constant


if __name__ == "__main__":
    main()
