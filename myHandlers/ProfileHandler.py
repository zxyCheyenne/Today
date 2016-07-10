from BaseHandler import BaseHandler
import bcrypt
import concurrent.futures
import torndb
import tornado.web
import tornado.escape
from tornado import gen

import time
from PIL import Image
from cStringIO import StringIO

page_size = 4
default_head_dir = "files/icon"
default_head_path = "default_icon.jpg"


image_type = ["image/gif",
              "image/jpeg",
              "image/png"]

small_image_size = 50,50
mid_image_size = 100,100
large_image_size = 250,250

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

class ProfileHandler(BaseHandler):
    def get(self, user_name):
        user = self.db.get("SELECT * FROM users WHERE name = %s", user_name)
        entries = self.db.query("SELECT * FROM entries where author_id=%s ORDER BY published "
                                "DESC", user.id)

        page = int(self.get_argument("page", 1))
        results_count = len(entries)
        st = (page-1)*page_size
        ed = page*page_size
        ed = ed if ed < results_count else results_count+1
        entries = entries[st:ed]

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
            if entry.imgPaths != "":
                entry.pic_paths = entry.imgPaths.strip(' ').split(' ')
            else:
                entry.pic_paths = []
        self.render("profile.html", entries=entries, user=user, hasFollowed=hasFollowed,\
                            page=page, page_size=page_size, results_count=results_count)

class MyProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_name = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id).name
        self.redirect("/profile/"+user_name)

def resizeWriteImage(file_name, image, size):
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(file_name, "JPEG")


class ProfileEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.db.get("SELECT * FROM users WHERE id = %s", self.current_user.id)
        self.render("profile_edit.html", user=user, error=None);

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        user_name = self.get_argument("name")

        current_user= self.db.get("SELECT * FROM users WHERE id = %s",
                             self.current_user.id)
        user = self.db.get("SELECT * FROM users WHERE name = %s",
                             self.get_argument("name"))
        if user and user.name != current_user.name:
            self.render("profile_edit.html", user=current_user, error="user name has benn used");
            return
        try:
            icon_file = self.request.files["iconFile"][0]
        except KeyError:
            self.db.execute(
                "UPDATE users SET name = %s "
                "WHERE id = %s", user_name, self.current_user.id)
            self.redirect("/profile/"+user_name)
            return
        else:
            pass
        if icon_file.content_type in image_type:
            file_size = int(self.request.headers.get('Content-Length'))
            if file_size/1024.0 > 2000.0:
                self.write("file_size should less than 2Mbytes")
                return
            name = str(self.current_user.id) + '_headimg'

            image = Image.open(StringIO(icon_file['body']))
            resizeWriteImage("./static/files/icon/small/" + name, image, small_image_size)
            resizeWriteImage("./static/files/icon/large/" + name, image, large_image_size)
            resizeWriteImage("./static/files/icon/mid/" + name, image, mid_image_size)
            self.db.execute(
                "UPDATE users SET name = %s, head_path = %s "
                "WHERE id = %s", user_name, default_head_dir+"/small/"+name, self.current_user.id)
            self.redirect("/profile/"+user_name)
        else:
            self.write("file_not_support")
        # self.redirect("/profile/"+user_name)
