import sys
from itertools import combinations
from math import floor


def parse_input():
    no_baskets = int(next(sys.stdin))
    s = float(next(sys.stdin))

    threshold = floor(no_baskets * s)

    no_compartments = int(next(sys.stdin))

    baskets = [list(map(int, next(sys.stdin).strip().split())) for _ in range(no_baskets)]

    return no_baskets, threshold, no_compartments, baskets


def main():
    no_baskets, threshold, no_compartments, baskets = parse_input()

    no_items = {}

    for basket in baskets:
        for item in basket:
            no_items[item] = no_items.get(item, 0) + 1

    compartments = [0] * no_compartments

    items_size = len(no_items)

    pairs = {}

    for basket in baskets:
        for i, j in combinations(basket, 2):
            if no_items[i] >= threshold and no_items[j] >= threshold:
                compartment = ((i * items_size) + j) % no_compartments
                compartments[compartment] += 1
                pairs[(i, j)] = 0

    for basket in baskets:
        for i, j in combinations(basket, 2):
            if no_items[i] >= threshold and no_items[j] >= threshold:
                compartment = ((i * items_size) + j) % no_compartments
                if compartments[compartment] >= threshold:
                    pairs[(i, j)] = pairs.get((i, j), 0) + 1

    m = len([item for item in no_items if no_items[item] >= threshold])
    A = m * (m - 1) // 2

    P = len([pair for pair in pairs if pairs[pair] >= threshold])

    x_s = sorted([pairs[pair] for pair in pairs if pairs[pair] >= threshold], reverse=True)

    print(A)
    print(P)

    [print(x) for x in x_s]

    print()


if __name__ == "__main__":
    main()
