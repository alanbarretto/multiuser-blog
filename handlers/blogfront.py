class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        comments = Comment.all().order('-created')
        
        self.render("front.html", posts = posts, comments=comments)
        