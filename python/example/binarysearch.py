#!/usr/bin/env python

def find_index(ordered_array, to_find):
    """
    Return index of ``to_find`` via binary search.
    Returns None if not in ``ordered_array``

    ordered_array -- array of ordered values
    to
    """
    if not ordered_array:
        return
    minimum = 0
    maximum = len(ordered_array)-1
    while True:
        middle = (minimum + maximum)/2
        value = ordered_array[middle]
        if value == to_find:
            return middle
        if maximum == minimum:
            return
        if value < to_find:
            minimum = middle+1
            continue
        if value > to_find:
            maximum = middle
            continue

if __name__ == '__main__':
    import unittest

    class TestFindIndex(unittest.TestCase):
        values = [1,2,4,8,16,17]
        def test_spotcheck(self):
            for index, value in enumerate(self.values):
                self.assertEqual(find_index(self.values, value), index)

    unittest.main()
