import bloghandler

class FrontPage(bloghandler.BlogHandler):
    def get(self):
        if not self.user:
            self.render('frontpage.html')

        else: 
            self.redirect('/blog')