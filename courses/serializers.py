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

class CourseSectionUnPaidSerializer(ModelSerializer):
    episodes=EpisodeUnpaidSerializer(many=True)
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
    class Meta:
        model=Course
        exclude=[
            'id'
        ]

# no-2,len-35min

