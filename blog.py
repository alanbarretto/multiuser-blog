import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'warriors'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    #checks to see if the user is logged in or not

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

##### user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

#how to verify passwords
def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

#This creates the ancestor element in the database to store all of our users
def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    #looks for the user by name
    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    #creates the user but doesn't store it yet in the database
    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


##### blog stuff

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    creator = db.StringProperty()
    likes_list = db.ListProperty(db.Key)
    
    def render(self):
        likesCount = len(self.likes_list)
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self, count=likesCount)

class Comment(db.Model):
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    creator = db.StringProperty()
    post_reference = db.StringProperty(required=True)
    user_Id = db.IntegerProperty()
    post_Id = db.IntegerProperty()
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", p=self)

class BlogFront(BlogHandler):
    def get(self):
        posts = greetings = Post.all().order('-created')
        comments = Comment.all().order('-created')
        
        self.render("front.html", posts = posts, comments=comments)
        
class PostPage(BlogHandler):
    def get(self, post_id):
        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)
        
        subject = p.subject
        comments = Comment.all().order('-post_reference')
        
        if not p:
            self.error(404)
            return

        self.render("permalink.html", post = p, comments=comments)

class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')
        user = self.user.name

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, creator=user)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class PostEdit(BlogHandler):

    def get(self, post_id):

        k = db.Key.from_path("Post", int(post_id), parent=blog_key())
        p = db.get(k)

        if not p:
            self.redirect('/')

        if self.user and (self.user.name == p.creator):
            self.render("newpost.html", subject=p.subject,
                        content=p.content)
        elif not self.user:
            self.redirect('/')
        else:
            posts = greetings = Post.all().order('-created')
            comments = Comment.all().order('-created')
            error = "You can only edit posts you created."
            self.render('front.html', posts=posts,
                        comments=comments, error=error)

    def post(self, post_id):
        if not self.user:
            self.redirect('/')

        k = db.Key.from_path("Post", int(post_id), parent=blog_key())
        p = db.get(k)

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

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BlogHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            #login fxn sets the cookie
            self.login(u)
            self.redirect('/blog')

class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/')

class Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')

class FrontPage(BlogHandler):
    def get(self):
        if not self.user:
            self.render('frontpage.html')

        else: 
            self.redirect('/blog')

class Comments(BlogHandler):
    def get(self, post_id):
        if not self.user:
            self.redirect('/blog')
        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)

        if self.user:
            self.render("usercomment.html")
        else:
            self.redirect('/')

    def post(self, post_id):
        if not self.user:
            self.redirect('/login')

        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)
        content = self.request.get('content')
        user = self.user.name

        if content:
            c = Comment(parent=blog_key(), post_reference=p.subject, content=content, creator=user)
            c.put()
            self.render("successfulcomment.html")
        else:
            error = "subject and content, please!"
            self.render("usercomment.html", error=error)
    
class EditComments(BlogHandler):
    def get(self, post_id):
        ck = db.Key.from_path('Comment', int(post_id), parent=blog_key())
        comment = db.get(ck)
        
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


class LikePost(BlogHandler):
    def get(self, post_id):
        
        k = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(k)

        if  self.user and (self.user.name != p.creator):
            if not self.user.key() in p.likes_list:
                p.likes_list.append(self.user.key())
                p.put()
                self.render("thanksLike.html")
            else: 
                self.redirect('/blog')
            
        elif self.user and (self.user.name == p.creator):
            error = "You can't Like your own Posts!"
            posts = db.GqlQuery("select * from Post order by created desc limit 10")
            comments = db.GqlQuery("select * from Comment order by created desc")
            self.render("front.html", posts=posts, comments=comments, error=error)
        else:
            self.redirect('/login')

app = webapp2.WSGIApplication([('/', FrontPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/login', Login),
                               ('/blog/postedit/([0-9]+)', PostEdit),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/newcomment/([0-9]+)', Comments),
                               ('/blog/editcomment/([0-9]+)', EditComments),
                               ('/blog/deletecomment/([0-9]+)', DeleteComments),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/signup', Register),
                               ('/logout', Logout),
                               ('/welcome', Welcome),
                               ],
                              debug=True)
