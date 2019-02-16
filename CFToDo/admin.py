from django.contrib import admin
from .models import UserDetails, Ladder, Tag, Problem
from django.contrib.auth.models import User


admin.site.register(UserDetails)
admin.site.register(Ladder)
admin.site.register(Tag)
admin.site.register(Problem)
