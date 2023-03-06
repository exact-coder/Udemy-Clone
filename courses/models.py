from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from decimal import Decimal
from courses.helpers import get_timer
from mutagen.mp4 import MP4,MP4StreamInfoError


# Create your models here.

class Sector(models.Model):
    name = models.CharField(_("Sector Name"), max_length=250)
    sector_uuid = models.UUIDField(_("Sector Unique Id"),default=uuid.uuid4,unique=True) # type: ignore
    releted_course = models.ManyToManyField("Course", verbose_name=_("Releted Courses"),blank=True)
    sector_image = models.ImageField(_("Sector Image"), upload_to="sector_image")

    def get_image_absolute_url(self):
        return 'http://localhost:8000'+self.sector_image.url


class Course(models.Model):
    title = models.CharField(_("Course Title"), max_length=250)
    description = models.TextField(_("Course Description"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("USER"), on_delete=models.CASCADE)
    language = models.CharField(_("Language"), max_length=50)
    course_section = models.ManyToManyField("CourseSection", verbose_name=_("Course Section"),blank=True)
    comments = models.ManyToManyField("Comment", verbose_name=_("Comments"),blank=True)
    image_url = models.ImageField(_("Course Image"), upload_to='course_images')
    course_uuid = models.UUIDField(_("Course Unique ID"),default=uuid.uuid4,unique=True)
    price = models.DecimalField(_("Course Price"), max_digits=7, decimal_places=2)

    def get_brief_description(self):
        return self.description[:100]
    
    def get_enrolled_student(self):
        students=get_user_model().objects.filter(paid_courses=self)
        return len(students)
    
    def get_total_lectures(self):
        lectures =0
        for section in self.course_section.all():
            lectures += len(section.episodes.all())
        return lectures
    
    def total_course_length(self):
        length=Decimal(0.0)
        for section in self.course_section.all():
            for episode in section.episodes.all():
                length += episode.length
        return get_timer(length,type='short') # type: ignore
    
    def get_absolute_image_url(self):
        return 'http://localhost:8000'+self.image_url.url

class CourseSection(models.Model):
    section_title = models.CharField(_("Section Title"), max_length=250)
    episodes = models.ManyToManyField("Episode", verbose_name=_("Episode"),blank=True)

    def total_length(self):
        total=Decimal(0.0)
        for episode in self.episodes.all():
            total+=episode.length
        return get_timer(total,type='min') # type: ignore


class Episode(models.Model):
    title = models.CharField(_("Title Of Episode"), max_length=250)
    file = models.FileField(_("Courses Vedio"), upload_to='course_vedios')
    length = models.DecimalField(_("Vedio Length"), max_digits=10, decimal_places=2)

    def get_video_length(self):
        try:
            vedio=MP4(self.file)
            return vedio.info.length
        except MP4StreamInfoError:
            return 0.0
    
    def get_video_length_time(self):
        return get_timer(self.length) # type: ignore
    
    def get_absolute_url(self):
        return 'http://localhost:8000/'+self.file.url 
    
    def save(self,*args, **kwargs):
        self.length = self.get_video_length()
        return super().save(*args,**kwargs)



class Comment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    message = models.TextField(_("Comment"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)




