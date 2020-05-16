import os
import random
import re
import sys
import copy
import collections
import numpy as np

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

    for page in corpus:
        if len(corpus[page])==0:
            corpus[page] = {p for p in corpus.keys()}
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
    all_pages = list(corpus.keys())

    # select a random number and check if it is long to [0,damping_factor) or [damping_factor,1)
    random_number = random.random()
    if (random_number < damping_factor) & (len(corpus[page]) > 0):
        next_page = random.choice(list(corpus[page]))
    else:
        next_page = random.choice(all_pages)
    return next_page



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    TRIALS = 100
    all_pages = list(corpus.keys())
    page_dict = {}
    for j in corpus.keys():
        page_dict[j]=0

    # loop over TRIALS with random starting page
    for i in range(TRIALS):
        # start a random page
        next_page = random.choice(all_pages)

        # for each sample we move over n steps
        for j in range(n):
            next_page = transition_model(corpus, next_page, damping_factor)
            page_dict[next_page] += 1

    for j in corpus.keys():
        page_dict[j] *= 1/(TRIALS*n)
    
    return page_dict

    
def root_mean_square_error(y1, y2):   
    return np.sqrt(np.average((np.array(y1) - np.array(y2)) ** 2))

def plink2p(corpus, page):
    return [p for p in corpus.keys() if (page in corpus[p])]


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    N = len(all_pages)
    epsilon = 10**(-10)
    diff = 10**6

    # initialize the output_dict
    page_dict = collections.OrderedDict()
    for j in corpus.keys():
        page_dict[j] = 1/N
    
    # loop until it converges
    while (diff > epsilon):
        start_dict = copy.deepcopy(page_dict)
        for j in corpus.keys():
            page_dict[j] = (1 - damping_factor)/N
            for i in plink2p(corpus, j):
                page_dict[j] += start_dict[i]*damping_factor/len(corpus[i])

        diff = root_mean_square_error(list(start_dict.values()), list(page_dict.values()))

    return page_dict
        

            

        


    




if __name__ == "__main__":
    main()
