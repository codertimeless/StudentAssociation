import unittest
from StudentAssociation.StudentAssociation.views import my_view


class TestMethods(unittest.TestCase):
    def test_add(self):
        results = my_view(1, 2)
        self.assertEqual(results, 3)


if __name__ == '__main__':
    unittest.main()
