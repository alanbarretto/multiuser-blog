from bloghandler import BlogHandler
from models import Post, Comment
from support import blog_key

from google.appengine.ext import db

class DeletePost(BlogHandler):
    def get(self, post_id):
        
        p = Post.get_by_id(int(post_id))

        if not p:
            self.error(404)
            return
        if self.user and (self.user.key() == p.user_obj):
            self.render("deletePost.html", subject= p.subject)

        elif self.user and (self.user.key() != p.user_obj):
            error = "You can only delete posts you created!"
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            self.render("front.html", posts=posts, comments=comments, error=error)
        else:
            self.redirect('/login')

    def post(self, post_id):
        #k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        
        p = Post.get_by_id(int(post_id))

        if self.user and (self.user.key() == p.user_obj):   
            db.delete(p)
            self.render("goodPostDelete.html")
            return