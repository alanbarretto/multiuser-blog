import bloghandler
import models
import support

class PostEdit(bloghandler.BlogHandler):

    def get(self, post_id):

        k = support.db.Key.from_path("Post", int(post_id), parent=support.blog_key())
        p = support.db.get(k)

        if not p:
            self.redirect('/')

        if self.user and (self.user.name == p.creator):
            self.render("newpost.html", subject=p.subject,
                        content=p.content)
        elif not self.user:
            self.redirect('/')
        else:
            posts = greetings = models.Post.all().order('-created')
            comments = models.Comment.all().order('-created')
            error = "You can only edit posts you created."
            self.render('front.html', posts=posts,
                        comments=comments, error=error)

    def post(self, post_id):
        if not self.user:
            self.redirect('/')

        k = support.db.Key.from_path("Post", int(post_id), parent=support.blog_key())
        p = support.db.get(k)

        subject = self.request.get('subject')
        content = self.request.get('content')
        

        if not p:
            self.redirect('/')

        if subject and content:
            p.subject = subject
            p.content = content
            p.put()
            self.render('goodPostEdit.html')
        else: 
            error = "Please provide subject and/or content!"
            self.render("newpost.html", subject=subject,
                        content=content, error=error)