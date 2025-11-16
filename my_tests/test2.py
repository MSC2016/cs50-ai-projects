# Sample data simulating what you'd get from CS50 Degrees project

people = {
    "102": {
        "name": "Kevin Bacon",
        "birth": "1958",
        "movies": {"112384", "104257"}
    },
    "200": {
        "name": "Tom Hanks",
        "birth": "1956",
        "movies": {"112384", "129456"}
    },
    "300": {
        "name": "Meg Ryan",
        "birth": "1961",
        "movies": {"129456"}
    }
}

movies = {
    "112384": {
        "title": "Apollo 13",
        "year": "1995",
        "stars": {"102", "200"}
    },
    "104257": {
        "title": "Footloose",
        "year": "1984",
        "stars": {"102"}
    },
    "129456": {
        "title": "Sleepless in Seattle",
        "year": "1993",
        "stars": {"200", "300"}
    }
}


def get_common_movies(person1, person2):
    """
    Return a set of movie_ids that both person1 and person2 starred in.
    """
    # Your code here
    return people[person1]["movies"] & people[person2]["movies"]


# Try it out
person1 = "102"  # Kevin Bacon
person2 = "200"  # Tom Hanks
common = get_common_movies(person1, person2)

print(f"Common movies of {people[person1]['name']} and {people[person2]['name']}:")
if common:
    for movie_id in common:
        title = movies[movie_id]["title"]
        print(f"- {title}")
else:
    print("None")
