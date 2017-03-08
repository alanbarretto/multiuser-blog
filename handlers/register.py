import signup
import models

class Register(signup.Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = models.User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = models.User.register(self.username, self.password, self.email)
            u.put()
            #login fxn sets the cookie
            self.login(u)
            self.redirect('/blog')