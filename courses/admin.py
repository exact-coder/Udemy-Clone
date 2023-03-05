from django.contrib import admin
from courses.models import Course,Sector,Episode,CourseSection,Comment


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display =['course_uuid','title','author','language','price']
    list_display_links=['course_uuid','title']
admin.site.register(Course,CourseAdmin)

class SectorAdmin(admin.ModelAdmin):
    list_display =['id','name','sector_uuid']
    list_display_links=['id','name']
admin.site.register(Sector,SectorAdmin)

class EpisodeAdmin(admin.ModelAdmin):
    list_display =['id','title','length']
    list_display_links=['id','title']
admin.site.register(Episode,EpisodeAdmin)

class CourseSectionAdmin(admin.ModelAdmin):
    list_display =['id','section_title']
    list_display_links=['id','section_title']
admin.site.register(CourseSection,CourseSectionAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display =['id','user','message']
    list_display_links=['id']
admin.site.register(Comment,CommentAdmin)
