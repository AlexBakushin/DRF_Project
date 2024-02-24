from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Course, Lesson, Subscription
from .paginators import MaterialPaginator
from .serliazers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsOwner, IsModer, IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialPaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
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


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = MaterialPaginator

    def get_queryset(self):
        if self.request.user.is_staff:
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer & IsOwner]


class SubscriptionView(APIView):
    queryset = Course.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message})
