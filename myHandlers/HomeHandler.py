from BaseHandler import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/all")
            return
        user_id = self.current_user.id
        entries = self.db.query("SELECT * FROM entries, following "
                                            "WHERE follower_id=%s and "
                                            "followed_id=author_id "
                                            "ORDER BY published "
                                            "DESC LIMIT 5", user_id)
        for entry in entries:
            entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(entry.author_id)).name
        self.render("home.html", entries=entries)

class AllPostHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 5")
        for entry in entries:
            entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(entry.author_id)).name
        self.render("home.html", entries=entries)
