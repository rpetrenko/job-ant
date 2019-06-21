def sum_interval(a1, a2, b1, b2):
    # if not intersection return None
    if a2 < b1 or a1 > b2:
        return None
    # assuming they intersect
    return min(a1, b1), max(a2, b2)


def mul_interval(a1, a2, b1, b2):
    if a2 < b1 or a1 > b2:
        return None
    return max(a1, b1), min(a2, b2)


def area(rec):
    x1, y1, x2, y2 = rec
    return (x2 - x1) * (y2 - y1)


def rectangle_left_of(rec_a, rec_b):
    _, _, a, _ = rec_a
    b, _, _, _ = rec_b
    return a < b


def merge_rectangles(rectangles, similarity=0.9):
    """
    Given a list of rectangles merge those which share enough pixels
    :param rectangles: list of [up_left_x, up_left_y, down_right_x, down_right_y]
    :param similarity:
    :return: new list of rectangles
    """
    if len(rectangles) < 2:
        return rectangles

    def sum_rectangle(rec1, rec2):
        x_int = sum_interval(rec1[0], rec1[2], rec2[0], rec2[2])
        if not x_int:
            return None
        y_int = sum_interval(rec1[1], rec1[3], rec2[1], rec2[3])
        if not y_int:
            return None
        return x_int[0], y_int[0], x_int[1], y_int[1]

    def mul_rectangle(rec1, rec2):
        x_int = mul_interval(rec1[0], rec1[2], rec2[0], rec2[2])
        if not x_int:
            return None
        y_int = mul_interval(rec1[1], rec1[3], rec2[1], rec2[3])
        if not y_int:
            return None
        return x_int[0], y_int[0], x_int[1], y_int[1]

    def rec_similar(rec_list, rec2):
        for rec1 in rec_list:
            mr = mul_rectangle(rec1, rec2)
            if mr:
                sr = sum_rectangle(rec1, rec2)
                sim_score = area(mr) / area(sr)
                if sim_score >= similarity:
                    return True
        return False

    res = [rectangles[0]]
    for rec in rectangles[1:]:
        if not rec_similar(res, rec):
            res.append(rec)
    return res


if __name__ == "__main__":
    rectangles = [
        [1, 100, 10, 110],
        [2, 101, 9, 111],
        [20, 200, 30, 210]
    ]
    res = merge_rectangles(rectangles, similarity=0.6)
    print(res)