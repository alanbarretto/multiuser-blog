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