import bloghandler
import models
import support

class PostComments(bloghandler.BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog')
        k = support.db.Key.from_path('Post', int(post_id), parent=support.blog_key())
        p = support.db.get(k)

        if self.user:
            self.render("usercomment.html")
        else:
            self.redirect('/')

    def post(self, post_id):
        if not self.user:
            self.redirect('/login')

        k = support.db.Key.from_path('Post', int(post_id), parent=support.blog_key())
        p = support.db.get(k)
        content = self.request.get('content')
        user = self.user.name

        if content:
            c = models.Comment(parent=support.blog_key(), post_reference=p.subject, content=content, creator=user)
            c.put()
            self.render("successfulcomment.html")
        else:
            error = "subject and content, please!"
            self.render("usercomment.html", error=error)