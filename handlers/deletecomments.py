class DeleteComments(BlogHandler):

    def get(self, post_id):

        ck = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        comment = db.get(ck)
        
        if not comment:
            self.error(404)
            return

        if self.user and (self.user.name == comment.creator):
            self.render("deletepage.html", comment=comment.content)

        elif self.user and (self.user.name != comment.creator):
            error = "You can only delete comments you created"
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            self.render('front.html', posts=posts,
                        comments=comments, error=error)
        
        else: 
            self.redirect('/login')


    def post(self, post_id):
        ck = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        comment = db.get(ck)

        if self.user:
            db.delete(ck)
            self.render("deletedComment.html")