from typing import List


def is_magic(square: List[List[int]]) -> bool:
    """determine whether a square is magic or not

    :param square: square to test
    :return: True if magic
    """
    # if this is not a square, false
    if len(square) != len(square[0]):
        return False

    # magic square of size 1 is trivial
    if len(square) == 1:
        return True

    try:
        # sum(cols) == sum(rows) in magic squares
        if rows_sum(square) != rows_sum(square, rotate=True):
            return False
    except ValueError:
        # raised if two consecutive rows doesn't have the same sum
        return False

    # check if the left diagonal is equal to the right one
    diag_sum = 0
    for i in range(len(square)):
        diag_sum += square[i][i]
        diag_sum -= square[i][len(square) - 1 - i]

    # if the sum of each diagonals is the same, r_diag - l_diag == 0
    return diag_sum == 0


def rows_sum(square: List[List[int]], rotate: bool = False) -> int:
    """evaluate the sum of all rows in a double array

    :param square: the double array
    :param rotate: if true, swaps columns and rows
    :return: the sum of all rows
    """
    if rotate:
        square = list(zip(*reversed(square)))

    total = 0
    prev = sum(square[0])

    for i in range(len(square)):
        tmp = sum(square[i])

        if prev != tmp:
            raise ValueError('Not magic')

        prev = tmp
        total += tmp

    return total


if __name__ == '__main__':
    # expected: True
    print(is_magic([
        [2, 7, 6],
        [9, 5, 1],
        [4, 3, 8]
    ]))
