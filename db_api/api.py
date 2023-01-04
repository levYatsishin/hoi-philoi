import psycopg2
from typing import Optional


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
                u_id_user INTEGER PRIMARY KEY not null,
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
                u_id_post INTEGER PRIMARY KEY not null ,
                u_id_user INTEGER not null,
                content VARCHAR not null,
                publication_date timestamp without time zone not null,
                constraint posts_users_fkey foreign key (u_id_user)
                references Users (u_id_user) on delete restrict on update cascade)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Likes (
                u_id_post INTEGER PRIMARY KEY not null,
                u_id_user INTEGER not null,
                constraint likes_users_fkey foreign key (u_id_user)
                references Users (u_id_user) on delete restrict on update cascade,
                constraint likes_posts_fkey foreign key (u_id_post)
                references Posts (u_id_post) on delete restrict on update cascade)
                """)
    conn.commit()


class DBApi:
    def __init__(self, db_name, db_host, db_user, db_pass, db_port) -> None:
        self.conn = psycopg2.connect(database=db_name,
                                     host=db_host,
                                     user=db_user,
                                     password=db_pass,
                                     port=db_port)
        self.cursor = self.conn.cursor()
        initialise_tables(self.conn, self.cursor)

    def get_user_by(self, **kwargs) -> Optional[dict]:
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

    def get_posts_by(self, **kwargs) -> Optional[list]:
        """
        This function returns list of dicts with posts info

        Possible keywords arguments:
        - u_id_post
        - u_id_user

        Example:
        api.get_post_by(u_id_post=100) # {"content": "hello", ...}
        api.get_post_by(dick='some_shit') # None

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

    def get_likes(self, post_id: int) -> Optional[int]:
        """
        This function returns number of likes by post id

        Example:
        api.get_likes(111) # 10
        api.get_likes(-1) # None

        :param post_id: post id
        :return: Return number of likes if post exists else None
        """
        self.cursor.execute(f""" SELECT count(*) FROM likes WHERE u_id_post = %s""", (post_id,))
        likes = self.cursor.fetchone()[0]

        return likes if likes else None

    def create_user(self, fields: dict) -> bool:
        """
        The function creates new user in database

        Example:
        fields = {}
        fields['username'] = 'leo'
        fields['password_hash'] = hash
        ...
        api.create_user(fields) # true
        api.create_user({}) # false

        :param fields: dict with user fields
        :return: Return true if user creation was successful else false
        """

    def create_post(self, fields: dict) -> bool:
        """
        The function create post in database

        Example:
        fields = {}
        fields['content'] = 'Hello, my name is leo. Now i tell about ...'
        fields['u_id_user'] = 1132
        ...
        api.create_post(fields) # true
        api.create_post({}) # false

        :param fields: dict with post fields
        :return: Return true if post creation was successful else false
        """
        pass

    def add_like(self, post_id: int) -> bool:
        """
        The function add like to post

        Example:
        api.add_like(1023) # true
        api.add_like(-131) # false

        :param post_id: int that contains post id
        :return: Return true if adding a like was successful else false
        """
        pass

    def close_connection(self):
        self.conn.clsoe()
        self.cursor.clsoe()
