from django.contrib import admin
from .models import Snack, Comment, Vote

# Register your models here.
admin.site.register(Snack)
admin.site.register(Comment)
admin.site.register(Vote)