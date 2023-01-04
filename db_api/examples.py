from api import DBApi

if __name__ == "__main__":
    api = DBApi('levyatsishin', 'localhost', 'levyatsishin', '', 5432)

    # api.get_user_by show cases
    existing_user = api.get_user_by(u_id_user=1)
    not_existing_user = api.get_user_by(u_id_user=12)
    print(f"User exists: {existing_user}\nUser doesnt exist: {not_existing_user}\n")

    existing_posts = api.get_posts_by(u_id_post=1)
    not_existing_posts = api.get_posts_by(u_id_post=12)
    print(f"Posts exist: {existing_posts}\nPosts dont exist: {not_existing_posts}\n")

    existing_likes = api.get_likes(1)
    not_existing_likes = api.get_likes(-1)
    print(f"Likes for Post exists: {existing_likes}\nLikes for Post doesnt exist: {not_existing_likes}\n")


