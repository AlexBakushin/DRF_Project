from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from materials.models import Lesson, Course
from users.models import User


class MaterialTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_lesson_is_admin(self):
        """
        Тест на то, что админ может создать урок
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

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

    def test_create_lesson_is_user(self):
        """
        Тест на то, что обычный пользователь может создать урок
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.test", is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

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
            {'id': 2, 'lesson_name': 'first_test', 'lesson_description': 'first_test', 'lesson_preview': None,
             'lesson_link': 'http://localhost:8000/lesson/1/', 'course': None, 'owner': 3}
        )

    def test_create_lesson_is_moder(self):
        """
        Тест на то, что модератор не может создать урок
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

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
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}

        )

    def test_list_lesson_is_admin(self):
        """
        Тест на то что админ видит все уроки
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

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
                {'id': 6, 'lesson_name': 'list_test', 'lesson_description': 'list_test', 'lesson_preview': None,
                 'lesson_link': 'http://localhost:8000/lesson_list/1/', 'course': None, 'owner': None}]}
        )

    def test_list_lesson_is_user(self):
        """
        Тест на то что обычный пользователь не видит чужие уроки, но видит свои
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.test", is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='list_test',
            lesson_description='list_test',
            lesson_link='http://localhost:8000/lesson_list/1/'
        )

        Lesson.objects.create(
            lesson_name='list_test_user',
            lesson_description='list_test_user',
            lesson_link='http://localhost:8000/lesson_list/2/',
            owner=self.user
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
                {'course': None, 'id': 9, 'lesson_description': 'list_test_user',
                 'lesson_link': 'http://localhost:8000/lesson_list/2/', 'lesson_name': 'list_test_user',
                 'lesson_preview': None, 'owner': 9}]}
        )

    def test_list_lesson_is_moder(self):
        """
        Тест на то что модератор видит все уроки
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

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
                {'id': 7, 'lesson_name': 'list_test', 'lesson_description': 'list_test', 'lesson_preview': None,
                 'lesson_link': 'http://localhost:8000/lesson_list/1/', 'course': None, 'owner': None}]}
        )

    def test_update_lesson_is_admin(self):
        """
        Тест на то что админ может обновлять урок
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='update_test_admin',
            lesson_description='update_test_admin',
            lesson_link='http://localhost:8000/update_test/1/',
            owner=self.user
        )

        response = self.client.patch(
            '/lesson/update/10/',
            {"lesson_description": "new_update_test_admin"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 10, 'lesson_name': 'update_test_admin', 'lesson_description': 'new_update_test_admin', 'lesson_preview': None,
             'lesson_link': 'http://localhost:8000/update_test/1/', 'course': None, 'owner': 13}
        )

    def test_update_lesson_is_user(self):
        """
        Тест на то что обычный пользователь может обновлять свой урок
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.test", is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='update_test_user',
            lesson_description='update_test_user',
            lesson_link='http://localhost:8000/update_test_user/1/',
            owner=self.user
        )

        response = self.client.patch(
            '/lesson/update/12/',
            {"lesson_description": "new_update_test_user"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 12, 'lesson_name': 'update_test_user', 'lesson_description': 'new_update_test_user',
             'lesson_preview': None,
             'lesson_link': 'http://localhost:8000/update_test_user/1/', 'course': None, 'owner': 15}
        )

    def test_update_lesson_is_moder(self):
        """
        Тест на то что модератор может обновлять урок
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='update_test_moder',
            lesson_description='update_test_moder',
            lesson_link='http://localhost:8000/update_test/1/',
        )

        response = self.client.patch(
            '/lesson/update/11/',
            {"lesson_description": "new_update_test_moder"}
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 11, 'lesson_name': 'update_test_moder', 'lesson_description': 'new_update_test_moder',
             'lesson_preview': None,
             'lesson_link': 'http://localhost:8000/update_test/1/', 'course': None, 'owner': None}
        )

    def test_delete_lesson_is_admin(self):
        """
        Тест на то что админ может удалять урок
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='delete_test_admin',
            lesson_description='delete_test_admin',
            lesson_link='http://localhost:8000/delete_test_admin/1/',
            owner=self.user
        )

        response = self.client.delete(
            '/lesson/delete/3/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_delete_lesson_is_user(self):
        """
        Тест на то что обычный пользователь не может удалять чужой урок
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.test", is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='delete_test_user',
            lesson_description='delete_test_user',
            lesson_link='http://localhost:8000/delete_test_user/1/',
        )

        response = self.client.delete(
            '/lesson/delete/5/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_delete_lesson_is_moder(self):
        """
        Тест на то что модератор не может удалять любой урок
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            lesson_name='delete_test',
            lesson_description='delete_test',
            lesson_link='http://localhost:8000/delete_test/1/',
        )

        response = self.client.delete(
            '/lesson/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_subscription_is_admin(self):
        """
        Тест на то что админ может делать подписку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="admin@sky.pro", is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

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

    def test_subscription_is_user(self):
        """
        Тест на то что обычный пользователь может делать подписку
        """
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.test", is_superuser=False, is_staff=False)
        self.client.force_authenticate(user=self.user)

        Course.objects.create(
            course_name='subscription_test',
            course_description='subscription_test',
        )

        resp = self.client.post(
            '/subscription/',
            {
                "user": 12,
                "course": 3
            }
        )

        self.client.patch(
            '/courses/3/',
            {
                "course_name": "new_subscription_test",
                "course_description": "new_subscription_test"
            }
        )

        response = self.client.post(
            '/subscription/',
            {
                "user": 12,
                "course": 3
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

    def test_subscription_is_moder(self):
        """
        Тест на то что модератор не может делать подписку
        """
        group, created = Group.objects.get_or_create(name='moderator')
        self.client = APIClient()
        self.user = User.objects.create(email="moder@test.com", is_superuser=False, is_staff=True)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        Course.objects.create(
            course_name='subscription_test',
            course_description='subscription_test',
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
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )
