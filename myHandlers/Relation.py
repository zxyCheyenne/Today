from BaseHandler import BaseHandler
import markdown
import torndb
import tornado.web
import unicodedata
import re

page_size = 4


class FollowHandler(BaseHandler):
    def get(self, user_name):
        current_user = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id)
        target_user= self.db.get("SELECT * FROM users WHERE name = %s", user_name)
        item = self.db.get("SELECT * FROM following WHERE follower_id = %s and followed_id=%s", 
                                    current_user.id, target_user.id)
        if item:
            self.redirect("/profile/"+user_name)
            return
        self.db.execute(
            "INSERT INTO following (follower_id,followed_id,follower_name,followed_name) VALUES (%s,%s,%s,%s)",
            current_user.id, target_user.id, current_user.name,target_user.name)
        self.redirect("/profile/"+user_name)

class UnFollowHandler(BaseHandler):
    def get(self, user_name):
        current_user = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id)
        target_user= self.db.get("SELECT * FROM users WHERE name = %s", user_name)
        item = self.db.get("SELECT * FROM following WHERE follower_id = %s and followed_id=%s", 
                                    current_user.id, target_user.id)
        if current_user.id == target_user.id:
            self.redirect("/profile/"+user_name)
            return
        if not item:
            self.redirect("/profile/"+user_name)
            return
        self.db.execute("DELETE FROM following WHERE follower_id=%s and followed_id=%s",
                                current_user.id, target_user.id)
        self.redirect("/profile/"+user_name)

class MyFollowerHandler(BaseHandler):
    def get(self):
        followers = self.db.query("SELECT * FROM following f,users u WHERE f.followed_id = %s AND u.id = f.follower_id AND u.id != %s", 
                                    self.current_user.id, self.current_user.id)
        self.render("followers.html", followers=followers)

class MyFollowHandler(BaseHandler):
    def get(self):
        follows = self.db.query("SELECT * FROM following f,users u WHERE f.follower_id = %s AND u.id = f.followed_id AND u.id != %s", 
                                    self.current_user.id, self.current_user.id)
        self.render("follows.html", follows=follows)
