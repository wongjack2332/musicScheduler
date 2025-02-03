from src.models import SchoolTimetable, MusicTimetable, MusicLesson, SchoolLesson, LessonRequest, Notification
import pytest
from datetime import datetime


@pytest.mark.parametrize("timetable_id", [1, 2, 3, 4])
def test_school_timetable(timetable_id):
    school_timetable = SchoolTimetable(schooltimetableid=timetable_id)
    assert school_timetable.schooltimetableid == timetable_id
    assert school_timetable.lessons == dict()


@pytest.mark.parametrize("timetable_id", [1, 2, 3, 4])
def test_music_timetable(timetable_id):
    music_timetable = MusicTimetable(musictimetableid=timetable_id)
    assert music_timetable.musictimetableid == timetable_id
    assert music_timetable.lessons == dict()


@pytest.mark.parametrize("kwargs", [
    {"title": "violin", "start": datetime(
        2025, 1, 1, 12, 30), "end": datetime(2025, 12, 31, 23, 59), "musiclessonid": 1, 'musicteacherid': 1, 'weekrepeat': 2},
    {"title": "violin", "start": datetime(
        2025, 8, 19, 2, 16), "end": datetime(2025, 8, 31, 23, 59), "musiclessonid": 2, 'musicteacherid': 2, 'weekrepeat': 2},
])
def test_music_lesson(kwargs):
    music_lesson = MusicLesson(**kwargs)
    assert music_lesson.musiclessonid == kwargs["musiclessonid"]
    assert music_lesson.musicteacherid == kwargs["musicteacherid"]
    assert music_lesson.musicteacher is None


@pytest.mark.parametrize("kwargs", [
    {"title": "math", "start": datetime(2025, 1, 1, 12, 30), "end": datetime(
        2025, 12, 31, 23, 59), "schoollessonid": 1, 'schoolteacherid': 1, 'weekrepeat': 2},
    {"title": "science", "start": datetime(2025, 8, 19, 2, 16), "end": datetime(
        2025, 8, 31, 23, 59), "schoollessonid": 2, 'schoolteacherid': 2, 'weekrepeat': 2},
])
def test_school_lesson(kwargs):
    school_lesson = SchoolLesson(**kwargs)
    assert school_lesson.schoollessonid == kwargs["schoollessonid"]
    assert school_lesson.schoolteacherid == kwargs["schoolteacherid"]
    assert school_lesson.schoolteacher is None


@pytest.mark.parametrize("kwargs", [
    {"requestid": 1, "studentid": 1, "musicteacherid": 1, "name": "Lesson Request 1"},
    {"requestid": 2, "studentid": 2, "musicteacherid": 2, "name": "Lesson Request 2"},
])
def test_lesson_request(kwargs):
    lesson_request = LessonRequest(**kwargs)
    assert lesson_request.requestid == kwargs["requestid"]
    assert lesson_request.studentid == kwargs["studentid"]
    assert lesson_request.musicteacherid == kwargs["musicteacherid"]
    assert lesson_request.name == kwargs["name"]


@pytest.mark.parametrize("kwargs", [
    {"notificationid": 1, "userid": 1, "title": "Notification 1",
        "message": "This is a notification", "notificationtime": datetime(2025, 1, 1, 12, 30)},
    {"notificationid": 2, "userid": 2, "title": "Notification 2",
        "message": "This is another notification", "notificationtime": datetime(2025, 12, 31, 23, 59)},
    {"notificationid": 3, "userid": 3, "message": "This is a notification with default title",
        "notificationtime": datetime(2025, 8, 19, 2, 16)},
])
def test_notification(kwargs):
    if "title" not in kwargs:
        kwargs["title"] = "Untitled"
    notification = Notification(**kwargs)
    assert notification.notificationid == kwargs["notificationid"]
    assert notification.userid == kwargs["userid"]
    assert notification.title == kwargs.get("title", "Untitled")
    assert notification.message == kwargs["message"]
    assert notification.notificationtime == kwargs["notificationtime"]
