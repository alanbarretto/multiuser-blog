from bloghandler import BlogHandler
from models import Post, Comment, User
from support import blog_key

from google.appengine.ext import db

class PostEdit(BlogHandler):

    def get(self, post_id):

        #k = db.Key.from_path("Post", int(post_id), parent=blog_key())
        p = Post.get_by_id(int(post_id))

        if not p:
            self.redirect('/')
            return

        if self.user and (self.user.key() == p.user_obj.key()):
            self.render("newpost.html", subject=p.subject,
                        content=p.content)
        elif not self.user:
            self.redirect('/')
        else:
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            error = "You can only edit posts you created."
            self.render('front.html', posts=posts,
                        comments=comments, error=error)

    def post(self, post_id):
        if not self.user:
            self.redirect('/')
            return

        #k = db.Key.from_path("Post", int(post_id), parent=blog_key())
        p = Post.get_by_id(int(post_id))

        subject = self.request.get('subject')
        content = self.request.get('content')
        

        if not p:
            self.redirect('/')
            return

        if self.user and (self.user.key() == p.user_obj.key()):
            if subject and content:
                p.subject = subject
                p.content = content
                p.put()
                self.render('goodPostEdit.html')
            else: 
                error = "Please provide subject and/or content!"
                self.render("newpost.html", subject=subject,
                        content=content, error=error)
        else:
            self.redirect('/blog')