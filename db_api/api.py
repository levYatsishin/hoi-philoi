class DBApi:
    def __init__(self) -> None:
        pass

    def get_user_by(self, **kwargs) -> dict:
        """
        Gets dict with user info

        Example:
        api.get_user_by(username='leo') # {"u_id_user": 213123, ...}
        api.get_post_by(name=231) # None

        :param kwargs: keywords arguments
        :return: Return dict thatА contains u_id_user, name, username, mail, password_hash, image_reference, location,
        bio, tag. If the user is not found return None
        """
        pass

    def get_posts_by(self, **kwargs) -> list[dict]:
        """
        Gets list of dicts with post info

        Possible keywords arguments:
        - u_id_post
        - u_id_user



        Example:
        api.get_posts_by(u_id_post=100) # [{"content": "hello", ...}, ...]
        api.get_posts_by(dick='some_shit') # None

        :param kwargs: keywords arguments
        :return: Return list of dict where dict contains content, u_id_post, u_id_user, date, image_reference if post exists
         else None
        """
        pass

    def get_likes(self, post_id: int) -> int:
        """
        Gets number of likes

        Example:
        api.get_likes(111) # 10
        api.get_likes(-1) # None

        :param post_id: post id
        :return: Return number of likes if post exists else None
        """
        pass

    def create_user(self, fields: dict) -> bool:
        """
        Gets create new user in database

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
        pass

    def create_post(self, fields: dict) -> bool:
        """
        Creates post in database

        Example:
        fields = {}
        fields['content'] = 'Hello, my name is leo. Now I tell about ...'
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
        Adds like to post

        Example:
        api.add_like(1023) # true
        api.add_like(-131) # false

        :param post_id: int that contains post id
        :return: Return true if adding a like was successful else false
        """
        pass
