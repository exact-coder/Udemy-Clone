from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from courses.models import Course,Comment,CourseSection,Episode
from users.serializers import UserSerializer

class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.ImageField(source='get_enrolled_student')
    author = UserSerializer()
    image_url=serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model = Course
        fields=[
            'course_uuid','title','student_no','author','price','image_url',
        ]

class CommentSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        exclude=[
            'id'
        ]

class EpisodeUnpaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    class Meta:
        model = Episode
        exclude=[
            'file'
        ]

class EpisodepaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    class Meta:
        model = Episode
        fields=[
            'file',
            'length',
            'title'
        ]


class CourseSectionUnPaidSerializer(ModelSerializer):
    episodes=EpisodeUnpaidSerializer(many=True)
    total_duration=serializers.CharField(source='total_length')
    class Meta:
        model = CourseSection
        fields=[
            'section_title','episodes','total_duration'
        ]


class CourseSectionPaidSerializer(ModelSerializer):
    episodes=EpisodepaidSerializer(many=True)
    total_duration=serializers.CharField(source='total_length')
    class Meta:
        model = CourseSection
        fields=[
            'section_title','episodes','total_duration'
        ]


class CourseUnpaidSerializer(ModelSerializer):
    comments =CommentSerializer(many=True)
    author=UserSerializer()
    course_section = CourseSectionUnPaidSerializer(many=True)
    student_no=serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration=serializers.CharField(source='total_course_length')
    image_url=serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model=Course
        exclude=[
            'id'
        ]

class CoursePaidSerializer(ModelSerializer):
    comments =CommentSerializer(many=True)
    author=UserSerializer()
    course_section = CourseSectionPaidSerializer(many=True)
    student_no=serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration=serializers.CharField(source='total_course_length')
    image_url=serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model=Course
        exclude=[
            'id'
        ]


class CourseListSerializer(ModelSerializer):
    student_no=serializers.IntegerField(source='get_enrolled_student')
    author=UserSerializer()
    description=serializers.CharField(source='get_brief_description')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    image_url=serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model=Course
        fields=['course_uuid','title','student_no','author','price','description','image_url','total_lectures'] 

class CartItemSerializer(ModelSerializer):
    author=UserSerializer()
    image_url=serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model=Course
        fields=[
            'author','title','price','image_url'
        ]






