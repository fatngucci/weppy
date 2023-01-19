from django.contrib import admin
from .models import Snack, Comment, Vote, Report

# Register your models here.
admin.site.register(Snack)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Report)
