from BaseHandler import BaseHandler
import markdown
import torndb
import tornado.web
import unicodedata
import re
import time
from PIL import Image
from cStringIO import StringIO

page_size = 4
picPath = "./static/files/pic"

def savePostPic(fileList, user_id):
    filePaths = "";
    for i in range(len(fileList)):
        file_name = time.strftime("%Y-%m-%d-%H:%M:%S") + "_" + user_id + "_" + str(i)
        fullPath = picPath + "/" + file_name
        image = Image.open(StringIO(fileList[i]['body']))
        image.save(fullPath, "JPEG")
        filePaths += "files/pic/"+file_name + " "
    return filePaths

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
        try:
            imgPaths = savePostPic(self.request.files["imagefiles"], str(author_id))
            imageCount = len(self.request.files["imagefiles"])
        except KeyError:
            imgPaths = ""
            imageCount = 0

        self.db.execute(
            "INSERT INTO entries (author_id,slug,html,imageCount,imgPaths,"
            "published) VALUES (%s,%s,%s,%s,%s,UTC_TIMESTAMP())",
            self.current_user.id, slug, html, imageCount, imgPaths)
        self.redirect("/detail/" + slug)

class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
        if entry.imgPaths != "":
            entry.pic_paths = entry.imgPaths.strip(' ').split(' ')
        else:
            entry.pic_paths = []
        entry.author_name = self.db.get("SELECT * FROM users WHERE id = %s", entry.author_id).name
        comments = self.db.query("SELECT * FROM comments where entry_id=%s ORDER BY published "
                                "DESC", entry.id)

        results_count = len(comments)
        page = int(self.get_argument("page", 1))
        st = (page-1)*page_size
        ed = page*page_size
        ed = ed if ed < results_count else results_count+1
        comments = comments[st:ed]

        if not entry: raise tornado.web.HTTPError(404)
        self.render("detail.html", entry=entry, comments=comments, \
                            page=page, page_size=page_size, results_count=results_count)

class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, slug):
        entry_id = self.db.get("SELECT * FROM entries WHERE slug = %s", slug).id
        author_name = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id).name
        html = self.get_argument("markdown")
        self.db.execute(
            "INSERT INTO comments (author_id,entry_id,author_name,html,"
            "published) VALUES (%s,%s,%s,%s,UTC_TIMESTAMP())",
            self.current_user.id, entry_id, author_name,html)
        self.redirect("/detail/"+slug)
