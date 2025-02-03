from models import SchoolTimetable, MusicTimetable, LessonRequest, MusicLesson, SchoolLesson
from datetime import datetime

student_timetable = SchoolTimetable(weekrepeat=2, schooltimetableid=1)
student_timetable.lessons = {
    1: SchoolLesson(schoollessonid=1, name="Meth", start=datetime(2025, 1, 1, 1, 0), end=datetime(2025, 1, 1, 2, 0), schoolteacherid=1, importance=10)
}

print(student_timetable)
