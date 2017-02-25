class Post(db.Model):
    user = db.ReferenceProperty(User, collection_name="blogpost")
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    likes_list = db.ListProperty(db.Key)
    
    def render(self):
        likesCount = len(self.likes_list)
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self, count=likesCount)