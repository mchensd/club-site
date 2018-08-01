from django.contrib import admin
from .models import Announcement, Comment, Contest, Score, Profile
# Register your models here.
admin.site.register(Announcement)
admin.site.register(Comment)
admin.site.register(Contest)
admin.site.register(Score)
admin.site.register(Profile)


