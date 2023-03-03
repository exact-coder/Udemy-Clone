from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Course(models.Model):
    title = models.CharField(_("Course Title"), max_length=250)
    description = models.TextField(_("Course Description"))
    created = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    # author = models.ForeignKey(User, verbose_name=_("USER"), on_delete=models.CASCADE)
    language = models.CharField(_("Language"), max_length=50)


# no-1,len-11min