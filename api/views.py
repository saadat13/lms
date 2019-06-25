from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gunicorn.http.wsgi import FileWrapper
from rest_framework import mixins, generics
from rest_framework.generics import ListAPIView
import magic

from .serializers import CourseSerializer, CollegeSerializer, DepartmentSerializer, SectionSerializer, \
    SolutionSerializer, HomeworkSerializer, DocumentSerializer, VideoSerializer, MessageSerializer
from .models import Course, College, Department, Section, Solution, Document, Video, Homework, Message


import os
from django.conf import settings
import json
from django.http import HttpResponse, Http404

def is_json(data):
    try:
        json_data = json.loads(data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


@method_decorator(csrf_exempt)
def download(request):
    # # if is_json(request.body):
    req_dict = json.loads(request.body)
    try:
        file_path = req_dict['path']
        strs = str(file_path).split("/")
        file_name = strs[len(strs)-1]
        mim = magic.Magic(mime=True)
        file_type = mim.from_file(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=file_type)
                response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
                return response
        else:
            return HttpResponse("does not exists!")
    except Exception as e:
        return HttpResponse(str(e))



################################################### College


class CollegeAPIView(mixins.CreateModelMixin,
                     ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = CollegeSerializer
    queryset         = College.objects.all()


class CollegeDetailAPIView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = CollegeSerializer
    queryset         = College.objects.all()
    lookup_field     = 'college_name'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name=self.kwargs['college_name']).distinct())


################################################### Department


class DepartmentAPIView(mixins.CreateModelMixin,
                        ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DepartmentSerializer
    queryset         = Department.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']).first().department_set.all()


class DepartmentDetailAPIView(mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.CreateModelMixin,
                              generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = DepartmentSerializer
    queryset         = Department.objects.all()
    lookup_field     = 'dep_name'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']).first().department_set.filter(dep_name=self.kwargs['dep_name']).distinct())

################################################### Course


class CourseAPIView(mixins.CreateModelMixin,
                    ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = CourseSerializer
    queryset         = Course.objects.all()
    #

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all()


class CourseDetailAPIView(mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.CreateModelMixin,
                          generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = CourseSerializer
    queryset         = Course.objects.all()
    lookup_field     = 'course_name'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(name=self.kwargs['course_name']).distinct())
    #
################################################### Section


class SectionAPIView(mixins.CreateModelMixin,
                     ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = SectionSerializer
    queryset         = Section.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.all()


class SectionDetailAPIView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = SectionSerializer
    queryset         = Section.objects.all()
    lookup_field     = 'id'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.filter(id=self.kwargs['id']).distinct())




################################################### Department


class DocumentAPIView(mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().document_set.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DocumentDetailAPIView(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            generics.RetrieveAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first()
                                 .section_set.filter(id=self.kwargs['id']).first().document_set.filter(id=self.kwargs['i']).distinct())

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)





################################################### Message



class MessageAPIView(mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().message_set.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




class MessageDetailAPIView(mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.filter(id=self.kwargs['id']).first().message_set.filter(
            id=self.kwargs['i']).first())


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


################################################### Video

class VideoAPIView(mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().video_set.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class VideoDetailView(mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first()
                                 .section_set.filter(id=self.kwargs['id']).first().video_set.filter(
            id=self.kwargs['i']).distinct())



################################################### Homework



class HomeworkAPIView(mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().homework_set.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class HomeworkDetailView(mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.CreateModelMixin,
                         generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first()
                                 .section_set.filter(id=self.kwargs['id']).first().homework_set.filter(
            id=self.kwargs['i']).distinct())

################################################### Solution



class SolutionAPIView(mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().homework_set.filter(id=self.kwargs['i']).first().solution_set.all()


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class SolutionDetailView(mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.CreateModelMixin,
                         generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()
    lookup_field = 'si'

    def get_object(self):
        return get_object_or_404(College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                                 .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first()
                                 .section_set.filter(id=self.kwargs['id']).first()
                                 .homework_set.filter(id=self.kwargs['i']).first().solution_set.filter(id=self.kwargs['si']))

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

