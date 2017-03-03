import BlogHandler
from models import User, Post

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")
            return

    def post(self):
        if not self.user:
            self.redirect('/login')
            return

        subject = self.request.get('subject')
        content = self.request.get('content')
        user = User.name

        if subject and content:
            p = Post(user=user, subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)