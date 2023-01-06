import traceback
from typing import Any

import psycopg2

from loguru import logger
from parse import *

from db_api.patterns import Singleton


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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subscriptions (
                u_id_user_subscribed_to INTEGER not null,
                u_id_user_who INTEGER not null,
                constraint subscriptions_users_fkey foreign key (u_id_user_subscribed_to)
                references Users (u_id_user) on delete restrict on update cascade,
                constraint subscriptions_users_fkey2 foreign key (u_id_user_who)
                references Users (u_id_user) on delete restrict on update cascade)
                """)
    conn.commit()


class PostgresApi(metaclass=Singleton):
    def __init__(self) -> None:
        self._conn = None
        self._cursor = None

    def connect(self, db_host, db_port, db_name, db_user, db_pass) -> None:
        logger.debug("PostgresDB: Connecting")
        self._conn = psycopg2.connect(database=db_name,
                                      host=db_host,
                                      user=db_user,
                                      password=db_pass,
                                      port=db_port)
        self._cursor = self._conn.cursor()
        initialise_tables(self._conn, self._cursor)
        logger.debug("PostgresDB: Connected")

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
        self._cursor.execute(f""" SELECT * FROM users WHERE {parameter} = %s""", (value,))
        user_info = self._cursor.fetchone()

        if user_info:
            self._cursor.execute(f"""SELECT column_name
                                                    FROM INFORMATION_SCHEMA.COLUMNS
                                                    WHERE TABLE_NAME=N'users'""")
            rows = self._cursor.fetchall()
            rows = [col_name[0] for col_name in rows]

            logger.debug("PostgresDB: User retrieved")
            return dict(zip(rows, user_info))
        else:
            logger.debug("PostgresDB: No users found")
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
        self._cursor.execute(f""" SELECT * FROM posts WHERE {parameter} = %s""", (value,))
        posts = self._cursor.fetchall()

        if posts:
            self._cursor.execute(f"""SELECT column_name
                                    FROM INFORMATION_SCHEMA.COLUMNS
                                    WHERE TABLE_NAME=N'posts'""")
            rows = self._cursor.fetchall()
            rows = [col_name[0] for col_name in rows]

            logger.debug("PostgresDB: Post retrieved")
            return [dict(zip(rows, post)) for post in posts]
        else:
            logger.debug("PostgresDB: No posts found")
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
        self._cursor.execute(f""" SELECT count(*) FROM likes WHERE u_id_post = %s""", (post_id,))
        likes = self._cursor.fetchone()[0]

        logger.debug("PostgresDB: Like retrieved")
        return likes

    def create_user(self, fields: dict) -> bool:
        """
        This function creates new a user in the database

        Example:

        fields.keys() = ('name', 'username', 'mail', 'password_hash')
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

            logger.debug("PostgresDB: Invalid keys in input dictionary")
            return False

        try:
            self._cursor.execute(f"""INSERT INTO users (name, username, mail, password_hash)
            VALUES (%s, %s, %s, %s)""", [fields[key] for key in keys])
            self._conn.commit()

            logger.debug("PostgresDB: User created")

        except Exception as e:
            self._cursor.execute("ROLLBACK")
            self._conn.commit()
            if type(e) == psycopg2.errors.UniqueViolation:

                violated_key = parse('duplicate key value violates unique constraint '
                                     '"users_{}_key"', e.args[0].split('\n')[0])[0]
                logger.warning(f"User with this {violated_key} already exists")
            else:
                logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
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

            logger.debug("PostgresDB: Invalid keys in input dictionary")
            return False
        try:
            self._cursor.execute(f"""INSERT INTO posts (u_id_user, content, publication_date)
                                    VALUES (%s, %s, %s)""", [fields[key] for key in keys])
            self._conn.commit()
            logger.debug("PostgresDB: Post created")

        except Exception as e:
            logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
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
            self._cursor.execute(f"""SELECT count(*) FROM likes 
                                    WHERE u_id_post = %s and u_id_user = %s""", (post_id, user_id,))

            already_liked = self._cursor.fetchone()[0]
            if not already_liked:
                self._cursor.execute(f"""INSERT INTO likes (u_id_post, u_id_user)
                VALUES (%s, %s)""", (post_id, user_id))
                self._conn.commit()
            else:
                self._cursor.execute(f"""DELETE FROM likes WHERE u_id_post = %s AND u_id_user = %s""",
                                     (post_id, user_id))
                self._conn.commit()
            logger.debug("PostgresDB: Like state changed")

        except Exception as e:
            logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
            success = False

        return success

    def get_events_by(self, **kwargs) -> list[dict[str, Any]] | None:
        """
        The function returns list of dicts with events info
        Possible keywords arguments:
            - u_id_event
            - u_id_user
        Example:
            api.get_events_by(u_id_event=212) # [{'u_id_event': 212, 'u_id_user': 312, ...}, ...]
            api.get_events_by(u_id_user=312) # [{'u_id_event': 212, 'u_id_user': 312, ...}, ...]
            api.get_events_by(name='name') # None
        :param kwargs: keywords arguments
        :return: Return list of user ids if post exists else None
        """
        pass

    def get_subscribers_by(self, **kwargs) -> list[int] | None:
        """
        This function returns list of user ids
        Possible keywords arguments:
            - u_id_user
            - u_id_subscriber
        Example:
            api.get_users_by(u_id_user=10) # [123, 2132, 21312, ...]
            api.get_users_by(u_id_subscriber=10) # [424, 312, ...]
            api.get_users_by(u_id_subscriber=-1) # []
        :param kwargs: keywords arguments
        :return: Return list of user ids if post exists else None
        """
        pass

    def create_event(self, fields: dict) -> bool:
        """
        The function create a new event in database
        :param fields: dict with event fields
        :return: Return true if post creation was successful else false
        """
        pass

    def change_subscription_state(self, user_id: int, post_id: int) -> bool:
        """
        The function of adding or removing subscriptions from the user
        :param user_id: id of the user who subscribed the person
        :param post_id: id of the subscribed person
        :return: Return True if successful else False
        """
        pass

    def drop_all_tables(self) -> None:
        self._cursor.execute("""DROP TABLE users, posts, likes, subscriptions""")
        self._conn.commit()
        logger.debug("PostgresDB: All tables successfully dropped")

    def close_connection(self) -> None:
        """
        Closes connection to the Data Base
        """

        self._conn.close()
        logger.debug("PostgresDB: Connection closed")

