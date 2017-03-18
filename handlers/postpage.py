from bloghandler import BlogHandler
from models import Post, Comment
from support import blog_key

from google.appengine.ext import db

class PostPage(BlogHandler):
    def get(self, post_id):
    	
        #k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = Post.get_by_id(int(post_id))
        
        if not p:
            self.error(404)
            return

        comments = Comment.all().order('-post_reference')
        

        self.render("permalink.html", post = p, comments=comments)