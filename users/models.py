from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from courses.models import Course

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self,email,password,name,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is not True:
            return ValueError('Superuser must be is_staff True')
        if other_fields.get('is_superuser') is not True:
            return ValueError('Superuser must be is_superuser True')
        return self.create_user(email,password,name,**other_fields)
    
    def create_user(self,email,password,name,**other_fields):
        other_fields.setdefault('is_staff',False)
        other_fields.setdefault('is_superuser',False)
        if not email:
            raise ValueError('You must provide a valid Email')
        email = self.normalize_email(email)
        user= self.model(email=email,name=name,**other_fields)

        user.set_password(password)
        user.save()
        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(_("User Name"), max_length=250)
    email = models.EmailField(_("User Email"), max_length=254,unique=True)
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    update=models.DateTimeField(_("Update"), auto_now=True, auto_now_add=False)
    is_staff=models.BooleanField(_("IS STAFF"),default=False)
    paid_courses = models.ManyToManyField(Course, verbose_name=_("course"))

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    objects=UserManager()
    
    def __str__(self):
        return self.name + " " + self.email
    
    def get_all_courses(self):
        courses=[]
        for course in self.paid_courses.all():
            courses.append(course.course_uuid)
        return courses

