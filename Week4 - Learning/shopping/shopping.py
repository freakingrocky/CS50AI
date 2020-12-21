import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


# Lookup table for formatting the csv data
lookup_table = {
    'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3,
    'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7,
    'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11,
    'TRUE': 1, 'FALSE': 0, 'Returning_Visitor': 1,
    'New_Visitor': 0, 'Other': 0
}


def format(item_data):
    """Return a formatted list from unformatted list."""
    # Creating an empty temporary list to start with
    tmp = []

    # Appending data according to item index and type
    tmp.append(int(item_data[0]))
    tmp.append(float(item_data[1]))
    tmp.append(int(item_data[2]))
    tmp.append(float(item_data[3]))
    tmp.append(int(item_data[4]))
    tmp.append(float(item_data[5]))
    tmp.append(float(item_data[6]))
    tmp.append(float(item_data[7]))
    tmp.append(float(item_data[8]))
    tmp.append(float(item_data[9]))
    tmp.append(lookup_table[item_data[10]])
    tmp.append(int(item_data[11]))
    tmp.append(int(item_data[12]))
    tmp.append(int(item_data[13]))
    tmp.append(int(item_data[14]))
    tmp.append(lookup_table[item_data[15]])
    tmp.append(lookup_table[item_data[16]])

    # Finally, return a formatted list
    return tmp


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Opening the csv file
    with open(filename, 'r') as database:
        # Loading data, returns a dict_reader object
        data = csv.DictReader(database)

        # Creating empty lists for label and evidence
        labels = []
        evidence = []

        # Going through each item in the dict_reader object
        for item in data:
            # Getting an ordered dictionary from item
            item = dict(item)
            # Item data will be the values of the dictionary
            item_data = list(item.values())
            # Calling format function on item_data and adding it to evidence
            evidence.append(format(item_data[:-1]))
            # Adding the label according to lookup_table
            labels.append(lookup_table[item_data[-1]])

        # Finally, returning required lists
        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Using sckit-learn to create a classifier
    classifier = KNeighborsClassifier(n_neighbors=1)
    # Running the classifier
    return classifier.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Initializing integers to 0 for sensitivity & specificity
    sens = 0
    spec = 0

    # Initializing integers to 0 for prediction values
    purchase = 0
    not_purchase = 0

    # Iterating through all the labels and predictions
    for label, prediction in zip(labels, predictions):
        # If prediction is correct
        if label == prediction:
            # If the user did purchase something
            if prediction == 1:
                # Increase sens by 1
                sens += 1
            # If the user did not purchase anything
            else:
                # Increase spec by 1
                spec += 1

        # If prediction was the user purchases something
        if prediction == 1:
            # Increase purchase by 1
            purchase += 1
            # and continue to next label, prediction
            continue
        # If prediction was the user does not purchase anything,
        # Increase not_purchase by 1
        not_purchase += 1

    return ((sens/purchase), (spec/not_purchase))


if __name__ == "__main__":
    main()
