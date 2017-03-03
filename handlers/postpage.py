import BlogHandler
from models import Comment

class PostPage(BlogHandler):
    def get(self, post_id):
        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)
        
        subject = p.subject
        comments = Comment.all().order('-post_reference')
        
        if not p:
            self.error(404)
            return

        self.render("permalink.html", post = p, comments=comments)