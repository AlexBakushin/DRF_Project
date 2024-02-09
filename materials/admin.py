from django.contrib import admin
from materials.models import Course, Lesson


@admin.register(Course)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('course_name',)
    list_filter = ('course_name',)
    search_fields = ('course_name',)


@admin.register(Lesson)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('lesson_name', 'course',)
    list_filter = ('lesson_name',)
    search_fields = ('lesson_name', 'course',)

