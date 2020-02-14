from django.contrib import admin

from qanda.models import Question, Answer
from .models import Profile


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)