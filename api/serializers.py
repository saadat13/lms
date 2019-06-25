from rest_framework import serializers

from .models import Course, College, Department, Section, Solution, Homework, Document, Message, Video


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            'id',
            'college_name'
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'dep_name'
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields=[
            'id',
            'code',
            'name',
            'department',
        ]


class SectionSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField(read_only=True)
    professor_name = serializers.SerializerMethodField(read_only=True)
    building_name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_course_name(obj):
        # obj is model instance
        return obj.course.name

    @staticmethod
    def get_professor_name(obj):
        # obj is model instance
        return obj.professor.firstName + " " + obj.professor.lastName

    @staticmethod
    def get_building_name(obj):
        # obj is model instance
        return obj.building.name

    class Meta:
        model = Section
        fields=[
            'id',
            'course_name',
            'name',
            'professor_name',
            'semester',
            'building_name',
            'classNumber',
            'year',
            'day1InWeek',
            'day2InWeek',
            'startTime',
            'endTime',
        ]


class HomeworkSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_section_id(self):
        return self.section_id

    class Meta:
        model = Homework
        fields=[
            'id',
            'title',
            'section_id',
            'question_file',
            'grades_file',
            'solution_file',
        ]


class SolutionSerializer(serializers.ModelSerializer):

    deliver_time = serializers.SerializerMethodField(read_only=True)
    homework_id = serializers.SerializerMethodField(read_only=True)
    student_id  = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_deliver_time(self):
        return self.deliverTime

    @staticmethod
    def get_student_id(self):
        return self.student.id

    @staticmethod
    def get_homework_id(self):
        return self.homework.id


    class Meta:
        model = Solution
        fields = [
            'id',
            'student_id',
            'homework_id',
            'file',
            'deliver_time',
        ]


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields=[
            'id',
            'title',
            'section',
            'file',
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField(read_only=True)
    section_id = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_section_id(self):
        return self.section_id

    @staticmethod
    def get_sender_name(self):
        sender = self.sender
        if sender is not None:
            name = "%s %s"%(sender.firstName, sender.lastName)
            return name
        return "undefined"

    class Meta:
        model = Message
        fields=[
            'id',
            'title',
            'sender_name',
            'section_id',
            'content'
        ]


class VideoSerializer(serializers.ModelSerializer):
    section_id = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_section_id(self):
        return self.section_id

    class Meta:
        model = Video
        fields=[
            'id',
            'title',
            'section_id',
            'file',
        ]

