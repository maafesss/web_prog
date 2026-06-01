from django.contrib import admin

from main.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass