import csv
import sys
from termcolor import cprint
from util import Node, StackFrontier, QueueFrontier
import os
from time import time, localtime

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def evaluate(source, target):
    source = person_id_for_name(source)
    target = person_id_for_name(target)
    if source is None:
        cprint("Person not found.", 'red', attrs=['bold'])
        return
    if target is None:
        cprint("Person not found.", 'red', attrs=['bold'])
        return

    path = shortest_path(source, target)

    if path is None:
        cprint("Not connected.", 'red')
    else:
        degrees = len(path)
        cprint(f"{degrees} degrees of separation.", 'green', attrs=['bold'])
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def main():
    if len(sys.argv) > 3:
        sys.exit("Usage: python degrees.py [directory] [file]")
    directory = sys.argv[1]

    start_time = localtime()
    cprint(
        f"Start Time: {start_time.tm_hour}h:{start_time.tm_min}m:{start_time.tm_sec}s", 'green')
    universal_start = time()

    start = time()
    # Load data from files into memory
    cprint(f"Loading data... {directory}", 'yellow')
    load_data(directory)
    cprint(f"Data Loaded in {round(time() - start, 4)} seconds.", 'green')

    counter = 0
    cprint("Starting Queries".center(os.get_terminal_size().columns - 5, "_"), 'green')
    with open(sys.argv[2], 'r') as actors:
        for query in actors.readlines():
            counter += 1
            start = time()
            Actors = query.replace("\n", "").split(',')
            print(f"Query No: {counter}".center(os.get_terminal_size().columns, '='))
            cprint(f"Actors: \n {Actors[0]} \n {Actors[1]}", 'green')
            evaluate(Actors[0], Actors[1])
            cprint(f"Time Taken For Query -> {round(time() - start, 4)} seconds", 'green', attrs=['bold'])

    cprint("Execution Completed Succesfully.".center(os.get_terminal_size().columns - 5, "_"), 'green')
    cprint(
        f"Total Runtime for {counter} queries: {time() - universal_start}s", 'green', attrs=['bold'])
    end_time = localtime()
    cprint(
        f"End Time: {end_time.tm_hour}h:{end_time.tm_min}m:{end_time.tm_sec}s", 'green')


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Starting with a frontier that contains the initial state.
    start = Node(source, None, None)
    frontier = QueueFrontier()  # Breadth-First Search Algorithm
    frontier.add(start)

    # Initialize an empty explored state list
    explored = []

    # Keep looping until the solution is found.
    while True:

        # If frontier is empty, i.e. nothing is left in it, there is no path.
        if frontier.empty():
            return None

        # Get the next node and remove it from frontier.
        node = frontier.remove()

        # Mark as explored
        explored.append(node.state)

        # Add possible future states to frontier
        for action, state in neighbors_for_person(node.state):
            # If the state is not in the fontier or the explores state
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state, node, action)
                # If the child is the target
                if child.state == target:
                    solution = []

                    # The initial state will have no parent nodes.
                    while child.parent is not None:
                        solution.append([child.action, child.state])
                        child = child.parent

                    # Reverse these since we went up when tracing steps.
                    solution.reverse()
                    return solution

                # Add new child node.
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
