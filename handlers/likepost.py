import bloghandler
import support

class LikePost(bloghandler.BlogHandler):
    def get(self, post_id):
        
        k = support.db.Key.from_path('Post', int(post_id), parent=support.blog_key())
        p = support.db.get(k)

        if  self.user and (self.user.name != p.creator):
            if not self.user.key() in p.likes_list:
                p.likes_list.append(self.user.key())
                p.put()
                self.render("thanksLike.html")
            else: 
                self.redirect('/blog')
            
        elif self.user and (self.user.name == p.creator):
            error = "You can't Like your own Posts!"
            posts = support.db.GqlQuery("select * from Post order by created desc limit 10")
            comments = support.db.GqlQuery("select * from Comment order by created desc")
            self.render("front.html", posts=posts, comments=comments, error=error)
        else:
            self.redirect('/login')