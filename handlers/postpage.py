import bloghandler
import models
import support

class PostPage(bloghandler.BlogHandler):
    def get(self, post_id):
        k = support.db.Key.from_path('Post', int(post_id), parent=support.blog_key())
        p = support.db.get(k)
        
        subject = p.subject
        comments = models.Comment.all().order('-post_reference')
        
        if not p:
            self.error(404)
            return

        self.render("permalink.html", post = p, comments=comments)