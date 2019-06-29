from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins as rest_mixins, generics, viewsets
# from . import mixins
from rest_framework.generics import ListAPIView
import magic
from django.core import serializers

from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import CourseSerializer, CollegeSerializer, DepartmentSerializer, SectionSerializer, \
    SolutionSerializer, HomeworkSerializer, DocumentSerializer, VideoSerializer, MessageSerializer
from .models import Course, College, Department, Section, Solution, Document, Video, Homework, Message


import os
import json
from django.http import HttpResponse, Http404

def is_json(data):
    try:
        json_data = json.loads(data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
#
# @method_decorator(csrf_exempt)
# def download(request):
#     # if is_json(request.body):
#     file_path = "%s/departments/%s/courses/%s/sections/%d/docs/%"
#     try:
#         strs = str(file_path).split("/")
#         file_name = strs[len(strs)-1]
#         mim = magic.Magic(mime=True)
#         file_type = mim.from_file(file_path)
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type=file_type)
#                 response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
#                 return response
#         else:
#             return HttpResponse("does not exists!")
#     except Exception as e:
#         return HttpResponse(str(e))


@method_decorator(csrf_exempt)
def download(request, encoded_url):
    # if is_json(request.body):id
    file_path = encoded_url
    try:
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


class CollegeAPIView(rest_mixins.CreateModelMixin,
                     ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = CollegeSerializer
    queryset         = College.objects.all()

    def list(self, *args, **kwargs):
        queryset = College.objects.all()
        serializer = CollegeSerializer(queryset, many=True)
        return JsonResponse({'colleges':serializer.data})


class CollegeDetailAPIView(rest_mixins.DestroyModelMixin,
                           rest_mixins.UpdateModelMixin,
                           rest_mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = CollegeSerializer
    queryset         = College.objects.all()
    lookup_field     = 'college_name'

    def get_object(self):
        q = College.objects.filter(college_name=self.kwargs['college_name']).distinct()
        return q

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        college = get_object_or_404(queryset)
        serializer = CollegeSerializer(college)
        return JsonResponse({'colleges': serializer.data})

################################################### Department


class DepartmentAPIView(rest_mixins.CreateModelMixin,
                        ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DepartmentSerializer
    queryset         = Department.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']).first().department_set.all()

    def list(self,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = DepartmentSerializer(queryset, many=True)
        return JsonResponse({'departments':serializer.data})


class DepartmentDetailAPIView(rest_mixins.DestroyModelMixin,
                              rest_mixins.UpdateModelMixin,
                              rest_mixins.CreateModelMixin,
                              generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = DepartmentSerializer
    queryset         = Department.objects.all()
    lookup_field     = 'dep_name'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']).first().department_set.filter(dep_name=self.kwargs['dep_name']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        dep = get_object_or_404(queryset)
        serializer = DepartmentSerializer(dep)
        return JsonResponse({'departments': serializer.data})


################################################### Course


class CourseAPIView(rest_mixins.CreateModelMixin,
                    ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = CourseSerializer
    queryset         = Course.objects.all()
    #

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all()

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True)
        return JsonResponse({'courses': serializer.data})


class CourseDetailAPIView(rest_mixins.DestroyModelMixin,
                          rest_mixins.UpdateModelMixin,
                          rest_mixins.CreateModelMixin,
                          generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = CourseSerializer
    queryset         = Course.objects.all()
    lookup_field     = 'course_name'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(name=self.kwargs['course_name']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        course = get_object_or_404(queryset)
        serializer = CourseSerializer(course)
        return JsonResponse({'courses': serializer.data})


    #
################################################### Section


class SectionAPIView(rest_mixins.CreateModelMixin,
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

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SectionSerializer(queryset, many=True)
        return JsonResponse({'sections': serializer.data})


class SectionDetailAPIView(rest_mixins.DestroyModelMixin,
                           rest_mixins.UpdateModelMixin,
                           rest_mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = SectionSerializer
    queryset         = Section.objects.all()
    lookup_field     = 'id'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.filter(id=self.kwargs['id']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        section = get_object_or_404(queryset)
        serializer = SectionSerializer(section)
        return JsonResponse({'sections': serializer.data})




################################################### Department


class DocumentAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().document_set.all()

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DocumentSerializer(queryset, many=True)
        return JsonResponse({'documents': serializer.data})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DocumentDetailAPIView(rest_mixins.DestroyModelMixin,
                            rest_mixins.UpdateModelMixin,
                            rest_mixins.CreateModelMixin,
                            generics.RetrieveAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().document_set.filter(id=self.kwargs['i']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        doc = get_object_or_404(queryset)
        serializer = DocumentSerializer(doc)
        return JsonResponse({'documents': serializer.data})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)





################################################### Message


class MessageAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().message_set.all()

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)
        return JsonResponse({'messages': serializer.data})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessageDetailAPIView(rest_mixins.DestroyModelMixin,
                           rest_mixins.UpdateModelMixin,
                           rest_mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.filter(id=self.kwargs['id']).first().message_set.filter(
            id=self.kwargs['i']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        msg = get_object_or_404(queryset)
        serializer = MessageSerializer(msg)
        return JsonResponse({'messages': serializer.data})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


################################################### Video

class VideoAPIView(rest_mixins.CreateModelMixin, ListAPIView):
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

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = VideoSerializer(queryset, many=True)
        return JsonResponse({'videos': serializer.data})


class VideoDetailView(rest_mixins.DestroyModelMixin,
                      rest_mixins.UpdateModelMixin,
                      rest_mixins.CreateModelMixin,
                      generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().video_set.filter(id=self.kwargs['i']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        vid = get_object_or_404(queryset)
        serializer = VideoSerializer(vid)
        return JsonResponse({'videos': serializer.data})


################################################### Homework


class HomeworkAPIView(rest_mixins.CreateModelMixin, ListAPIView):
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

    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = HomeworkSerializer(queryset, many=True)
        return JsonResponse({'homeworks': serializer.data})



class HomeworkDetailView(rest_mixins.DestroyModelMixin,
                         rest_mixins.UpdateModelMixin,
                         rest_mixins.CreateModelMixin,
                         generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().homework_set.filter(
            id=self.kwargs['i']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        vid = get_object_or_404(queryset)
        serializer = HomeworkSerializer(vid)
        return JsonResponse({'homeworks': serializer.data})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


################################################### Solution


class SolutionAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().homework_set.filter(id=self.kwargs['i']).first().solution_set.all()


    def list(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SolutionSerializer(queryset, many=True)
        return JsonResponse({'solutions': serializer.data})


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SolutionDetailView(rest_mixins.DestroyModelMixin,
                         rest_mixins.UpdateModelMixin,
                         rest_mixins.CreateModelMixin,
                         generics.RetrieveAPIView):
    # permission_classes   = []
    # authentication_classes = []
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()
    lookup_field = 'si'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first()\
        .section_set.filter(id=self.kwargs['id']).first()\
        .homework_set.filter(id=self.kwargs['i']).first().solution_set.filter(id=self.kwargs['si']).distinct()

    def retrieve(self, *args, **kwargs):
        queryset = self.get_object()
        vid = get_object_or_404(queryset)
        serializer = SolutionSerializer(vid)
        return JsonResponse({'solutions': serializer.data})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

