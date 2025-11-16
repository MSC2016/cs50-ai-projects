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
        with open(os.path.join(directory, filename)) as f:
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

    # initialize the return with all values set to 0
    probabilities = {web_page: 0 for web_page in corpus}
    
    # store all the links in the current page
    current_page_links = corpus[page]

    # calculate the amount of probability to distribute to each page, when selection is random
    random_page_prob = (1-damping_factor) / len(corpus)

    # if all pages have links to other pages
    if len(current_page_links) > 0:
        # calculate the amount of probability to distribute to each link in the current page
        current_page_link_prob = damping_factor / len(current_page_links)
        # iterate trough all keys, adding 1-d to all, and distribuiting d to the links in the current page
        for p in probabilities:
            probabilities[p] += random_page_prob
            if p in current_page_links:
                probabilities[p] += current_page_link_prob
        return probabilities
    # if the current page has no links to other page, set all values to 1/number of pages
    else:
        for p in probabilities:
            probabilities[p] = 1/len(probabilities)
        return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # initialize the dictionary that holds the visit count
    pagerank = {web_page: 0 for web_page in corpus}

    # chose the first page to visit
    current_page = random.choice(list(pagerank.keys()))

    for _ in range(0, n):
        # get the transition model for the current choice
        tm = transition_model(corpus, current_page, damping_factor)
        # get a list of all available pages
        pages = list(tm.keys())
        # get a list of probabilities for each page
        probabilities = list(tm.values())
        # get a random choice acording to the probability distribuition
        current_page = random.choices(pages, probabilities)[0]
        # increment the nnumber of times the chosen page was visited
        pagerank[current_page] += 1

    # normalize the values dividing (visit_count /n)
    for page in pagerank:
        pagerank[page] = pagerank[page] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize the dictionary that holds the visit count and the
    # one that holds the new values after each iteration, and check
    # what the max variation was for each iteration

    pagerank = {web_page: 1/len(corpus) for web_page in corpus}
    new_pagerank = pagerank.copy()
    
    # get a dictionary of {pages : links to current page}
    links_to_current_page = {web_page: set() for web_page in corpus}
    for page in corpus:
        for link in corpus[page]:
            if link in links_to_current_page:
                links_to_current_page[link].add(page)

    # current_variation set to 1, to ensure the while loop starts
    max_variation = 0.001
    current_variation = 1
    while current_variation >= max_variation:

        # calculate probability assignd to pages without external links
        no_e_link_probability = sum(pagerank[page] for page in corpus if len(corpus[page]) == 0) / len(corpus)

        # iterate trough every page in the corpus
        for page in corpus:
            weighted_sum = 0 
            # sum all the pages that link to current page, ensuring the probability is always
            # distributed, even if the page has no links.
            for linking_page in links_to_current_page[page]:
                if len(corpus[linking_page]) == 0:
                    weighted_sum += pagerank[linking_page] / len(corpus)
                else:
                    weighted_sum += pagerank[linking_page] / len(corpus[linking_page])
            # assign the new rank to each page, random probability + weighted sum * damping_factor
            new_pagerank[page] = (1-damping_factor) / len(corpus) + (weighted_sum + no_e_link_probability) * damping_factor 
        # get the value that had the biggest change and assign it to current_variation
        current_variation = max(abs(pagerank[page] - new_pagerank[page]) for page in pagerank)
        # assign the new values to page_rank
        pagerank = new_pagerank.copy()

    return pagerank


if __name__ == "__main__":
    main()
