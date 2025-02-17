from models import SchoolTimetable, MusicTimetable, LessonRequest, MusicLesson, SchoolLesson
from datetime import datetime
from collections import deque

student_timetable = SchoolTimetable(weekrepeat=2, schooltimetableid=1)
student_timetable.lessons = {
    1: SchoolLesson(schoollessonid=1, name="Meth", start=datetime(2025, 1, 1, 1), end=datetime(2025, 1, 1, 2, 0), schoolteacherid=1, importance=2),
    2: SchoolLesson(schoollessonid=2, name="Chemistry", start=datetime(2025, 1, 1, 2), end=datetime(2025, 1, 1, 3, 0), schoolteacherid=2, importance=1),
    3: SchoolLesson(schoollessonid=3, name="Computing", start=datetime(2025, 1, 1, 3), end=datetime(2025, 1, 1, 4, 0), schoolteacherid=2, importance=12)
    # follow the same procedure to create more lessons
}

music_timetable = MusicTimetable(weekrepeat=2, musictimetableid=1)
music_timetable.lessons = {
    1: MusicLesson(name="vioin", start=datetime(2025, 1, 1, 1), end=datetime(2025, 1, 1, 2, 0), musiclessonid=1, musicteacherid=1)
}

lesson_requests = deque([LessonRequest(
    # dummy lesson requests, i.e. have to fit in 100 lessons
    requestid=1, studentid=1, musicteacherid=1)])

# gets all lessons in order of start date and start time
student_lessons = student_timetable.get_lessons()

teacher_lessons = music_timetable.get_lessons()

request = lesson_requests.popleft()

# write an algorithm which takes each request from lr queue, checks for lessons in timetables and find the optimal timeslot to add a lesson
# lst[i].start, lst[i].end to get start and end time in datetime.datetime format
# choose a 30 minute segment from the timetable start time, i mean it isn't mentioned above, but all existing music lessons will be written in, although name = None to indicate a free lesson
