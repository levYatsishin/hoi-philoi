from api import DBApi

if __name__ == "__main__":
    api = DBApi('levyatsishin', 'localhost', 'levyatsishin', '', 5432)

    user = api.get_user_by(u_id_user=12)
    print(user)

