class DBApi:
    def __init__(self) -> None:
        pass

    def get_user(self, user_id: int) -> dict:
        """
        The function get dict with user info
        :param user_id: user id
        :return: dict; Dict contains content, u_id_post, u_id_user, date, image_reference
        """
        pass

    def get_post(self, post_id: int) -> dict:
        """
        The function get dict with post info
        :param post_id: post id
        :return: dict; Dict contains u_id_user, name, username, mail, password_hash, image_reference, location, bio, tag
        """
        pass

    def get_likes(self, post_id: int) -> int:
        """
        The function get number of likes
        :param post_id: post id
        :return: number of likes
        """
        pass
