from bloghandler import BlogHandler
from models import Post, Comment
from support import Support
#blog_key

class EditComments(BlogHandler):
    def get(self, post_id):
        ck = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        comment =  db.get(ck)
        
        if not comment:
            self.error(404)
            return

        if self.user and (self.user.name == comment.creator):
            self.render("usercomment.html", content=comment.content)
        
        elif self.user and (self.user.name != comment.creator):
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            error = "You can only edit comments you created."
            self.render('front.html', posts=posts,
                        comments=comments, error=error)
        else: 
            self.redirect('/login')

    def post(self, post_id):
        
        ck = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        comment = db.get(ck)
        
        if self.user and (self.user.name == comment.creator):
            content = self.request.get('content')
            user = self.user.name

            if content: 
                comment.content = content
                comment.put()
                self.render("goodCommentEdit.html")
            else:
                error = "content, please!"
                self.render("usercomment.html", content=comment.content, error=error)
        else:
            self.redirect('/blog')