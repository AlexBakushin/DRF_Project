from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Subscription
from .paginators import MaterialPaginator
from .serliazers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsOwner, IsModer, IsOwnerOrModerator
from .services import get_session
from drf_yasg.utils import swagger_auto_schema
from .tasks import update_notification
from users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet модели Курса
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialPaginator

    def perform_create(self, serializer):
        """
        При создании модели курса owner автоматически становится авторизированный пользователь
        """
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        """
        Передает queryset только тех курсов, где owner - пользователь, кроме админа и модератора
        """
        if self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Ограничения режимами доступа
        """
        if self.action == 'create':
            self.permission_classes = [~IsModer]
        elif self.action == 'list':
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == 'update':
            self.permission_classes = [IsOwnerOrModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner, ~IsModer & IsOwner]

        return [permission() for permission in self.permission_classes]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        users_id_sub = Subscription.objects.filter(course=instance).values_list('user', flat=True)
        for user_id in users_id_sub:
            user_email = User.objects.get(id=user_id).email
            course_name = instance.course_name
            update_notification.delay(user_email=user_email, course_name=course_name)

        return Response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создание модели урока, модератор не может
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """
        При создании, owner - пользователь
        """
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    Список уроков
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = MaterialPaginator

    def get_queryset(self):
        """
        Передает queryset только тех уроков, где owner - пользователь, кроме админа и модератора
        """
        if self.request.user.is_staff:
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Выводит модель выбранного урока, только те, где owner - пользователь, кроме админа и модератора
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление выбранного урока, только те, где owner - пользователь, кроме админа и модератора
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление выбранного урока, только те, где owner - пользователь, модератор не может
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer & IsOwner]


class SubscriptionView(APIView):
    """
    Создает или удаляет подписку
    """
    queryset = Course.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    @swagger_auto_schema(operation_description="Если нет - создает, если есть - удаляет модель Subscription",
                         responses={200: SubscriptionSerializer(many=True)})
    def post(self):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
            return Response({"message": message})
        else:
            new_sub = Subscription.objects.create(user=user, course=course_item)
            session = get_session(new_sub)
            message = 'Ссылка на оплату'
            return Response({"message": message, "session": session['url']})


class SubscriptionSuccessView(APIView):
    """
    Переводит поле 'is_paid' модели 'Subscription' в положение 'True'
    и выводит поздравительное сообщение
    """
    queryset = Course.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    @swagger_auto_schema(operation_description="Переводит поле 'is_paid' модели 'Subscription' в положение 'True'"
                                               "и выводит поздравительное сообщение",
                         responses={200: SubscriptionSerializer(many=True)})
    def get(self):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item).first()
        subs_item.is_paid = True
        subs_item.save()
        message = 'Подписка оформлена'

        return Response({"message": message})
