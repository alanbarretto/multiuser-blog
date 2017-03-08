import bloghandler
import models

class BlogFront(bloghandler.BlogHandler):
    def get(self):
        posts = greetings = models.Post.all().order('-created')
        comments = models.Comment.all().order('-created')
        
        self.render("front.html", posts = posts, comments=comments)
        