from BaseHandler import BaseHandler
import markdown
import torndb
import tornado.web
import unicodedata
import re


class PublishHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        entry = None
        self.render("post.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        html = markdown.markdown(self.get_argument("markdown"))
        author_id = self.current_user.id
        author_name = self.db.get("SELECT * FROM users WHERE id = %s", int(author_id)).name
        counter = 0;
        prefix = unicodedata.normalize("NFKD", author_name).encode(
                "ascii", "ignore")
        prefix = re.sub(r"[^\w]+", " ", prefix)
        prefix = "-".join(prefix.lower().strip().split())
        while True:
            slug = prefix + "-" + str(counter)
            e = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
            if not e: break
            counter += 1

        self.db.execute(
            "INSERT INTO entries (author_id,slug,html,"
            "published) VALUES (%s,%s,%s,UTC_TIMESTAMP())",
            self.current_user.id, slug, html)
        self.redirect("/detail/" + slug)

class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
        entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", entry.author_id).name
        comments = self.db.query("SELECT * FROM comments where entry_id=%s ORDER BY published "
                                "DESC LIMIT 5", entry.id)
        if not entry: raise tornado.web.HTTPError(404)
        self.render("detail.html", entry=entry, comments=comments)

class CommentHandler(BaseHandler):
    def post(self, slug):
        entry_id = self.db.get("SELECT * FROM entries WHERE slug = %s", slug).id
        author_name = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id).name
        html = self.get_argument("markdown")
        self.db.execute(
            "INSERT INTO comments (author_id,entry_id,author_name,html,"
            "published) VALUES (%s,%s,%s,%s,UTC_TIMESTAMP())",
            self.current_user.id, entry_id, author_name,html)
        self.redirect("/detail/"+slug)
