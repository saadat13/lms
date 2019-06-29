from django.urls import path,re_path

# from api.views import mAuthView, login
from api.views import login, check_header
from . import views


urlpatterns = [
    path('colleges/', views.CollegeAPIView.as_view()),
    path('colleges/<college_name>/', views.CollegeDetailAPIView.as_view()),
    path('colleges/<college_name>/departments/', views.DepartmentAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/', views.DepartmentDetailAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/', views.CourseAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/', views.CourseDetailAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/', views.SectionAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/', views.SectionDetailAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/stds/', views.SectionStudentsAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/docs/', views.DocumentAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/docs/<i>/', views.DocumentDetailAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/msgs/', views.MessageAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/msgs/<i>/', views.MessageDetailAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/vids/', views.VideoAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/vids/<i>/', views.VideoDetailView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/hws/', views.HomeworkAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/hws/<i>/', views.HomeworkDetailView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/sls/<i>/', views.SolutionAPIView.as_view()),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/sls/<i>/<si>/', views.SolutionDetailView.as_view()),
    path('dl/<path:encoded_url>', views.download) ,# download file using posting file path to server
    path('<student_id>/sections/', views.StudentSectionAPIView.as_view()),
    path('login/', login),
    path('colleges/<college_name>/departments/<dep_name>/courses/<course_name>/sections/<id>/enroll/', views.enrollSection),

]
