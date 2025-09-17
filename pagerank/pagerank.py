import os
from numpy import random
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
    current_page_links = corpus[page]
    if len(current_page_links) == 0:
        return dict.fromkeys(corpus.keys(), 1/ len(corpus))

    random_probability = (1 - damping_factor ) / len(corpus)
    transition = dict()
    for c in corpus: 
        if c in current_page_links:
            transition[c] = random_probability + (damping_factor / len(current_page_links))
        else: 
            transition[c] = random_probability 
    return transition           

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """  
    pages = list(corpus.keys())
    page_ranks = dict.fromkeys(pages, 0)
    current_page = random.choice(pages) 
    for _ in range(n):
        sample = transition_model(corpus, current_page, damping_factor)         
        page_ranks[current_page] += 1
        current_page = random.choice(pages, p=[ sample[p] for p in pages])  

    for c in corpus:
        page_ranks[c] = page_ranks[c] /n
    
    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    no_of_pages = len(corpus)
    initial_pr = 1 / no_of_pages
    random_probability = (1 - damping_factor ) / no_of_pages
    page_ranks = dict()
    for c in corpus:
        page_ranks[c] = initial_pr

    def caculate_page_rank(page): 
        sum_of_rank = 0
        for c in corpus:     
            if len(corpus[c]) == 0:
                sum_of_rank +=  page_ranks[c] /no_of_pages           
            elif page in corpus[c]:
                sum_of_rank += page_ranks[c]/ (len(corpus[c]))
        return random_probability + (damping_factor * sum_of_rank)         

    is_good_enough = False
    while is_good_enough == False:
        new_page_ranks = dict()
        for pr in page_ranks.items():   
                new_page_rank = caculate_page_rank(pr[0])   
                new_page_ranks[pr[0]] = new_page_rank 
        is_good_enough = all(abs(new_page_ranks[page] - page_ranks[page]) < 0.001 for page in corpus)   
        page_ranks = new_page_ranks                   
    return page_ranks 

if __name__ == "__main__":
    main()
