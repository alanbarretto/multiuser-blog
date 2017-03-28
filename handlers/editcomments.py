from bloghandler import BlogHandler
from models import Post, Comment
from support import blog_key
from google.appengine.ext import db


class EditComments(BlogHandler):
    def get(self, post_id):
        k = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        c =  db.get(k) 
        
        if not c:
            self.error(404)
            return

        if self.user and (self.user.key() == c.comment_user.key()):
            self.render("usercomment.html", content=c.content)
        
        elif self.user and (self.user.key() != c.comment_user.key()):
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            error = "You can only edit comments you created."
            self.render('front.html', posts=posts,
                        comments=comments, error=error)
        else: 
            self.redirect('/login')

    def post(self, post_id):

        if not self.user:
            self.redirect('/')
        
        k = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        c = db.get(k)  

        if not c:
            self.error(404)
            return
        
        if self.user and (self.user.key() == c.comment_user.key()):
            content = self.request.get('content')
            user = self.user.name

            if content: 
                c.content = content
                c.put()
                self.render("goodCommentEdit.html")
            else:
                error = "content, please!"
                self.render("usercomment.html", content=c.content, error=error)
        else:
            self.redirect('/blog')