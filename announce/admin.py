from django.contrib import admin
from .models import Announce, Comment, Applying

admin.site.register(Announce)
admin.site.register(Comment)
admin.site.register(Applying)