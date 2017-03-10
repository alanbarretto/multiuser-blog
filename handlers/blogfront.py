from bloghandler import BlogHandler
from models import Post, Comment

#from file_name import ClassName

class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        comments = Comment.all().order('-created')
        
        self.render("front.html", posts = posts, comments=comments)
        