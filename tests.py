import unittest
from StudentAssociation.views import main_view


class TestMethods(unittest.TestCase):
    def test_add(self):
        results = main_view(1, 2)
        self.assertEqual(results, 3)


if __name__ == '__main__':
    unittest.main()
