class DeletePost(BlogHandler):
    def get(self, post_id):
        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)

        if not p:
            self.error(404)
            return
        if self.user and (self.user.name == p.creator):
            self.render("deletePost.html", subject= p.subject)

        elif self.user and (self.user.name != p.creator):
            error = "You can only delete posts you created!"
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            self.render("front.html", posts=posts, comments=comments, error=error)
        else:
            self.redirect('/login')

    def post(self, post_id):
        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)

        if self.user:   
            db.delete(k)
            self.render("goodPostDelete.html")