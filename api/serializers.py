from abc import ABC

from rest_framework import serializers

from .models import Course, College, Department, Section, Solution, Homework, Document, Message, Video, User


# class CollegeListSerializer(serializers.ListSerializer, ABC):
#     class Meta:
#         model = College
#         fields = [
#             'id',
#             'college_name'
#         ]
#
#     def to_representation(self, user):
#         data = super().to_representation(user)  # the original data
#         print(data)
#         dic = {}
#         for k in range(len(data)):
#             dic['colleges'] = [{data.__getitem__(k)['id']: data.__getitem__(k) for i, j in data}]
#         return dic
#


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        # list_serializer_class = CollegeListSerializer
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

class StudentSerializer(serializers.ModelSerializer):
    field_name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_field_name(obj):
        # obj is model instance
        return obj.field.name

    class Meta:
        model = User
        fields = [
            'id',
            'firstName',
            'lastName',
            'email',
            'field_name'
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

    class Meta:
        model = Homework
        fields=[
            'id',
            'title',
            'section',
            'question_file',
            'grades_file',
            'solution_file',
        ]


class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = [
            'id',
            'student',
            'homework',
            'file',
            'deliverTime',
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

    class Meta:
        model = Message
        fields=[
            'id',
            'title',
            'section',
            'sender_name',
            'content'
        ]


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields=[
            'id',
            'title',
            'section',
            'file',
        ]

