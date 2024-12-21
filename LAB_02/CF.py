import sys
from decimal import Decimal, ROUND_HALF_UP
from math import sqrt

ITEM_ITEM = 0
USER_USER = 1


def parse_input():
    N, M = next(sys.stdin).strip().split()
    rows = [list(next(sys.stdin).strip().split()) for _ in range(int(N))]
    Q = int(next(sys.stdin).strip())
    queries = [next(sys.stdin).strip().split() for _ in range(Q)]

    return N, M, rows, queries


def parse_query(query):
    I, J, T, K = query
    return int(I), int(J), int(T), int(K)


def pearson_coefficient(r1, r2):
    r_xs = sum(r1) / len(r1)
    r_ys = sum(r1) / len(r1)

    numerator = sum(
        [(r1[i] - r_xs) * (r2[i] - r_ys) for i in range(len(r1))])
    denominator = sqrt(sum(
        [(r1[i] - r_xs) ** 2 for i in range(len(r1))]) * sum(
        [(r2[i] - r_ys) ** 2 for i in range(len(r2))]
    ))

    return numerator / denominator


def rating_for_user_with_x(rows, user):
    return [row[user] for row in rows]


def normalized_user_rating(rows, user):
    ratings = rating_for_user_with_x(rows, user)
    scores = [int(r) for r in ratings if r != "X"]
    avg = sum(scores) / len(scores)

    return [(int(r) - avg) if r != "X" else 0 for r in ratings]


def normalized_item_rating(rows, item):
    ratings = rows[item]
    scores = [int(r) for r in ratings if r != "X"]
    avg = sum(scores) / len(scores)

    return [(int(r) - avg) if r != "X" else 0 for r in ratings]


def user_user_similarity(rows, user1, user2):
    r1 = normalized_user_rating(rows, user1)
    r2 = normalized_user_rating(rows, user2)

    return pearson_coefficient(r1, r2)


def item_item_similarity(rows, item1, item2):
    r1 = normalized_item_rating(rows, item1)
    r2 = normalized_item_rating(rows, item2)

    return pearson_coefficient(r1, r2)


def calculate_rating(rows, query):
    item, user, _type, cardinality = parse_query(query)

    user_index = user - 1
    item_index = item - 1

    if _type == ITEM_ITEM:
        similarities = []
        for i, _ in enumerate(rows):
            if i == item_index or rows[i][user_index] == "X":
                continue

            similarity = item_item_similarity(rows, i, item_index)
            if similarity > 0:
                similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        if len(similarities) >= cardinality:
            similarities = similarities[:cardinality]

        numerator = 0
        denominator = 0

        for similarity in similarities:
            other_rating = rows[similarity[0]][user_index]

            numerator += similarity[1] * int(other_rating)
            denominator += similarity[1]

        output = Decimal(Decimal(numerator / denominator).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))

        return output
    else:
        similarities = []
        for i, _ in enumerate(rows[0]):
            if i == user_index or rows[item_index][i] == "X":
                continue

            similarity = user_user_similarity(rows, user_index, i)
            if similarity > 0:
                similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        if len(similarities) >= cardinality:
            similarities = similarities[:cardinality]

        numerator = 0
        denominator = 0

        for similarity in similarities:
            other_rating = rows[item_index][similarity[0]]

            numerator += similarity[1] * int(other_rating)
            denominator += similarity[1]

        output = Decimal(Decimal(numerator / denominator).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))

        return output


if __name__ == "__main__":
    N, M, rows, queries = parse_input()
    for query in queries:
        rating = calculate_rating(rows, query)
        print(rating)
