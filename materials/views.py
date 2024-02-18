from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serliazers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsOwner, IsNotModer, IsOwnerOrStaff


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModer]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner, IsNotModer]

        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsNotModer]
