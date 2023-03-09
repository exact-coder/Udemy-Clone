from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from courses.serializers import (CourseDisplaySerializer,CourseUnpaidSerializer,CourseListSerializer,CommentSerializer,CartItemSerializer,CoursePaidSerializer)
from courses.models import *
from django.http import HttpResponseBadRequest,HttpResponseNotAllowed
from django.db.models import Q
import json
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated




# Create your views here.

class CoursesHomeView(APIView):
    def get(self,request,*args, **kwargs):
        sectors = Sector.objects.order_by('?')[:6]
        sector_response=[]

        for sector in sectors:
            sector_courses = sector.releted_course.order_by("?")[:4]
            course_serializer=CourseDisplaySerializer(sector_courses,many=True)

            sector_obj={
                'sector_name':sector.name,
                'sector_uuid':sector.sector_uuid,
                'featured_course':course_serializer.data,
                'sector_image':sector.get_image_absolute_url(),
            }
            sector_response.append(sector_obj)
        return Response(data=sector_response,status=status.HTTP_200_OK)
    
class CourseDetail(APIView):
    def get(self,request,course_uuid,*args, **kwargs):
        course = Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseBadRequest('Course does not exist')
        serializer=CourseUnpaidSerializer(course[0])

        return Response(data=serializer.data,status=status.HTTP_200_OK)
        
class SectorCourse(APIView):
    def get(self,request,sector_uuid,*args, **kwargs):
        sector=Sector.objects.filter(sector_uuid=sector_uuid)

        if not sector:
            return HttpResponseBadRequest('Sector does not exist')
        sector_courses=sector[0].releted_course.all()
        serializer=CourseListSerializer(sector_courses,many=True)

        total_students=0
        for course in sector_courses:
            total_students +=course.get_enrolled_student()

        return Response({
            'data':serializer.data,
            'sector_name':sector[0].name,
            'total_students':total_students,
        },status=status.HTTP_200_OK)

class SearchCourse(APIView):
    def get(self,request,search_term):
        matches=Course.objects.filter(Q(title__icontains=search_term)| Q(description__icontains=search_term)|Q(language__icontains=search_term) |Q(price__icontains=search_term))
        serializer=CourseListSerializer(matches,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class AddComment(APIView):
    permission_classes={IsAuthenticated}
    def post(self,request,course_uuid):
        try:
            course=Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest('Course Does not Exist')

        try:
            content=json.loads(request.body)
        
        except json.decoder.JSONDecodeError:
            return Response('Please provide a JSON Body',status=status.HTTP_400_BAD_REQUEST)
        
        if not content.get('message'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=CommentSerializer(data=content)

        if serializer.is_valid():
            comment=serializer.save(user=request.user)
            course.comments.add(comment)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetCartDetail(APIView):
    def post(self,request):
        try:
            body=json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest("404,Bad Req")
        if type(body.get('cart')) != list:
            return HttpResponseBadRequest("404,Bad Man")
        if len(body.get('cart')) ==0:
            return Response([])
        
        courses=[]
        for uuid in body.get('cart'):
            item=Course.objects.filter(course_uuid=uuid)

            if not item:
                return HttpResponseBadRequest("Not get the item")
            courses.append(item[0])
        serializer = CartItemSerializer(courses,many=True)
        cart_total=Decimal(0.00)
        for item in serializer.data:
            cart_total+=Decimal(item.get('price'))

        return Response(data={
            'cart_detail':serializer.data,
            'cart_total':cart_total,
        },status=status.HTTP_200_OK)

class CourseStudy(APIView):
    permission_classes=[IsAuthenticated] 
    def get(self,request,course_uuid):
        try:
            course=Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest("Course Does not exist")
        
        # request.user=User.objects.get(id=1)
        user_course = request.user.paid_courses.filter(course_uuid=course_uuid)

        if not user_course:
            return HttpResponseNotAllowed('User does not own this Course')
        serializer=CoursePaidSerializer(course)
        return Response(serializer.data,status=status.HTTP_200_OK)


# no-4,len-00min
