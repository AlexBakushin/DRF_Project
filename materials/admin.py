from django.contrib import admin
from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name',)
    list_filter = ('course_name',)
    search_fields = ('course_name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_name', 'course',)
    list_filter = ('lesson_name',)
    search_fields = ('lesson_name', 'course',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user',)
    search_fields = ('user',)
