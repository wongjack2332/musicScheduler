import pytest
from src.models import Student, MusicTeacher, SchoolTeacher


@pytest.mark.parametrize(
    "userid, email, firstname, lastname, year, studentid, schooltimetableid, musictimetableid",
    [(1, "email@email.com", "jack", "wong", 8, 1, 1, 1),
     ('2', "email@email.com", "jack", "wong", 8, 1, 1, 1),
     (4, "email@email.com", "jack", "wong", 2, 1, 1, 1),
     (5, "email@email.com", "jack", "wong", 17, 1, 1, 1),
     (6, "email@email.com", "jack", "wong", 7, "2", 1, 1)
     ]
)
def test_student(userid, email, firstname, lastname, year, studentid, schooltimetableid, musictimetableid):
    if year < 7 or year > 13:
        with pytest.raises(ValueError):
            student = Student(userid=userid, email=email, firstname=firstname, lastname=lastname, year=year,
                              studentid=studentid, schooltimetableid=schooltimetableid, musictimetableid=musictimetableid)
        return
    student = Student(userid=userid, email=email, firstname=firstname, lastname=lastname, year=year,
                      studentid=studentid, schooltimetableid=schooltimetableid, musictimetableid=musictimetableid)

    assert student.email == email
    assert student.user_type == "Student"
    assert student.year == year
    assert student.studentid == studentid
    assert student.schooltimetableid == schooltimetableid
    assert student.musictimetableid == musictimetableid


@pytest.mark.parametrize(
    "userid, email, firstname, lastname, musicteacherid, musictimetableid",
    [(1, "email@email.com", "john", "doe", 1, 1),
     ('2', "email@email.com", "john", "doe", 1, 1),
     ]
)
def test_music_teacher(userid, email, firstname, lastname, musicteacherid, musictimetableid):
    music_teacher = MusicTeacher(userid=userid, email=email, firstname=firstname, lastname=lastname,
                                 musicteacherid=musicteacherid, musictimetableid=musictimetableid)

    assert music_teacher.email == email
    assert music_teacher.user_type == "MusicTeacher"
    assert music_teacher.musicteacherid == musicteacherid
    assert music_teacher.musictimetableid == musictimetableid


@pytest.mark.parametrize(
    "userid, email, firstname, lastname, schoolteacherid, schooltimetableid",
    [(1, "email@email.com", "john", "doe", 1, 1),
     (2, "email@email.com", "john", "doe", 2, 2),
     ]
)
def test_school_teacher(userid, email, firstname, lastname, schoolteacherid, schooltimetableid):
    school_teacher = SchoolTeacher(userid=userid, email=email, firstname=firstname, lastname=lastname,
                                   schoolteacherid=schoolteacherid, schooltimetableid=schooltimetableid)

    assert school_teacher.email == email
    assert school_teacher.user_type == "SchoolTeacher"
    assert school_teacher.schoolteacherid == schoolteacherid
    assert school_teacher.schooltimetableid == schooltimetableid
