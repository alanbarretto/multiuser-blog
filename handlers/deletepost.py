import bloghandler
import models
import support

class DeletePost(bloghandler.BlogHandler):
    def get(self, post_id):
        k = support.db.Key.from_path('Post', int(post_id), parent=support.blog_key())
        p = support.db.get(k)

        if not p:
            self.error(404)
            return
        if self.user and (self.user.name == p.creator):
            self.render("deletePost.html", subject= p.subject)

        elif self.user and (self.user.name != p.creator):
            error = "You can only delete posts you created!"
            posts = greetings = models.Post.all().order('-created')
            comments = models.Comment.all().order('-created')
            self.render("front.html", posts=posts, comments=comments, error=error)
        else:
            self.redirect('/login')

    def post(self, post_id):
        k = support.db.Key.from_path('Post', int(post_id), parent=support.blog_key())
        p = support.db.get(k)

        if self.user:   
            support.db.delete(k)
            self.render("goodPostDelete.html")