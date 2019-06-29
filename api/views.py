import jwt
from django.contrib.auth import authenticate, user_logged_in
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins as rest_mixins, generics, viewsets, permissions, status
# from . import mixins
from rest_framework.generics import ListAPIView
import magic
from django.core import serializers

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework_jwt.views import jwt_response_payload_handler

# from api.permission import group_user
from api.authen import CustomAuthentication
from .serializers import CourseSerializer, CollegeSerializer, DepartmentSerializer, SectionSerializer, \
    SolutionSerializer, HomeworkSerializer, DocumentSerializer, VideoSerializer, MessageSerializer, StudentSerializer
from .models import Course, College, Department, Section, Solution, Document, Video, Homework, Message, User

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


@method_decorator(csrf_exempt)
def download(request, encoded_url):
    # if is_json(request.body):id
    file_path = encoded_url
    try:
        strs = str(file_path).split("/")
        file_name = strs[len(strs) - 1]
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


@csrf_exempt
def login(request, *args, **kwargs):
    try:
        json_data = json.loads(request.body)
        username = json_data['id']
        password = json_data['password']
        user = User.objects.filter(id=username, password=password).first()
        if user:
            try:
                # user = authenticate(username = username, password = password)
                secret_key = "strange secret key"
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
                id = user.id
                role = user.get_role
                first_name = user.firstName
                last_name = user.lastName
                email = user.email
                user_details = {"id": id, "role": role, "first_name": first_name, "last_name": last_name,
                                "email": email,
                                'token': token}
                setattr(user, 'token', token)
                user.save()
                return JsonResponse(user_details, status=200)
            except Exception as e:
                raise e
        else:
            return JsonResponse({'error': 'Some error'}, status=401)
    except KeyError:
        return JsonResponse({'error': 'Some keyerror'}, status=401)


def enrollSection(request, *args, **kwargs):
    if check_header(request):
        import re
        regex = re.compile('^HTTP_')
        dict_ = dict((regex.sub('', header), value) for (header, value)
                     in request.META.items() if header.startswith('HTTP_'))
        try:
            token = dict_['TOKEN']
        except KeyError:
            return JsonResponse({"error":"not authenticate"})
        section_id = kwargs['id']
        user = User.objects.filter(token=token).first()
        section = Section.objects.filter(id=section_id).first()
        section.student.add(user)
        section.save()
        return JsonResponse({"message":"successful"})
    return JsonResponse({"error": "not authenticate"})


################################################### College

def check_header(request):
    flag = False
    import re
    regex = re.compile('^HTTP_')
    dict_ = dict((regex.sub('', header), value) for (header, value)
                 in request.META.items() if header.startswith('HTTP_'))
    try:
        token = dict_['TOKEN']
    except KeyError:
        return False
    user = User.objects.filter(token=token).first()
    if user:
        flag = True
    return bool(flag)


class CollegeAPIView(rest_mixins.CreateModelMixin,
                     ListAPIView):
    # permission_classes   = [IsAuthenticated]
    # authentication_classes = [CustomAuthentication]
    serializer_class = CollegeSerializer
    queryset = College.objects.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = College.objects.all()
            serializer = CollegeSerializer(queryset, many=True)
            return JsonResponse({'colleges': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


class CollegeDetailAPIView(rest_mixins.DestroyModelMixin,
                           rest_mixins.UpdateModelMixin,
                           rest_mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = []
    serializer_class = CollegeSerializer
    queryset = College.objects.all()
    lookup_field = 'college_name'

    def get_object(self):
        q = College.objects.filter(college_name=self.kwargs['college_name']).distinct()
        return q

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            college = get_object_or_404(queryset)
            serializer = CollegeSerializer(college)
            return JsonResponse({'colleges': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Department


class DepartmentAPIView(rest_mixins.CreateModelMixin,
                        ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']).first().department_set.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = DepartmentSerializer(queryset, many=True)
            return JsonResponse({'departments': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


class DepartmentDetailAPIView(rest_mixins.DestroyModelMixin,
                              rest_mixins.UpdateModelMixin,
                              rest_mixins.CreateModelMixin,
                              generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = []
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    lookup_field = 'dep_name'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']).first().department_set.filter(
            dep_name=self.kwargs['dep_name']).distinct()

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            dep = get_object_or_404(queryset)
            serializer = DepartmentSerializer(dep)
            return JsonResponse({'departments': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Course


class CourseAPIView(rest_mixins.CreateModelMixin,
                    ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    #

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = CourseSerializer(queryset, many=True)
            return JsonResponse({'courses': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


class CourseDetailAPIView(rest_mixins.DestroyModelMixin,
                          rest_mixins.UpdateModelMixin,
                          rest_mixins.CreateModelMixin,
                          generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = []
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'course_name'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).distinct()

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            course = get_object_or_404(queryset)
            serializer = CourseSerializer(course)
            return JsonResponse({'courses': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})

    #


################################################### Section


class SectionAPIView(rest_mixins.CreateModelMixin,
                     ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = SectionSerializer(queryset, many=True)
            return JsonResponse({'sections': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


class SectionDetailAPIView(rest_mixins.DestroyModelMixin,
                           rest_mixins.UpdateModelMixin,
                           rest_mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = []
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.filter(id=self.kwargs['id']).distinct()

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            section = get_object_or_404(queryset)
            serializer = SectionSerializer(section)
            return JsonResponse({'sections': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Department


class DocumentAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().document_set.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = DocumentSerializer(queryset, many=True)
            return JsonResponse({'documents': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})

    def post(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.create(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


class DocumentDetailAPIView(rest_mixins.DestroyModelMixin,
                            rest_mixins.UpdateModelMixin,
                            rest_mixins.CreateModelMixin,
                            generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().document_set.filter(id=self.kwargs['i']).distinct()

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            doc = get_object_or_404(queryset)
            serializer = DocumentSerializer(doc)
            return JsonResponse({'documents': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})

    def put(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def patch(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def delete(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.destroy(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Message


class MessageAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().message_set.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = MessageSerializer(queryset, many=True)
            return JsonResponse({'messages': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})

    def post(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.create(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


class MessageDetailAPIView(rest_mixins.DestroyModelMixin,
                           rest_mixins.UpdateModelMixin,
                           rest_mixins.CreateModelMixin,
                           generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = []
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'i'

    def get_object(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(
            dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first().section_set.filter(
            id=self.kwargs['id']).first().message_set.filter(
            id=self.kwargs['i']).distinct()

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            msg = get_object_or_404(queryset)
            serializer = MessageSerializer(msg)
            return JsonResponse({'messages': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})

    def put(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def patch(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def delete(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.destroy(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Video

class VideoAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_queryset(self):
        if check_header(self.request):
            return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
                .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
                name=self.kwargs['course_name']).first() \
                .section_set.filter(id=self.kwargs['id']).first().video_set.all()
        else:
            return JsonResponse({"error": "not authen!"})

    def post(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.create(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = VideoSerializer(queryset, many=True)
            return JsonResponse({'videos': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


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
        if check_header(self.request):
            queryset = self.get_object()
            vid = get_object_or_404(queryset)
            serializer = VideoSerializer(vid)
            return JsonResponse({'videos': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Homework


class HomeworkAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().homework_set.all()

    def post(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.create(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = HomeworkSerializer(queryset, many=True)
            return JsonResponse({'homeworks': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


class HomeworkDetailView(rest_mixins.DestroyModelMixin,
                         rest_mixins.UpdateModelMixin,
                         rest_mixins.CreateModelMixin,
                         generics.RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
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
        if check_header(self.request):
            queryset = self.get_object()
            vid = get_object_or_404(queryset)
            serializer = HomeworkSerializer(vid)
            return JsonResponse({'homeworks': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})

    def put(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def patch(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def delete(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.destroy(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


################################################### Solution


class SolutionAPIView(rest_mixins.CreateModelMixin, ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()

    def get_queryset(self):
        return College.objects.filter(college_name__iexact=self.kwargs['college_name']) \
            .first().department_set.filter(dep_name=self.kwargs['dep_name']).first().course_set.all().filter(
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first().homework_set.filter(
            id=self.kwargs['i']).first().solution_set.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = SolutionSerializer(queryset, many=True)
            return JsonResponse({'solutions': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


    def post(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.create(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


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
            name=self.kwargs['course_name']).first() \
            .section_set.filter(id=self.kwargs['id']).first() \
            .homework_set.filter(id=self.kwargs['i']).first().solution_set.filter(id=self.kwargs['si']).distinct()

    def retrieve(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_object()
            vid = get_object_or_404(queryset)
            serializer = SolutionSerializer(vid)
            return JsonResponse({'solutions': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


    def put(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def patch(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.update(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})

    def delete(self, request, *args, **kwargs):
        if check_header(self.request):
            return self.destroy(request, *args, **kwargs)
        else:
            return JsonResponse({"error": "not authen!"})


class StudentSectionAPIView(rest_mixins.CreateModelMixin,
                            ListAPIView):
    #permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    def get_queryset(self):
        return Section.objects.filter(student__id=self.kwargs['student_id'])

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = SectionSerializer(queryset, many=True)
            return JsonResponse({'sections': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})


class SectionStudentsAPIView(rest_mixins.CreateModelMixin,
                             ListAPIView):
    # permission_classes   = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = StudentSerializer
    queryset = Section.objects.all()

    def get_queryset(self):
        section_id = self.kwargs['id']
        return Section.objects.filter(id=section_id).first().student.all()

    def list(self, *args, **kwargs):
        if check_header(self.request):
            queryset = self.get_queryset()
            serializer = StudentSerializer(queryset, many=True)
            return JsonResponse({'students': serializer.data})
        else:
            return JsonResponse({"error": "not authen!"})
