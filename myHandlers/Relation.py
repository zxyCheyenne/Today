from BaseHandler import BaseHandler
import markdown
import torndb
import tornado.web
import unicodedata
import re

class ProfileHandler(BaseHandler):
    def get(self, user_name):
        user = self.db.get("SELECT * FROM users WHERE name = %s", user_name)
        entries = self.db.query("SELECT * FROM entries where author_id=%s ORDER BY published "
                                "DESC LIMIT 5", user.id)
        current_user = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id)
        target_user= self.db.get("SELECT * FROM users WHERE name = %s", user_name)
        item = self.db.get("SELECT * FROM following WHERE follower_id = %s and followed_id=%s", 
                                    current_user.id, target_user.id)
        if item:
            hasFollowed=True
        else:
            hasFollowed=False
        for entry in entries:
            entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(entry.author_id)).name
        self.render("profile.html", entries=entries, user=user, hasFollowed=hasFollowed)

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
        if not item:
            self.redirect("/profile/"+user_name)
            return
        self.db.execute("DELETE FROM following WHERE follower_id=%s and followed_id=%s",
                                current_user.id, target_user.id)
        self.redirect("/profile/"+user_name)

class MyFollowerHandler(BaseHandler):
    def get(self):
        followings = self.db.query("SELECT * FROM following WHERE followed_id = %s", 
                                    self.current_user.id)
        self.render("followers.html", followings=followings)

class MyFollowHandler(BaseHandler):
    def get(self):
        followings = self.db.query("SELECT * FROM following WHERE follower_id = %s", 
                                    self.current_user.id)
        self.render("follows.html", followings=followings)

class MyProfileHandler(BaseHandler):
    def get(self):
        user_name = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id).name
        self.redirect("/profile/"+user_name)
