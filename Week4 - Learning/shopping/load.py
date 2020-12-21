"""
Just checking out some methods.
"""
import csv

lookup_table = {
    'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3,
    'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7,
    'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11,
    'TRUE': 1, 'FALSE': 0, 'Returning_Visitor': 1,
    'New_Visitor': 0
}

def format(item_data):
    tmp = []
    # print(item_data)
    tmp.append(int(item_data[0]))
    tmp.append(float(item_data[1]))
    tmp.append(int(item_data[2]))
    tmp.append(float(item_data[3]))
    tmp.append(int(item_data[4]))
    tmp.append(float(item_data[5]))
    # Bounce Rates
    tmp.append(float(item_data[6]))
    tmp.append(float(item_data[7]))
    tmp.append(float(item_data[8]))
    tmp.append(float(item_data[9]))
    # Month
    tmp.append(lookup_table[item_data[10]])
    tmp.append(int(item_data[11]))
    tmp.append(int(item_data[12]))
    tmp.append(int(item_data[13]))
    tmp.append(int(item_data[14]))
    # Visitor Type
    tmp.append(lookup_table[item_data[15]])
    tmp.append(lookup_table[item_data[16]])
    return tmp

def load(filename):
    with open(filename, 'r') as database:
        data = csv.DictReader(database)
        labels = []
        print("Dunder Methods: \n", dir(data), '\n')
        print("Elements: \n", list(dict(next(data)).values())[:-1], '\n')
        print("Size: \n", data.__sizeof__(), '\n')
        # exit()
        evidence = []
        for item in data:
            item = dict(item)
            item_data = list(item.values())
            evidence.append(format(item_data[:-1]))
            labels.append(lookup_table[item_data[-1]])

            print("Evidence: \n", evidence, '\n')
            print("Labels: \n", labels)
            exit("\nOne Iteration Complete")

        return (evidence, labels)


print(load('shopping.csv'))

"""
A lot like a generator.
It is an iterable.
"""
