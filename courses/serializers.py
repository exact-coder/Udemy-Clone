from rest_framework.serializers import ModelSerializer
from courses.models import Course
from rest_framework.serializers import Serializer

class CourseDisplaySerializer(ModelSerializer):
    student_no = Serializer
    class Meta:
        model = Course
        fields=[
            'course_uuid','title','student_no','author','price','image_url',
        ]

# no-1,len-1.49min