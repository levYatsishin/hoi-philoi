from api import DBApi
import datetime
import os

if __name__ == "__main__":
    db_password = os.environ["POSTGRES_PASS"]
    db_ip = os.environ["POSTGRES_IP"]

    api = DBApi('postgres', db_ip, 'admin', db_password, 5432)
    api_2 = DBApi('postgres', db_ip, 'admin', db_password, 5432)
    print(f"Single tone works: {api_2 is api}")

    user_fields = {'name': "Вася Пупкин", 'username': "dv1asya", 'mail': "d2dds", 'password_hash': "sdcsfsdcvsdcvsdc"}
    print("User created:", api.create_user(user_fields))
    post_fields = {'u_id_user': 1, 'content': "hi!", 'publication_date': datetime.datetime.now()}
    print("Create post: ", api.create_post(post_fields))

    existing_user = api.get_user_by(u_id_user=1)
    not_existing_user = api.get_user_by(u_id_user=12)
    print(f"User exists: {existing_user}\nUser doesnt exist: {not_existing_user}\n")

    existing_posts = api.get_posts_by(u_id_post=1)
    not_existing_posts = api.get_posts_by(u_id_post=12)
    print(f"Posts exist: {existing_posts}\nPosts dont exist: {not_existing_posts}\n")
