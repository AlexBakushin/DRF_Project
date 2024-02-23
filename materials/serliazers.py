from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from .validators import DescriptionValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [DescriptionValidator(field='lesson_description')]


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [DescriptionValidator(field='course_description')]

    def get_quantity_lessons(self, instance):
        return instance.lesson_set.all().count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
