import unittest
from management.views import test_view


class TestMethods(unittest.TestCase):
    def test_add(self):
        results = test_view(1, 2)
        self.assertEqual(results, 3)


if __name__ == '__main__':
    unittest.main()
