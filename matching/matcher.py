from db_api import PostgresApi


class Matcher:
    def __init__(self, postgres_api: PostgresApi):
        self.postgres_api = postgres_api

    def get_matching_users(self, user: dict) -> list:
        """
        Returns list of users info(dicts) who have desired tags

        :param user: user info
        :return: list of users with desired tags sorted by number of intersection in tags
        """
        tags = user["tags"]
        matched_users = self.postgres_api.get_users_by_tags(tags, strict=False, exclude_id=user['u_id'])

        matched_users.sort(key=lambda a: len(set(a['tags']) & set(tags)), reverse=True)

        return matched_users
