from bloghandler import BlogHandler
from models import Post, Comment
from support import blog_key

from google.appengine.ext import db

class DeleteComments(BlogHandler):

    def get(self, post_id):

        k = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        c = db.get(k)
        
        if not c:
            self.error(404)
            return

        if self.user and (self.user.key() == c.comment_user):
            self.render("deletepage.html", comment=c.content)

        elif self.user and (self.user.key() != c.comment_user):
            error = "You can only delete comments you created"
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            self.render('front.html', posts=posts,
                        comments=comments, error=error)
        
        else: 
            self.redirect('/login')


    def post(self, post_id):
        k = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        c = db.get(k)

        if self.user and (self.user.key() == c.comment_user):
            db.delete(k)
            self.render("deletedComment.html")
            return