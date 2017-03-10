#from handlers import blogfront, bloghandler, comments, \
#                  deletecomments, deletepost, editcomments, frontpage, likepost,\
#                  login, logout, newpost, postedit, postpage, register, signup, welcome 

#from handlers import blogfront, frontpage, login, logout, newpost, \
#                     register, signup, welcome, likepost, postcomments, \
#                     deletecomments, deletepost, editcomments, postedit, \
#                     postpage

from handlers import BlogHandler, BlogFront, FrontPage, Login, Logout, \
                     NewPost, Register, Signup, Welcome, LikePost, PostComments, \
                     DeleteComments, DeletePost, EditComments, PostEdit, \
                     PostPage 








app = webapp2.WSGIApplication([('/', FrontPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/login', Login),
                               ('/blog/postedit/([0-9]+)', PostEdit),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/newcomment/([0-9]+)', PostComments),
                               ('/blog/editcomment/([0-9]+)', EditComments),
                               ('/blog/deletecomment/([0-9]+)', DeleteComments),
                               ('/blog/like/([0-9]+)', LikePost),
                               ('/signup', Register),
                               ('/logout', Logout),
                               ('/welcome', Welcome),
                               ],
                              debug=True)
