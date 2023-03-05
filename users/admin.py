from django.contrib import admin
from users.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=['id','name','email','is_staff']
    list_display_links=['id','name','email']
admin.site.register(User,UserAdmin)
