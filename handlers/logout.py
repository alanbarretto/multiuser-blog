import bloghandler

class Logout(bloghandler.BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')