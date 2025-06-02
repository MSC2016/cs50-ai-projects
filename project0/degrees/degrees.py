import csv
import sys

from util import Node, StackFrontier, QueueFrontier

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


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")


    ################################################################
    #                                                              #
    #        DONT FORGET TO RESTORE MAIN() BEFORE SUBMITTING       #
    #                                                              #
    ################################################################


    #source = person_id_for_name(input("Name: "))
    source = "Cary Elwes"
    source = "tom cruise"
    #source = "emma watson"
    print(f"\n\nsource is {source}")
    

    if source is None:
        sys.exit("Person not found.")


    #target = person_id_for_name(input("Name: "))
    target = "Demi Moore"
    print(f"target is {target}\n\n")

    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Initialize start node to source and frontier
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # variable that stores all possible paths
    paths = {}

    # variable that stores nodes we already checked
    already_checked_ids = set()

    while True:
        # break if there are no more options to explore
        if frontier.empty():
            break

        # pull one node from the frontier 
        node = frontier.remove()
        
        # get the person_id from the selected node
        person_id = person_id_for_name(node.state.lower())

        # add that node to the already checked list
        already_checked_ids.add(person_id)

        # get the movies the person participated in, 
        movies_stared_by_person = people[person_id]['movies']

        # abort this iteration if the person hasnt participated in any movies
        if len(movies_stared_by_person) == 0:
            print("if you didnt chose emma watson and you are seeing this, you messed up")
            continue

        # get everybody else that participated in that/those movie(s)
        # and add enlarge the frontier
        for movie in movies_stared_by_person:
            stars_ids = movies[movie]['stars']

            ## probably mesing up ---
            ## check print's - this is where i want to create nodes
            
            for star_id in stars_ids:
                yet_another_star_id_check = sel()
                if star_id not in already_checked_ids:
                    star_name = people[star_id]["name"]
                    new_node = Node(state=star_name, parent=node, action=None)
                    frontier.add(new_node)
                    print(f"checking {star_name}")





    raise Exception("OOOps, something went wrong... you were not suposed to see this...")


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
