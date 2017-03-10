from bloghandler import BlogHandler
from models import Post, User

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")
            

    def post(self):
        if not self.user:
            self.redirect('/login')
            return

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_name = self.user.name
        
        # post = Post(user=self.user, subject = subject, content = content)
        # post.put()

        if subject and content:
            p = Post(user=user_name, subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
            
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)