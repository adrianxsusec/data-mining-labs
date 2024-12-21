from util import load_data_and_generate_simhash, hamming_distance_within


def determine_similarity(simhashes, queries):
    for query in queries:
        i = int(query[0])
        k = int(query[1])

        num_of_similar = 0

        current_simhash = simhashes[i]
        for index, simhash in enumerate(simhashes):
            if i != index and hamming_distance_within(current_simhash, simhash, k):
                num_of_similar += 1

        print(num_of_similar)


if __name__ == "__main__":
    simhashes, queries = load_data_and_generate_simhash()
    determine_similarity(simhashes, queries)
    print()
