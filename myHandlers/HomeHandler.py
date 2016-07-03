from BaseHandler import BaseHandler

<<<<<<< HEAD
page_size = 4

class HomeHandler(BaseHandler):
    def get(self, arg=None):
        if not self.current_user:
            all = True
        else:
            all = self.get_argument("all", False)
            user_id = self.current_user.id

        page = int(self.get_argument("page", 1))
        if not all:
            results_count = self.db.execute_rowcount("SELECT * FROM entries, following "
                                                "WHERE follower_id=%s and "
                                                "followed_id=author_id "
                                                "ORDER BY published ", user_id)
            st = (page-1)*page_size
            ed = page*page_size
            ed = ed if ed < results_count else results_count+1
            entries = self.db.query("SELECT * FROM entries, following "
                                                "WHERE follower_id=%s and "
                                                "followed_id=author_id "
                                                "ORDER BY published "
                                                "DESC LIMIT %s,%s", user_id, st, (ed-st))
        else:
            results_count = self.db.execute_rowcount("SELECT * FROM entries ORDER BY published "
                                "DESC")
            st = (page-1)*page_size
            ed = page*page_size
            ed = ed if ed < results_count else results_count+1
            entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                    "DESC LIMIT %s,%s", st, (ed-st))

        for entry in entries:
            entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(entry.author_id)).name
        self.render("home.html", entries=entries, page=page, page_size=page_size, results_count=results_count)
=======
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
>>>>>>> faa8d0b2fbf760d32bb7eb41553ae2c6ac1de25a

class AllPostHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
<<<<<<< HEAD
                                "DESC")
        for entry in entries:
            entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(entry.author_id)).name
        self.render("home.html", entries=entries, page=1, page_size=1000, results_count=10)
=======
                                "DESC LIMIT 5")
        for entry in entries:
            entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(entry.author_id)).name
        self.render("home.html", entries=entries)
>>>>>>> faa8d0b2fbf760d32bb7eb41553ae2c6ac1de25a
