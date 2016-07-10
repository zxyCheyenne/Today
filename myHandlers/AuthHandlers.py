import bcrypt
import torndb
import concurrent.futures
import tornado.escape
from tornado import gen

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

from BaseHandler import BaseHandler

default_head_dir = "files/icon"
default_head_path = "default_icon.jpg"

class AuthSignupHandler(BaseHandler):
    def get(self):
        self.render("signup.html", error=None)

    @gen.coroutine
    def post(self):
        user = self.db.get("SELECT * FROM users WHERE email = %s",
                             self.get_argument("email"))
        if user:
            self.render("signup.html", error="email has been registed")
            return
        user = self.db.get("SELECT * FROM users WHERE name = %s",
                             self.get_argument("name"))
        if user:
            self.render("signup.html", error="name has been userd")
            return
        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt())
        user_id = self.db.execute(
            "INSERT INTO users (email, name, hashed_password, head_path) "
            "VALUES (%s, %s, %s, %s)",
            self.get_argument("email"), self.get_argument("name"),
            hashed_password, default_head_dir+"/small/"+default_head_path)
        self.db.execute(
                    "INSERT INTO following (follower_id,followed_id,follower_name,followed_name) VALUES (%s,%s,%s,%s)",
                    user_id, user_id, self.get_argument("name"),self.get_argument("name"))
        self.set_secure_cookie("today_user", str(user_id))
        self.xsrf_cookie_kwargs=dict(user_name = self.get_argument("name"))
        self.redirect(self.get_argument("next", "/"))

class AuthSigninHandler(BaseHandler):
    def get(self):
        if not self.any_user_exists():
            self.redirect("/auth/signup")
        else:
            self.render("signin.html", error=None)

    @gen.coroutine
    def post(self):
        user = self.db.get("SELECT * FROM users WHERE email = %s",
                             self.get_argument("email"))
        if not user:
            self.render("signin.html", error="email not found")
            return
        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8(user.hashed_password))
        if hashed_password == user.hashed_password:
            self.set_secure_cookie("today_user", str(user.id),30,2)
            self.xsrf_cookie_kwargs=dict(user_name = user.name)
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("signin.html", error="incorrect password")

class AuthSignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("today_user")
        self.redirect(self.get_argument("next", "/"))
