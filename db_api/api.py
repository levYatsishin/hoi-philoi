from typing import Any
import psycopg2


def initialise_tables(conn, cursor) -> None:
    """
    Initialise tables in Data Base

    :param conn: db connection
    :param cursor: conn.cursor()
    :return:
    """

    # TODO: add image ref

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
                u_id_user SERIAL PRIMARY KEY not null,
                name VARCHAR(100) not null, 
                username VARCHAR(50) not null unique,
                mail  VARCHAR(500) not null unique,
                password_hash VARCHAR(500) not null, 
                location VARCHAR(500),
                bio VARCHAR,
                tags VARCHAR)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Posts (
                u_id_post SERIAL PRIMARY KEY not null ,
                u_id_user INTEGER not null,
                content VARCHAR not null,
                publication_date timestamp without time zone not null,
                constraint posts_users_fkey foreign key (u_id_user)
                references Users (u_id_user) on delete restrict on update cascade)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Likes (
                u_id_post INTEGER not null,
                u_id_user INTEGER not null,
                constraint likes_users_fkey foreign key (u_id_user)
                references Users (u_id_user) on delete restrict on update cascade,
                constraint likes_posts_fkey foreign key (u_id_post)
                references Posts (u_id_post) on delete restrict on update cascade)
                """)
    conn.commit()


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


class DBApi(Singleton):
    def __init__(self, db_name, db_host, db_user, db_pass, db_port) -> None:
        self.conn = psycopg2.connect(database=db_name,
                                     host=db_host,
                                     user=db_user,
                                     password=db_pass,
                                     port=db_port)
        self.cursor = self.conn.cursor()
        initialise_tables(self.conn, self.cursor)

    def get_user_by(self, **kwargs) -> dict | None:
        """
        This function returns dict with user info

        Possible keywords arguments:
        - u_id_user
        - username
        - mail

        Example:
        api.get_user_by(username='leo') # {"u_id_user": 213123, ...}
        api.get_post_by(name=231) # None

        :param kwargs: PARAM_NAME=PARAM_VALUE – one pair only
        :return: Returns dict that contains u_id_user, name, username, mail, password_hash, image_reference, location,
        bio, tag. If the user is not found returns None
        """

        parameter, value = list(kwargs.items())[0]
        self.cursor.execute(f""" SELECT * FROM users WHERE {parameter} = %s""", (value,))
        user_info = self.cursor.fetchone()

        if user_info:
            self.cursor.execute(f"""SELECT column_name
                                                    FROM INFORMATION_SCHEMA.COLUMNS
                                                    WHERE TABLE_NAME=N'users'""")
            rows = self.cursor.fetchall()
            rows = [col_name[0] for col_name in rows]

            return dict(zip(rows, user_info))
        else:
            return None

    def get_posts_by(self, **kwargs) -> list[dict[str, Any]] | None:
        """
        This function returns list of dicts with posts info

        Possible keywords arguments:
            - u_id_post
            - u_id_user

        Example:
        api.get_posts_by(u_id_post=100) # [{"content": "hello", ...}, ...]
        api.get_posts_by(u_id_post=-1) # None

        :param kwargs: keywords arguments
        :return: Return list of dict that contains content, u_id_post, u_id_user, date, image_reference if post exists
         else None
        """

        parameter, value = list(kwargs.items())[0]
        self.cursor.execute(f""" SELECT * FROM posts WHERE {parameter} = %s""", (value,))
        posts = self.cursor.fetchall()

        if posts:
            self.cursor.execute(f"""SELECT column_name
                                    FROM INFORMATION_SCHEMA.COLUMNS
                                    WHERE TABLE_NAME=N'posts'""")
            rows = self.cursor.fetchall()
            rows = [col_name[0] for col_name in rows]

            return [dict(zip(rows, post)) for post in posts]
        else:
            return None

    def get_likes(self, post_id: int) -> int:
        """
        This function returns number of likes by post id

        Example:
        api.get_likes(111) # 10
        api.get_likes(-1) # None

        :param post_id: post id
        :return: Return number of likes. If post does not also exist returns 0
        """
        self.cursor.execute(f""" SELECT count(*) FROM likes WHERE u_id_post = %s""", (post_id,))
        likes = self.cursor.fetchone()[0]

        return likes

    def create_user(self, fields: dict) -> bool:
        """
        This function creates new a user in the database

        Example:

        fields.keys() = (name, username, mail, password_hash)
            - name: str
            - username: str
            - mail: str
            - password_hash: str
        fields['username'] = 'leo'
        fields['password_hash'] = hash
        ...
        api.create_user(fields) # true
        api.create_user({}) # false

        :param fields: dict with user fields
        :return: Return true if user creation was successful else false
        """
        success = True

        keys = ['name', 'username', 'mail', 'password_hash']
        if list(fields.keys()) != keys:
            return False

        try:
            self.cursor.execute(f"""INSERT INTO users (name, username, mail, password_hash)
            VALUES (%s, %s, %s, %s)""", [fields[key] for key in keys])
            self.conn.commit()

        except psycopg2.errors.UniqueViolation:
            success = False

        finally:
            return success

    def create_post(self, fields: dict) -> bool:
        """
        This function creates a new post in the database

        Example:
        fields.keys() = ('u_id_user', 'content', 'publication_date')
            - u_id_user: int
            - content: str
            - publication_date: datatime object
        fields['content'] = 'Hello, my name is Leo. Now i will tell you about ...'
        fields['u_id_user'] = 1132
        ...
        api.create_post(fields) # true
        api.create_post({}) # false

        :param fields: dict with post fields
        :return: Return true if post creation was successful else false
        """
        success = True

        keys = ['u_id_user', 'content', 'publication_date']
        if list(fields.keys()) != keys:
            return False
        try:
            self.cursor.execute(f"""INSERT INTO posts (u_id_user, content, publication_date)
                                    VALUES (%s, %s, %s)""", [fields[key] for key in keys])
            self.conn.commit()

        except psycopg2.errors.ForeignKeyViolation:
            success = False

        finally:
            return success

    def change_like_state(self, user_id: int, post_id: int) -> bool:
        """
        This function adds or removes like from a post.

        :param user_id: id of the user who liked the post
        :param post_id: id of the liked post
        :return: Return True if successful else False
        """
        success = True

        try:
            self.cursor.execute(f"""SELECT count(*) FROM likes 
                                    WHERE u_id_post = %s and u_id_user = %s""", (post_id, user_id,))

            already_liked = self.cursor.fetchone()[0]
            if not already_liked:
                self.cursor.execute(f"""INSERT INTO likes (u_id_post, u_id_user)
                VALUES (%s, %s)""", (post_id, user_id))
                self.conn.commit()
            else:
                self.cursor.execute(f"""DELETE FROM likes WHERE u_id_post = %s AND u_id_user = %s""",
                                    (post_id, user_id))
                self.conn.commit()
        except psycopg2.errors.ForeignKeyViolation:
            success = False

        return success

    def close_connection(self) -> None:
        """
        Closes connection to the Data Base
        """

        self.conn.clsoe()
        self.cursor.clsoe()
