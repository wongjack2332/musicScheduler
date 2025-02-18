from typing import Any, Optional
from datetime import datetime

from pymysql import connections

from database_utils import get_connection, run_sql, close_connection
from models import User, Student, MusicTeacher, SchoolTeacher
from models import Timetable, SchoolTimetable, MusicTimetable
from models import Lesson, SchoolLesson, MusicLesson
from models import LessonRequest


class UserFactory:
    type_to_obj = {
        "Student": Student,
        "MusicTeacher": MusicTeacher,
        "SchoolTeacher": SchoolTeacher
    }

    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.connection = connection

    def is_user(self, username):
        sql = "SELECT * FROM users WHERE email = '%s'" % (username)

        return len(run_sql(self.cursor, sql)) > 0

    def sql_from_username(self, username):
        sql = "SELECT userid FROM users WHERE email = '%s'" % (username)
        t = run_sql(self.cursor, sql)
        if len(t) != 1:
            raise LookupError("duplicate or missing email")

        return self.sql_get(t[0]['userid'])

    def sql_get(self, userid: int):

        self.userid = userid
        user = run_sql(
            self.cursor, f"SELECT * FROM users WHERE userid = {userid}")

        if len(user) != 1:
            raise LookupError("duplicate uid")

        user = user[0]
        print(user)
        user = dict(user, **self.get_user_type(user['usertype']))
        # different names for user types
        user['usertype'] = user['usertype'].title()
        user_type = user['usertype']
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

        create_user = "INSERT INTO users(usertype) VALUES ('%s')" % (usertype)
        print(create_user)
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
        return {f'{usertype.lower()}id': run_sql(self.cursor, f"SELECT LAST_INSERT_ID()")[0]['LAST_INSERT_ID()']}

    def sql_write(self, user: Student | MusicTeacher | SchoolTeacher):
        usertype = user.usertype
        sql_users = f"""UPDATE Users
        SET email = {repr(user.email) if user.email is not None else 'NULL'},
        firstname = {repr(user.firstname) if user.firstname is not None else 'NULL'},
        lastname = {repr(user.lastname) if user.lastname is not None else 'NULL'},
        usertype = {repr(user.usertype) if user.usertype is not None else 'NULL'},
        password = {repr(user.password)}
        WHERE userid = {user.userid}
        """
        print(sql_users)
        run_sql(self.cursor, sql_users)
        self.connection.commit()

        if usertype == 'Student':
            student: Student = user
            sql = f"""UPDATE {usertype}s
            SET year = {user.year or 'NULL'},
            schooltimetableid = {user.schooltimetableid or 'NULL'},
            musictimetableid = {user.musictimetableid or 'NULL'},
            userid = {user.userid}
            WHERE studentid = {student.studentid}
            """

        elif usertype == 'MusicTeacher':
            musicteacher: MusicTeacher = user
            sql = f"""UPDATE {usertype}s
            SET musictimetableid = {user.musictimetableid},
            userid = {user.userid}
            WHERE musicteacherid = {musicteacher.musicteacherid}
            """

        elif usertype == 'SchoolTeacher':
            schoolteacher: SchoolTeacher = user
            sql = f"""UPDATE {usertype}s
            SET schooltimetableid = {user.schooltimetableid},
            userid = {user.userid}
            WHERE schoolteacherid = {schoolteacher.schoolteacherid}
            """
        print(sql)
        run_sql(self.cursor, sql)
        self.connection.commit()


class LessonFactory:
    type_to_obj = {
        "SchoolLesson": SchoolLesson,
        "MusicLesson": MusicLesson
    }

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def sql_get(self, lessontype: str = "SchoolLesson", idx: int = 1):
        sql = f"SELECT * FROM {lessontype}s WHERE {lessontype.lower()}id = {idx}"
        dct = run_sql(self.cursor, sql)
        if len(dct) != 1:
            raise LookupError("duplicate or missing uid")
        dct = dct[0]
        del dct[f'{lessontype.lower().replace("lesson", "timetable")}id']
        return self.type_to_obj[lessontype](**dct)

    def sql_create(self, lessontype: str = "SchoolLesson"):

        if lessontype not in self.type_to_obj:
            raise TypeError("Invalid lesson type")

        sql = f"INSERT INTO {lessontype}s VALUES ()"

        run_sql(self.cursor, sql)
        result = run_sql(self.cursor, "SELECT LAST_INSERT_ID()")
        idx = result[0]['LAST_INSERT_ID()']
        lesson = self.type_to_obj[lessontype](
            **{f"{lessontype.lower()}id": idx})

        self.connection.commit()
        return lesson

    def sql_write(self, lesson_type: str, lesson: SchoolLesson | MusicLesson, timetableid: Optional[int] = None):
        if lesson_type not in self.type_to_obj:
            raise TypeError("Invalid lesson type")

        if lesson_type == 'SchoolLesson':
            sql = f"""UPDATE {lesson_type}s
            SET name = {repr(lesson.name) if lesson.name is not None else 'NULL'},
            start = '{lesson.start.strftime(' % Y-%m-%d % H: % M: % S')}',
            end = '{lesson.end.strftime(' % Y-%m-%d % H: % M: % S')}',
            schoolteacherid = {lesson.schoolteacherid or 'NULL'},
            importance = {lesson.importance or 'NULL'},
            schooltimetableid = {timetableid or 'NULL'}
            WHERE {lesson_type.lower()}id = {lesson.schoollessonid}"""
            print(sql)

        elif lesson_type == 'MusicLesson':
            sql = f"""UPDATE {lesson_type}s
            SET name = {repr(lesson.name) if lesson.name is not None else 'NULL'},
            start = '{lesson.start.strftime(' % Y-%m-%d % H: % M: % S')}',
            end = '{lesson.end.strftime(' % Y-%m-%d % H: % M: % S')}',
            musicteacherid = {lesson.musicteacherid or 'NULL'},
            musictimetableid = {timetableid or 'NULL'}
            WHERE {lesson_type.lower()}id = {lesson.musiclessonid}"""

        print(sql)

        run_sql(self.cursor, sql)
        print("written to sql database")

        self.connection.commit()


class TimetableFactory:

    type_to_obj = {
        "SchoolTimetable": SchoolTimetable,
        "MusicTimetable": MusicTimetable
    }

    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.connection = connection

    def sql_get(self, timetabletype: str, idx: int):
        if timetabletype not in self.type_to_obj:
            raise TypeError("Invalid timetable type")

        sql = f"SELECT * FROM {timetabletype}s WHERE {timetabletype.lower()}id = {
            idx}"
        dct = run_sql(self.cursor, sql)
        if len(dct) != 1:
            raise LookupError("duplicate or missing uid")
        timetable = self.type_to_obj[timetabletype](**dct[0])
        if timetabletype == "SchoolTimetable":
            lesson_name = "SchoolLesson"

        elif timetabletype == "MusicTimetable":
            lesson_name = "MusicLesson"

        sql = f"SELECT {timetabletype}id FROM {
            lesson_name}s WHERE {timetabletype}id = {idx}"
        dct = run_sql(self.cursor, sql)

        for lesson in dct:
            timetable.lessons[lesson[f"{timetabletype.lower()}id"]] = self.sql_get(
                lesson_name, lesson[f"{timetabletype.lower()}id"])

        return timetable

    def sql_create(self, timetabletype: str = "SchoolTimetable"):
        if timetabletype not in self.type_to_obj:
            raise TypeError("Invalid timetable type")

        sql = f"INSERT INTO {timetabletype}s VALUES ()"

        run_sql(self.cursor, sql)
        result = run_sql(self.cursor, "SELECT LAST_INSERT_ID()")
        idx = result[0]['LAST_INSERT_ID()']

        timetable = self.type_to_obj[timetabletype](
            **{f"{timetabletype.lower()}id": idx})

        self.connection.commit()
        return timetable

    def sql_write(self, timetable: Timetable, timetabletype: str = "SchoolTimetable"):
        if timetabletype not in self.type_to_obj:
            raise TypeError("Invalid timetable type")

        sql = f"""UPDATE {timetabletype}s
        SET weekrepeat = {timetable.weekrepeat or 'NULL'}
        WHERE {timetabletype.lower()}id = {timetable.__getattribute__(f"{timetabletype.lower()}id")}"""

        run_sql(self.cursor, sql)

        for lesson in timetable.get_lessons():
            LessonFactory(self.connection).sql_write(lesson_type=timetabletype.replace(
                "Timetable", "Lesson"), lesson=lesson, timetableid=timetable.__getattribute__(f"{timetabletype.lower()}id"))

        self.connection.commit()


class LessonRequestFactory:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def sql_create(self):
        sql = "INSERT INTO lessonreqs VALUES ()"
        run_sql(self.cursor, sql)
        result = run_sql(self.cursor, "SELECT LAST_INSERT_ID()")
        request = LessonRequest(requestid=result[0]['LAST_INSERT_ID()'])
        self.connection.commit()
        return request

    def sql_get(self, idx: int):
        sql = f"SELECT * FROM lessonreqs WHERE requestid = {idx}"

        res = run_sql(self.cursor, sql)
        if len(res) != 1:
            raise LookupError("duplicate or missing uid")
        return LessonRequest(**res[0])

    def sql_write(self, request: LessonRequest):
        sql = f"UPDATE lessonreqs SET studentid = {request.studentid}, musicteacherid = {request.musicteacherid}, name = {repr(request.name) if request.name is not None else 'NULL'} WHERE requestid = {request.requestid}"
        run_sql(self.cursor, sql)
        self.connection.commit()


if __name__ == "__main__":
    connection = get_connection()
    ufac = UserFactory(connection)
    print(ufac.sql_create(usertype='Student'))

    close_connection(connection)
