# Sample data structure
people = {
    "1": {"name": "Kevin Bacon", "birth": "1958", "movies": {"10", "20"}},
    "2": {"name": "Tom Hanks", "birth": "1956", "movies": {"10"}},
    "3": {"name": "Meryl Streep", "birth": "1949", "movies": {"30"}},
    "4": {"name": "Gary Sinise", "birth": "1955", "movies": {"10", "30"}},
}

movies = {
    "10": {"title": "Apollo 13", "year": "1995", "stars": {"1", "2", "4"}},
    "20": {"title": "Footloose", "year": "1984", "stars": {"1"}},
    "30": {"title": "The Post", "year": "2017", "stars": {"3", "4"}},
}

def my_version_get_costars(person_id):
    #works but not ideal
    """
    Return a set of all person_ids who have acted in a movie with the given person_id.
    """
    # Your code here
    mv = []
    for movie in movies:
        if person_id in movies[movie]["stars"]:
            mv.append(movie)
    
    cs = []
    for id in mv:
        for star in movies[id]["stars"]:
            if star != index:
                cs.append(star)
    return cs

def get_costars(person_id):
    # AI suggested after i posted my solution
    """
    Return a set of all person_ids who have acted in a movie with the given person_id.
    """
    costars = set()

    for movie_id in people[person_id]["movies"]:
        for star_id in movies[movie_id]["stars"]:
            if star_id != person_id:
                costars.add(star_id)
                
    return costars


# Try it out
index = "4"
costars = get_costars(index)
print(f"Co-stars of {people[index]['name']}:", {people[p]['name'] for p in costars})
