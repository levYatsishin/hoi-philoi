import psycopg2

from loguru import logger
from parse import parse
import traceback
from typing import Any

from db_api.patterns import Singleton


def initialise_tables(conn, cursor) -> None:
    """
    Initialise tables in Data Base

    :param conn: db connection
    :param cursor: conn.cursor()
    :return:
    """

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
                u_id SERIAL PRIMARY KEY not null,
                name VARCHAR(100) not null, 
                username VARCHAR(50) not null unique,
                mail  VARCHAR(500) not null unique,
                password_hash VARCHAR(500) not null, 
                image VARCHAR,
                location VARCHAR(500),
                bio VARCHAR,
                tags VARCHAR)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Posts (
                u_id SERIAL PRIMARY KEY not null ,
                u_id_user INTEGER not null,
                content VARCHAR not null,
                publication_date timestamp without time zone not null,
                image VARCHAR,
                constraint posts_users_fkey foreign key (u_id_user)
                references Users (u_id) on delete restrict on update cascade)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Likes (
                u_id_post INTEGER not null,
                u_id_user INTEGER not null,
                constraint likes_users_fkey foreign key (u_id_user)
                references Users (u_id) on delete restrict on update cascade,
                constraint likes_posts_fkey foreign key (u_id_post)
                references Posts (u_id) on delete restrict on update cascade)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subscriptions (
                u_id_user_subscribed_to INTEGER not null,
                u_id_user_who INTEGER not null,
                constraint subscriptions_users_fkey foreign key (u_id_user_subscribed_to)
                references Users (u_id) on delete restrict on update cascade,
                constraint subscriptions_users_fkey2 foreign key (u_id_user_who)
                references Users (u_id) on delete restrict on update cascade)
                """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Events (
                u_id SERIAL PRIMARY KEY not null ,
                u_id_user INTEGER not null,
                content VARCHAR not null,
                publication_date timestamp without time zone not null,
                time_start timestamp without time zone not null,
                time_end timestamp without time zone not null,
                location VARCHAR not null,
                image VARCHAR,
                constraint events_users_fkey foreign key (u_id_user)
                references Users (u_id) on delete restrict on update cascade)
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

    def _generic_create(self, table: str, input_fields: dict, required_keys: list) -> bool:
        """
        This is a generic function for creating new rows in the Data Base

        :param table: table name in which row is being created
        :param input_fields: dictionary  {column_name:value}
        :param required_keys: keys which must be in input_fields.keys()
        :return: True if success else False
        """
        success = True

        if list(input_fields.keys()) != required_keys:
            logger.debug("PostgresDB: Invalid keys in input dictionary")
            return False

        try:
            self._cursor.execute(f"""INSERT INTO {table} ({", ".join([col for col in required_keys])})
                                     VALUES ({', '.join(['%s' for _ in required_keys])})""",
                                 [input_fields[key] for key in required_keys])
            self._conn.commit()

            logger.debug(f"PostgresDB: {table} created")

        except Exception as e:
            self._cursor.execute("ROLLBACK")
            self._conn.commit()
            if type(e) == psycopg2.errors.UniqueViolation:

                violated_key = parse('duplicate key value violates '
                                     'unique constraint "{}"', e.args[0].split('\n')[0])[0]
                logger.warning(f"Creation aborted: row with this {violated_key} already exists")
            else:
                logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
            success = False

        finally:
            return success

    def _generic_change_state(self, table, input_info: dict) -> bool:
        """
        This is a generic function for changing state of some of the 2-states parameters in the Data Base

        :param table: id of first entity of the process
        :param input_info: what row to change if form of {column: value, column, value}
        :return: Return True if successful else False
        """
        success = True

        try:
            values = list(input_info.items())

            column1 = values[0][0]
            column2 = values[1][0]
            value1 = values[0][1]
            value2 = values[1][1]

            self._cursor.execute(f"""SELECT count(*) FROM {table} 
                                            WHERE {values[0][0]} = %s and {column2} = %s""", (value1, value2,))

            current_state = self._cursor.fetchone()[0]
            if not current_state:
                self._cursor.execute(f"""INSERT INTO {table} ({column1}, {column2})
                        VALUES (%s, %s)""", (value1, value2))
                self._conn.commit()
            else:
                self._cursor.execute(f"""DELETE FROM {table} WHERE {column1} = %s AND {column2} = %s""",
                                     (value1, value2))
                self._conn.commit()
            logger.debug(f"PostgresDB: {table} state changed")

        except Exception as e:
            logger.error(f"Error: {e}\n Traceback: {traceback.format_exc()}")
            success = False

        return success

    def _generic_get_by(self, table: str, parameter: str, value: str | int, limit=10) -> list[dict] | None:
        """
        This is a generic function for getting rows from the Data Bast

        :param table: in which table the search happens
        :param parameter: by which column
        :param value: what is the required value
        :return:
        """

        self._cursor.execute(f""" SELECT * FROM {table} WHERE {parameter} = %s
                                  order by u_id desc limit {limit}""", (value,))
        info = self._cursor.fetchall()

        if info:
            self._cursor.execute(f"""SELECT column_name
                                                    FROM INFORMATION_SCHEMA.COLUMNS
                                                    WHERE TABLE_NAME=N'{table}'""")
            rows = self._cursor.fetchall()
            rows = [col_name[0] for col_name in rows]

            logger.debug(f"PostgresDB: {table} retrieved")
            return [dict(zip(rows, info[x])) for x in range(len(info))]
        else:
            logger.debug(f"PostgresDB: No {table} found")
            return None

    def create_user(self, fields: dict) -> bool:
        """
        This function creates new a user in the database

        fields.keys() = ('name', 'username', 'mail', 'password_hash')
            - name: str
            - username: str
            - mail: str
            - password_hash: str

        :param fields: dict with user fields
        :return: Return True if user creation was successful else False
        """
        required_keys = ['name', 'username', 'mail', 'password_hash']

        return self._generic_create('users', fields, required_keys)

    def create_post(self, fields: dict) -> bool:
        """
        This function creates a new post in the database

        Example:
        fields.keys() = ('u_id_user', 'content', 'publication_date')
            - u_id_user: int
            - content: str
            - publication_date: datatime object

        :param fields: dict with post fields
        :return: Return True if post creation was successful else False
        """
        required_keys = ['u_id_user', 'content', 'publication_date']

        return self._generic_create('posts', fields, required_keys)

    def create_event(self, fields: dict) -> bool:
        """
        fields.keys() = ('u_id_user', 'content', 'publication_date', 'time_start', 'time_end', 'location')
            - u_id_user: int
                - creators' id
            - content: str
                - description of the event
            - publication_date: datatime object
            - time_start: datatime object
            - time_end: datatime object
            - location: str

        The function create a new event in database
        :param fields: dict with event fields
        :return: Return true if post creation was successful else false
        """
        required_keys = ['u_id_user', 'content', 'publication_date', 'time_start', 'time_end', 'location']

        return self._generic_create('events', fields, required_keys)

    def change_like_state(self, user_id: int, post_id: int) -> bool:
        """
        This function adds or removes like from a post.

        :param user_id: id of the user who liked the post
        :param post_id: id of the liked post
        :return: Return True if successful else False
        """
        info = {'u_id_user': user_id, 'u_id_post': post_id}

        return self._generic_change_state('likes', info)

    def change_subscription_state(self, user_id_who_subscribing: int, user_id_subscribing_to: int) -> bool:
        """
        The function of adding or removing subscriptions from the user

        :param user_id_who_subscribing: id of the user who subscribed to the person(user_id_subscribing_to)
        :param user_id_subscribing_to: id of the user with new subscription
        :return: Return True if successful else False
        """
        info = {'u_id_user_who': user_id_who_subscribing, 'u_id_user_subscribed_to': user_id_subscribing_to}

        return self._generic_change_state('subscriptions', info)

    def get_user_by(self, parameter: str, value: str | int) -> dict | None:
        """
        This function returns dict with user info

        Possible parameters:
        - 'u_id'
            - user id
        - 'username'
        - 'mail'

        :param parameter: by what column the search happens
        :param value: for which value the search happens
        :return: Returns dict that contains information about the user
        """
        user = self._generic_get_by('users', parameter, value)
        return user[0] if user else None

    def get_posts_by(self, parameter: str, value: int) -> list[dict[str, Any]] | None:
        """
        This function returns list of dicts with posts info

         Possible parameters:
            - u_id
                - id of the post
            - u_id_user
                - id of the user(to get all his posts)

        :param parameter: by what column the search happens
        :param value: for which value the search happens
        :return: Return list of dict that contains info about the post(s) if post exists else None
        """

        return self._generic_get_by('posts', parameter, value)

    def get_events_by(self, parameter: str, value: int) -> list[dict[str, Any]] | None:
        """
        The function returns list of dicts with events info
        Possible keywords arguments:
            - u_id
                - id of the event
            - u_id_user
                - id of the user(to get all his events)

        :param parameter: by what column the search happens
        :param value: for which value the search happens
        :return: Return list of dicts that contains info about the event(s) if event exists else None
        """

        return self._generic_get_by('events', parameter, value)

    def get_subscribers_by(self, parameter: str, value: int) -> list[int]:
        """
        This function returns list of user ids
        Possible keywords arguments:
            - u_id_user_who
                - id of the user who subscribed to the person(user_id_subscribing_to)
            - u_id_user_subscribed_to
                - id of the user with mew subscription


        :param parameter: by what column the search happens
        :param value: for which value the search happens
        :return: Return list of subscribers ids
        """

        column_to_get = "u_id_user_who" if parameter == "u_id_user_who" else "u_id_user_subscribed_to"
        self._cursor.execute(f"""SELECT {column_to_get} FROM subscriptions WHERE {parameter} = %s""", (value,))
        subscriptions = self._cursor.fetchall()

        logger.debug("PostgresDB: Subscriptions retrieved")
        return subscriptions

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

    def is_subscribed(self, user_id_who_subscribing: int, user_id_subscribing_to: int) -> bool:
        """

        :param user_id_who_subscribing: id of the user who subscribed to the person(user_id_subscribing_to)
        :param user_id_subscribing_to: id of the user with new subscription
        :return: True if user_id_who_subscribing sis subscribed to user_id_subscribing_to
        """

        self._cursor.execute(f"""SELECT count(*) FROM subscriptions
                                        WHERE u_id_user_subscribed_to = %s and u_id_user_who = %s""",
                             (user_id_subscribing_to, user_id_who_subscribing,))

        is_subscribed = self._cursor.fetchone()[0]

        if is_subscribed:
            return True
        else:
            return False

    def _drop_all_tables(self) -> None:
        self._cursor.execute("""DROP TABLE users, posts, events, likes, subscriptions""")
        self._conn.commit()
        logger.debug("PostgresDB: All tables successfully dropped")

    def close_connection(self) -> None:
        """
        Closes connection to the Data Base
        """

        self._conn.close()
        logger.debug("PostgresDB: Connection closed")

