from google.appengine.ext import db
from support import render_str
from models.user import User

class Comment(db.Model):
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    comment_user = db.ReferenceProperty(User)
    creator = db.StringProperty()
    post_reference = db.StringProperty(required=True)
    user_Id = db.IntegerProperty()
    post_Id = db.IntegerProperty()
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", p=self)