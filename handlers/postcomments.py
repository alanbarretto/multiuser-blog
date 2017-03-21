from bloghandler import BlogHandler
from models import Comment
from support import blog_key
from models import Post, Comment

from google.appengine.ext import db

class PostComments(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog')
        #k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = Post.get_by_id(int(post_id))

        if self.user:
            self.render("usercomment.html")
            
        else:
            self.redirect('/')
            

    def post(self, post_id):
        if not self.user:
            self.redirect('/login')
            return

        #k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = Post.get_by_id(int(post_id))
        content = self.request.get('content')
        user = self.user.name

        if not p:
            self.redirect('/')
        else: 
            if content:
                c = Comment(parent=blog_key(), post_reference=p.subject, content=content, creator=user)
                c.put()
                self.render("successfulcomment.html")
            
            else:
                error = "subject and content, please!"
                self.render("usercomment.html", error=error)
            