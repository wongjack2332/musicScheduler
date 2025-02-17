from dataclasses import dataclass, field
from datetime import datetime
from types import FunctionType
from typing import Generator, Optional


@dataclass(kw_only=True)
class User:
    userid: int
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    usertype: Optional[str] = None


@dataclass(kw_only=True)
class MusicTeacher(User):
    musicteacherid: int
    musictimetableid: Optional[int] = None
    musictimetable: Optional['MusicTimetable'] = None


@dataclass(kw_only=True)
class SchoolTeacher(User):
    schoolteacherid: int
    schooltimetableid: Optional[int] = None
    schooltimetable: Optional['SchoolTimetable'] = None


@dataclass(kw_only=True)
class Student(User):
    studentid: int
    year: Optional[int] = None
    schooltimetableid: Optional[int] = None
    schooltimetable: Optional['SchoolTimetable'] = None
    musictimetableid: Optional[int] = None
    musictimetable: Optional['MusicTimetable'] = None


@dataclass(kw_only=True)
class Lesson:
    name: Optional[str] = None
    start: datetime = datetime(1, 1, 1)
    end: datetime = datetime(1, 1, 1)


@dataclass(kw_only=True)
class MusicLesson(Lesson):
    musiclessonid: int
    musicteacherid: Optional[int] = None


@dataclass(kw_only=True)
class SchoolLesson(Lesson):
    schoollessonid: int
    schoolteacherid: Optional[int] = None
    schoolteacher: Optional['SchoolTeacher'] = None
    importance: Optional[int] = None


@dataclass(kw_only=True)
class Timetable:
    weekrepeat: Optional[int] = None
    lessons: Optional[dict[int, Lesson]] = field(default_factory=dict)

    def get_lessons(self):
        if not self.lessons:
            return None

        lst = sorted(self.lessons.values(), key=lambda x: x.start)
        for i in lst:
            yield i


@dataclass(kw_only=True)
class MusicTimetable(Timetable):
    musictimetableid: int


@dataclass(kw_only=True)
class SchoolTimetable(Timetable):
    schooltimetableid: int


@dataclass(kw_only=True)
class LessonRequest:
    requestid: int
    studentid: Optional[int] = None
    musicteacherid: Optional[int] = None
    name: Optional[str] = None


@dataclass(kw_only=True)
class Notification:
    notificationid: int
    userid: Optional[int] = None
    title: Optional[str] = None
    message: Optional[str] = None
    notificationtime: Optional[datetime] = None
