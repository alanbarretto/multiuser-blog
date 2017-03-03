import BlogHandler

class FrontPage(BlogHandler):
    def get(self):
        if not self.user:
            self.render('frontpage.html')

        else: 
            self.redirect('/blog')