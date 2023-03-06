from django.urls import path
from courses.views import CoursesHomeView,CourseDetail


urlpatterns = [
    path('',CoursesHomeView.as_view(),name='home'),
    path('detail/<uuid:course_uuid>/',CourseDetail.as_view(),name='course_details'),
]
