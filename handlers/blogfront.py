from handler import bloghandler
from models import User, Post, Comment

class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        comments = Comment.all().order('-created')
        
        self.render("front.html", posts = posts, comments=comments)
        