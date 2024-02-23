from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from materials.models import Lesson, Course
from users.models import User


class MaterialTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            "lesson_name": "first_test",
            "lesson_description": "first_test",
            "lesson_link": "http://localhost:8000/lesson/1/"
        }

        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'lesson_name': 'first_test', 'lesson_description': 'first_test', 'lesson_preview': None,
             'lesson_link': 'http://localhost:8000/lesson/1/', 'course': None, 'owner': 1}
        )

    def test_list_lesson(self):
        Lesson.objects.create(
            lesson_name='list_test',
            lesson_description='list_test',
            lesson_link='http://localhost:8000/lesson_list/1/'
        )

        response = self.client.get(
            '/lesson/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': 1, 'lesson_name': 'list_test', 'lesson_description': 'list_test', 'lesson_preview': None,
                 'lesson_link': 'http://localhost:8000/lesson_list/1/', 'course': None, 'owner': None}]}
        )

    def test_update_lesson(self):
        Lesson.objects.create(
            lesson_name='update_test',
            lesson_description='update_test',
            lesson_link='http://localhost:8000/update_test/1/',
            owner=self.user
        )

        response = self.client.patch(
            '/lesson/update/1/',
            {"lesson_description": "new_update_test"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'lesson_name': 'update_test', 'lesson_description': 'new_update_test', 'lesson_preview': None,
             'lesson_link': 'http://localhost:8000/update_test/1/', 'course': None, 'owner': 1}
        )

    def test_delete_lesson(self):
        Lesson.objects.create(
            lesson_name='delete_test',
            lesson_description='delete_test',
            lesson_link='http://localhost:8000/delete_test/1/',
            owner=self.user
        )

        response = self.client.delete(
            '/lesson/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_subscription(self):
        Course.objects.create(
            course_name='subscription_test',
            course_description='subscription_test',
        )

        resp = self.client.post(
            '/subscription/',
            {
                "user": 1,
                "course": 1
            }
        )

        self.client.patch(
            '/courses/1/',
            {
                "course_name": "new_subscription_test",
                "course_description": "new_subscription_test"
            }
        )

        response = self.client.post(
            '/subscription/',
            {
                "user": 1,
                "course": 1
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            resp.json(),
            {'message': 'Подписка добавлена'}

        )

        self.assertEqual(
            response.json(),
            {'message': 'Подписка удалена'}
        )
