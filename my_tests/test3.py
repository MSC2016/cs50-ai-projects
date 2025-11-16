people = {
    "1": {"name": "Kevin Bacon", "birth": "1958"},
    "2": {"name": "Tom Hanks", "birth": "1956"},
    "3": {"name": "Bill Paxton", "birth": "1955"},
    "4": {"name": "Gary Sinise", "birth": "1955"},
    "5": {"name": "Johnny Depp", "birth": "1963"},
    "6": {"name": "Helena Bonham Carter", "birth": "1966"},
    "7": {"name": "Winona Ryder", "birth": "1971"}
}

movies = {
    "101": {"title": "Apollo 13", "year": "1995", "stars": {"1", "2", "3", "4"}},
    "102": {"title": "Footloose", "year": "1984", "stars": {"1", "7"}},
    "103": {"title": "Sweeney Todd", "year": "2007", "stars": {"5", "6"}},
    "104": {"title": "my movie 1", "year": "2007", "stars": {"3", "6"}},
    "105": {"title": "my movie 12", "year": "2007", "stars": {"5", "3"}},
    "106": {"title": "my movie 123", "year": "2007", "stars": {"5", "6"}}
}


def most_collaborative_actor():
    """
    Return the person_id of the actor who has the most unique co-stars.
    """
    # Your code here
    colab_count={}
    for movie in movies:
        for star in movies[movie]["stars"]:
            if star not in colab_count:
                colab_count.update({star:1})
            else:
                colab_count[star] += 1


    print(f"The most colaborative actor was: {people[max(colab_count, key = colab_count.get)]['name']}")
    print(f"The one with the least was: {people[min(colab_count, key = colab_count.get)]['name']}")

most_collaborative_actor()