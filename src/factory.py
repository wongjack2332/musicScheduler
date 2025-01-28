from typing import Any
from database_utils import get_connection, run_sql, close_connection
from models import User, Student, MusicTeacher, SchoolTeacher


class UserFactory:
    type_to_obj = {
        "Student": Student,
        "MusicTeacher": MusicTeacher,
        "SchoolTeacher": SchoolTeacher
    }

    def __init__(self):
        self.connection, self.cursor = get_connection()

    def sql_get(self, userid: int):

        self.userid = userid
        user = run_sql(
            self.cursor, f"SELECT * FROM users WHERE userid = {userid}")

        if len(user) != 1:
            raise LookupError("duplicate uid")

        user = user[0]
        user = dict(user, **self.get_user_type(user['usertype']))
        del user['password']
        user_type = user['usertype'].title()  # different names for user types

        if self.type_to_obj.get(user_type) is not None:
            self.user = self.type_to_obj[user_type](**user)
        return self.user

    def get_user_type(self, user_type: str):
        sql = f"SELECT * FROM {user_type}s WHERE userid = {self.userid}"
        dct = run_sql(self.cursor, sql)
        if len(dct) != 1:
            raise LookupError("duplicate or missing uid")
        return dct[0]

    def sql_create(self, usertype: str = "Student"):
        if usertype not in ["Student", "MusicTeacher", "SchoolTeacher"]:
            raise TypeError("Invalid user type")

        create_user = "INSERT INTO users VALUES ()"

        run_sql(self.cursor, create_user)
        result = run_sql(self.cursor, "SELECT LAST_INSERT_ID()")
        self.userid = result[0]['LAST_INSERT_ID()']

        user = self.type_to_obj[usertype](
            userid=self.userid, usertype=usertype, **self.create_usertype(usertype))

        self.connection.commit()
        return user

    def create_usertype(self, usertype: str):
        sql = f"INSERT INTO {usertype}s (userid) VALUES ({self.userid})"
        run_sql(self.cursor, sql)
        return {'studentid': run_sql(self.cursor, f"SELECT LAST_INSERT_ID()")[0]['LAST_INSERT_ID()']}


if __name__ == "__main__":
    factory = UserFactory()
    print(factory.sql_create(usertype="Student"))
    # print(factory.sql_create(usertype="Student"))
