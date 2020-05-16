import csv
import itertools
import sys
import os

os.chdir('CS50_Python/Projects/heredity/')

# PROBS = {

#     # Unconditional probabilities for having gene
#     "gene": {
#         2: 0.01,
#         1: 0.03,
#         0: 0.96
#     },

#     "trait": {

#         # Probability of trait given two copies of gene
#         2: {
#             True: 0.65,
#             False: 0.35
#         },

#         # Probability of trait given one copy of gene
#         1: {
#             True: 0.56,
#             False: 0.44
#         },

#         # Probability of trait given no gene
#         0: {
#             True: 0.01,
#             False: 0.99
#         }
#     },

#     # Mutation probability
#     "mutation": 0.01
# }


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    nodes = {
        person: {
            "node": Node(DiscreteDistribution({
            "none": 0.7,
            "light": 0.2,
            "heavy": 0.1
            }), name=person_name)
        }
        for person in people
    }

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def parent_prob(people, person, papamama, one_gene, two_genes, got_gene=True):
    if (person not in one_gene) & (person not in two_genes):
        if people[person][papamama] in one_gene:
            pm = 0.5
        elif people[person][papamama] in two_genes: 
            pm = PROBS['mutation']
        else:   
            pm = 1 - PROBS['mutation']
    if person in two_genes:
        if people[person][papamama] in one_gene:
            pm = 0.5
        elif people[person][papamama] in two_genes: 
            pm = 1 - PROBS['mutation'] 
        else:   
            pm = PROBS['mutation']  
    if person in one_gene:
        if got_gene == True:
            if people[person][papamama] in one_gene:
                pm = 0.5
            elif people[person][papamama] in two_genes: 
                pm = 1 - PROBS['mutation'] 
            else:   
                pm = PROBS['mutation']  
        else:
            if people[person][papamama] in one_gene:
                pm = 0.5
            elif people[person][papamama] in two_genes: 
                pm = PROBS['mutation'] 
            else:   
                pm = 1- PROBS['mutation'] 
    return pm


def check_valid_parents(people, person):
    if (people[person]['mother'] != None) and (people[person]['father'] != None):
        return True
    else:
        return False 


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = {}
    result = 1

    # loop over each person in the list of people
    for person in people.keys():
        if person in one_gene:
            if check_valid_parents(people, person): # with parents
                # child get the gene from the father
                pp1 = parent_prob(people, person, 'father', one_gene, two_genes, got_gene=True)
                mm1 = parent_prob(people, person, 'mother', one_gene, two_genes, got_gene=False)
                # child get the gene from the mother
                pp2 = parent_prob(people, person, 'father', one_gene, two_genes, got_gene=False)
                mm2 = parent_prob(people, person, 'mother', one_gene, two_genes, got_gene=True)                
                prob[person] = PROBS["trait"][1][person in have_trait] * (pp1 * mm1 + pp2 * mm2)
            else: # no known parents
                prob[person] = PROBS["gene"][1] * PROBS["trait"][1][person in have_trait]  
        elif person in two_genes:
            if check_valid_parents(people, person): # with parents
                pp = parent_prob(people, person, 'father', one_gene, two_genes)
                mm = parent_prob(people, person, 'mother', one_gene, two_genes)
                prob[person] = pp * mm * PROBS["trait"][2][person in have_trait]
            else: # no known parents
                prob[person] = PROBS["gene"][2] * PROBS["trait"][2][person in have_trait]            

        else:
            # the person with no-gene
            if check_valid_parents(people, person): # with parents
                pp = parent_prob(people, person, 'father', one_gene, two_genes)
                mm = parent_prob(people, person, 'mother', one_gene, two_genes)
                prob[person] = pp * mm * PROBS["trait"][0][person in have_trait]
            else: # no known parents
                prob[person] = PROBS["gene"][0] * PROBS["trait"][0][person in have_trait]
        result *= prob[person]

    return result



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        # update the probabilities based on the number of gene for each person
        if person in one_gene:
            probabilities[person]["gene"][1] += p
            probabilities[person]["trait"][person in have_trait] += p 
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
            probabilities[person]["trait"][person in have_trait] += p 
        else:        
            probabilities[person]["gene"][0] += p
            probabilities[person]["trait"][person in have_trait] += p 


    


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        # dict of gene of each person 
        gene_dict = probabilities[person]["gene"]
        probabilities[person]["gene"] = {val: gene_dict[val]/sum(gene_dict.values()) for val in gene_dict.keys()}
        # dict of trait of each person 
        trait_dict = probabilities[person]["trait"]
        probabilities[person]["trait"] = {val: trait_dict[val]/sum(trait_dict.values()) for val in trait_dict.keys()}

if __name__ == "__main__":
    main()