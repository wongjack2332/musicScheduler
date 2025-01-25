from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class User:
    userid: int
    email: str
    firstname: str
    lastname: str
    user_type: Optional[str] = field(default=None)

    def check_usertype(self):
        if self.user_type not in [None, "Student", "MusicTeacher", "SchoolTeacher"]:
            raise ValueError("Invalid user type")


@dataclass(kw_only=True)
class MusicTeacher(User):
    musicteacherid: int
    musictimetableid: int
    musictimetable: Optional['MusicTimetable'] = None

    def __post_init__(self):
        super().check_usertype()
        self.user_type = "MusicTeacher"


@dataclass(kw_only=True)
class SchoolTeacher(User):
    schoolteacherid: int
    schooltimetableid: int
    schooltimetable: Optional['SchoolTimetable'] = None

    def __post_init__(self):
        super().check_usertype()
        self.user_type = "SchoolTeacher"


@dataclass(kw_only=True)
class Student(User):
    studentid: int
    year: int
    schooltimetableid: int
    schooltimetable: Optional['SchoolTimetable'] = None
    schoolteachers: dict[int, Optional[SchoolTeacher]
                         ] = field(default_factory=dict)
    musictimetableid: int
    musictimetable: Optional['MusicTimetable'] = None

    def __post_init__(self):
        super().check_usertype()
        self.user_type = "Student"
        if self.year < 7 or self.year > 13:
            raise ValueError("Invalid school year")


@dataclass
class Timetable:
    weekrepeat: int
    lessons: dict[int, Optional['MusicLesson'] |
                  Optional['SchoolLesson']] = field(default_factory=dict)


@dataclass
class SchoolTimetable:
    schooltimetableid: int
    lessons: dict[int, Optional['SchoolLesson']] = field(default_factory=dict)


@dataclass
class MusicTimetable:
    musictimetableid: int
    lessons: dict[int, Optional['MusicLesson']] = field(default_factory=dict)


@dataclass
class Lesson:
    title: str
    start: datetime
    end: datetime


@dataclass
class MusicLesson(Lesson):
    musiclessonid: int
    musicteacherid: int
    musicteacher: Optional[MusicTeacher] = None
    weekrepeat: int = 2


@dataclass
class SchoolLesson(Lesson):
    schoollessonid: int
    schoolteacherid: int
    schoolteacher: Optional[SchoolTeacher] = None
    weekrepeat: int = 2


@dataclass(kw_only=True)
class LessonRequest:
    requestid: int
    studentid: int
    student: Optional[Student] = None
    musicteacherid: int
    musicteacher: Optional[MusicTeacher] = None
    name: str


@dataclass(kw_only=True)
class Notification:
    notificationid: int
    userid: int
    title: str = "Untitled"
    message: str
    notificationtime: datetime
