from models import SchoolTimetable, MusicTimetable, LessonRequest, MusicLesson, SchoolLesson
from datetime import datetime
from collections import deque

student_timetable = SchoolTimetable(weekrepeat=2, schooltimetableid=1)
student_timetable.lessons = {
    1: SchoolLesson(schoollessonid=1, name="Meth", start=datetime(2025, 1, 1, 1), end=datetime(2025, 1, 1, 2, 0), schoolteacherid=1, importance=10)
    # follow the same procedure to create more lessons
}

music_timetable = MusicTimetable(weekrepeat=2, musictimetableid=1)
music_timetable.lessons = {
    1: MusicLesson(name="vioin", start=datetime(2025, 1, 1, 1), end=datetime(2025, 1, 1, 2, 0), musiclessonid=1, musicteacherid=1)
}

lesson_requests = deque([LessonRequest(
    # dummy lesson requests, i.e. have to fit in 100 lessons
    requestid=i, studentid=1, musicteacherid=1) for i in range(1, 101)])

# gets all lessons in order of start date and start time
print(student_timetable.get_lessons())

print(music_timetable.get_lessons())

print(lesson_requests.pop())
