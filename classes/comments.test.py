# Tiffany

import unittest
from comments import *

class Comments(unittest.TestCase):
    def test1_empty_fulfilmentText(self):
        """Don't let users post empty comments"""
        self.assertRaises(ValueError, Comment(1, ""))

    def test2_upvote(self):
        """Score increases by 1 after upvote method"""
        testComment = Comment(1,"hello")
        testComment.upvote()
        testComment.upvote()
        testComment.upvote()
        self.assertEqual(testComment.score, 3)

    def test3_downvote(self):
        """Score decreases by 1 after downvote method"""

if __name__ == '__main__':
    unittest.main()
