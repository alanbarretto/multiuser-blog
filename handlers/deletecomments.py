import bloghandler
import models
import support

class DeleteComments(bloghandler.BlogHandler):

    def get(self, post_id):

        ck = support.db.Key.from_path('Comment', int(post_id), parent=support.blog_key())
        comment = support.db.get(ck)
        
        if not comment:
            self.error(404)
            return

        if self.user and (self.user.name == comment.creator):
            self.render("deletepage.html", comment=comment.content)

        elif self.user and (self.user.name != comment.creator):
            error = "You can only delete comments you created"
            posts = greetings = models.Post.all().order('-created')
            comments = models.Comment.all().order('-created')
            self.render('front.html', posts=posts,
                        comments=comments, error=error)
        
        else: 
            self.redirect('/login')


    def post(self, post_id):
        ck = support.db.Key.from_path('Comment', int(post_id), parent=support.blog_key())
        comment = support.db.get(ck)

        if self.user:
            support.db.delete(ck)
            self.render("deletedComment.html")