# Tiffany

from datetime import datetime

class Comment:
    def __init__(self, userID, commentText, score=0):
        self.userID = userID
        self.fulfilmentText = commentText
        self.score = score
        self.time = datetime.now()

    def upvote(self):
        """Upvote comment"""
        self.score += 1

    def downvote(self):
        """Downvote comment"""

    def remove(self):
        """Remove comment"""

    def make_anon(self):
        """Make comment anonymous"""

    def __repr__(self):
        return str(self.userID)+": "+str(self.fulfilmentText)
