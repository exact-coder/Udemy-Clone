from django.urls import path
from courses.views import CoursesHomeView,CourseDetail,SectorCourse,SearchCourse,AddComment,GetCartDetail,CourseStudy


urlpatterns = [
    path('',CoursesHomeView.as_view(),name='home'),
    path('detail/<uuid:course_uuid>/',CourseDetail.as_view(),name='course_details'),
    path('<uuid:sector_uuid>/',SectorCourse.as_view(),name='sector_course'),
    path('search/<str:search_term>/',SearchCourse.as_view(),name='search'),
    path('comment/<uuid:course_uuid>/',AddComment.as_view(),name='add_comment'),
    path('cart/',GetCartDetail.as_view(),name='cart'),
    path('study/<uuid:course_uuid>',CourseStudy.as_view(),name='course_study'),
]
