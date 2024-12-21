import time
from collections import defaultdict

from util import load_data_and_generate_simhash, hamming_distance_within


def generate_candidates(simhashes: list, band_count: int):
    candidates = defaultdict(set)
    for band in range(band_count):
        buckets = dict()
        for i, simhash in enumerate(simhashes):
            reversed_simhash = bin(int(simhash, 16))[2:].zfill(128)[::-1]
            start = band * 16
            end = start + 16
            bucket = int(reversed_simhash[start:end], 2)
            texts_in_bucket = set()

            if bucket in buckets:
                texts_in_bucket = buckets.get(bucket)
                for text_id in texts_in_bucket:
                    candidates[i].add(text_id)
                    candidates[text_id].add(i)

            texts_in_bucket.add(i)
            buckets[bucket] = texts_in_bucket

    return candidates

def determine_similarity(simhashes, queries):
    for query in queries:
        i = int(query[0])
        k = int(query[1])

        num_of_similar = 0
        for candidate in candidates[i]:
            if i != candidate and hamming_distance_within(simhashes[i], simhashes[candidate], k):
                num_of_similar += 1

        print(num_of_similar)

if __name__ == "__main__":
    band_count = 8
    simhashes, queries = load_data_and_generate_simhash()
    candidates = generate_candidates(simhashes, band_count)

    determine_similarity(simhashes, queries)

    print()