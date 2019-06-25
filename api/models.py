from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import os


weekDays = (
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday")
)


def year_choices():
    return [(r, r) for r in range(2015, datetime.date.today().year+1)]


class Role(models.Model):
    STUDENT = 1
    PROFESSOR = 2
    STAFF = 3
    ADMIN = 4
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (PROFESSOR, 'professor'),
        (STAFF, 'staff'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.ROLE_CHOICES.__getitem__(self.id-1)[1].__str__()


class Field(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    code = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s, %d" % (self.name, self.code)


class User(AbstractUser):
    roles = models.ManyToManyField(Role)
    firstName = models.CharField(max_length=300)
    lastName = models.CharField(max_length=300)
    ssn = models.CharField(max_length=10)  # in iran max length of melli code without - is 10 digits
    email = models.EmailField()
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s, %s" % (self.firstName, self.lastName)


class College(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    college_name = models.CharField(max_length=300)

    def __str__(self):
        return self.college_name


class Department(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    dep_name = models.CharField(max_length=300)
    college = models.ForeignKey(College, on_delete=models.CASCADE)  # Each college has some departments

    def __str__(self):
        return self.dep_name


class Course(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    code = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=300)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Building(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Section(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prof')
    student = models.ManyToManyField(User, related_name='stu')
    semester = models.CharField(max_length=6, choices=(('first', 'First'), ('second', 'Second')))
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    classNumber = models.IntegerField()  # must be integer because number may be negative e.g -1
    year = models.IntegerField(choices=year_choices())
    day1InWeek = models.CharField(max_length=20, choices=weekDays, blank=False, null=False)
    day2InWeek = models.CharField(max_length=20, choices=weekDays)
    startTime = models.CharField(max_length=20)
    endTime   = models.CharField(max_length=20)

    def __str__(self):
        return self.course.name


def upload_document_to(instance, name):
    col_name = instance.section.course.department.college.college_name
    dep_name = instance.section.course.department.dep_name
    course_name = instance.section.course.name
    section_id = instance.section.id
    #year = instance.section.year
    return "media/colleges/%s/departments/%s/courses/%s/sections/%d/documents/%s" % (col_name, dep_name, course_name, section_id, name)


class Document(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=300)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_document_to)

    def __str__(self):
        return self.title


def upload_video_to(instance, name):
    col_name = instance.section.course.department.college.college_name
    dep_name = instance.section.course.department.dep_name
    course_name = instance.section.course.name
    section_id = instance.section.id
    #year = instance.section.year
    return "media/colleges/%s/departments/%s/courses/%s/sections/%d/videos/%s" % (col_name, dep_name, course_name, section_id, name)


class Video(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=300)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_video_to)
    # /media/departmentName/courses/courseName/sections/sectionId/videos


class Message(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()

    def __str__(self):
        return "%s: %s..."%(self.title, self.content[:20])


def id_generator(instance,college_name ,department_name, course_name, section_id):
    directory = "media/colleges/%s/departments/%s/courses/%s/sections/%d/homeworks/" % (college_name, department_name, course_name, section_id)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if instance.id is None:
        files_list = os.listdir(directory)
        if len(files_list) != 0:
            max_id = int(max(files_list))
            return max_id+1
        else:
            return 1
    return instance.id



def upload_homework_question_to(instance, name):
    col_name = instance.section.course.department.college.college_name
    dn = instance.section.course.department.dep_name
    course_name = instance.section.course.name
    section_id = instance.section.id
    # year = instance.section.year
    homework_id = id_generator(instance,col_name,dn, course_name, section_id)
    return "media/colleges/%s/departments/%s/courses/%s/sections/%d/homeworks/%d/questions/%s/" % (col_name, dn, course_name, section_id, homework_id, name)
    # return "media/question/%s"%name


def upload_homework_solution_to(instance, name):
    col_name = instance.section.course.department.college.college_name
    dn = instance.section.course.department.dep_name
    course_name = instance.section.course.name
    section_id = instance.section.id
    # year = instance.section.year
    homework_id = id_generator(instance, col_name, dn, course_name, section_id)
    return "media/colleges/%s/departments/%s/courses/%s/sections/%d/homeworks/%d/final solution/%s" % (col_name, dn, course_name, section_id, homework_id, name)


def upload_homework_grades_to(instance, name):
    col_name = instance.section.course.department.college.college_name
    dn = instance.section.course.department.dep_name
    course_name = instance.section.course.name
    section_id = instance.section.id
    # year = instance.section.year
    homework_id = id_generator(instance, col_name, dn, course_name, section_id)
    return "media/colleges/%s/departments/%s/courses/%s/sections/%d/homeworks/%d/grades/%s" % (col_name, dn, course_name, section_id, homework_id, name)


class Homework(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question_file = models.FileField(upload_to=upload_homework_question_to)  # questions file
    solution_file = models.FileField(upload_to=upload_homework_solution_to, blank=True, null=True)  # solutions file
    grades_file = models.FileField(upload_to=upload_homework_grades_to, blank=True, null=True)  # grades file
    # /media/departmentNameself/courses/courseName/sections/sectionId/homeworks

    def __str__(self):
        return self.title


def upload_solution_to(instance, name):
    col_name = instance.section.course.department.college.college_name
    dn = instance.homework.section.course.department.dep_name
    course_name = instance.homework.section.course.name
    section_id = instance.homework.section.id
    # year = instance.homework.section.year
    homework_id = instance.homework.id
    return "media/colleges/%s/departments/%s/courses/%s/sections/%d/homeworks/%d/solutions/%s" % (col_name, dn, course_name, section_id, homework_id, name)


class Solution(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_solution_to)
    deliverTime = models.DateTimeField(auto_now_add=True)
    # /media/students/studentId/courses

    def __str__(self):
        return "delivered at: " + self.deliverTime.__str__()

