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
    is_subscribe = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [DescriptionValidator(field='course_description')]

    def get_quantity_lessons(self, instance):
        return instance.lesson_set.all().count()

    def get_is_subscribe(self, course):
        """
        Добавляет в сериализатор признак подписки на данный курс
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_subscription = Subscription.objects.filter(course=course.pk, user=request.user).first()
            return user_subscription is not None

        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
