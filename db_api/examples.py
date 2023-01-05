from api import DBApi
import datetime
import os

if __name__ == "__main__":
    db_password = os.environ["POSTGRES_PASS"]
    db_ip = os.environ["POSTGRES_IP"]
    api = DBApi('postgres', db_ip, 'admin', db_password, 5432)

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

    user_fields = {'name': "Вася Пупкин", 'userasname': "dvasya", 'mail': "ddds", 'password_hash': "sdcsfsdcvsdcvsdc"}
    print("User created:", api.create_user(user_fields))

    print("Like: ", api.change_like_state(1, 1))

    post_fields = {'u_id_user': 1, 'content': "hi!", 'publication_date': datetime.datetime.now()}
    print("Create post: ", api.create_post(post_fields))

    api2 = DBApi('postgres', db_ip, 'admin', db_password, 5432)

    print(f"Single tone works: {api2 is api}")
