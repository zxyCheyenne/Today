from BaseHandler import BaseHandler

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
            if entry.imgPaths != "":
                entry.pic_paths = entry.imgPaths.strip(' ').split(' ')
            else:
                entry.pic_paths = []
        self.render("home.html", entries=entries, page=page, page_size=page_size, results_count=results_count)
