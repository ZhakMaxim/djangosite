from rest_framework.test import APITestCase
from django.urls import reverse
from MarkingSystem.urls import *
from edushedule.serializers import *

class UserRegistrationViewTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('register')
        cls.group = Group.objects.create(id=1, name='11')
        cls.student = Student.objects.create(name='student', group=cls.group)

    def test_valid_registration(self):
        data = {
            'login': 'user',
            'password': '1234',
            'status': 'teacher',
            'student': self.student.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.login, 'user')
        self.assertEqual(user.status, 'teacher')
        self.assertEqual(user.student, self.student)

    def test_invalid_registration(self):
        data = {
            'login': 'user',
            'password': '1234',
            'status': 'invalid',
            'student': self.student.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserAuthorizationViewTests(APITestCase):

    def setUp(self):
        self.group = Group.objects.create(id=1, name='11')
        self.student = Student.objects.create(name='student', group=self.group)
        self.user = User.objects.create(login='test', password='1234', status='teacher', student=self.student)
        self.url = 'http://127.0.0.1:8000/eduschedule/api/v1/login'

    def test_valid_login(self):
        data = {
            'login': 'test',
            'password': '1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['login'], 'test_user')
        self.assertEqual(response.data['status'], 'teacher')
        self.assertEqual(response.data['student'], self.student.id)
        self.assertEqual(response.data['group_id'], self.group.id)
        self.assertEqual(response.data['group'], self.group.name)


class EventViewSetTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = 'http://127.0.0.1:8000/eduschedule/api/v1/events/'
        cls.url_1 = 'http://127.0.0.1:8000/eduschedule/api/v1/events/1/'
        cls.model = Event.objects.create(name='event1', description='...')

    def test_get_events_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'event1')

    def test_get_one_event(self):
        response = self.client.get(self.url_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data['name'], 'event1')

    def test_create_event(self):
        data = {'name': 'event2', 'description': '...'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.get(id=2).name, 'event2')
        self.assertEqual(Event.objects.get(id=2).description, '...')

    def test_change_event(self):
        data = {'name': 'new_event', 'description': '123'}
        response = self.client.put(self.url_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get(id=1).name, 'new_event')
        self.assertEqual(Event.objects.get(id=1).description, '123')

    def test_delete_event(self):
        response = self.client.delete(self.url_1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)


class StudentsListViewTests(APITestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/eduschedule/api/v1/students'
        self.url_filter_by_group_id = 'http://127.0.0.1:8000/eduschedule/api/v1/students/1/'
        self.group = Group.objects.create(id=1, name='11')
        self.student1 = Student.objects.create(name='Student1', group_id=self.group.id)
        self.student2 = Student.objects.create(name='Student2', group_id=self.group.id)
        self.mark1 = Mark.objects.create(value=10, subject='Math', student=self.student1)
        self.mark2 = Mark.objects.create(value=9, subject='History', student=self.student1)

    def test_get_students_list(self):
        response = self.client.get(self.url)
        expected_data = StudentListSerializer([self.student1, self.student2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_students_list_filter_by_group_name(self):
        response = self.client.get(self.url_filter_by_group_id)
        expected_data = StudentListSerializer([self.student1, self.student2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class SheduleListViewTests(APITestCase):

    def setUp(self):
        self.group = Group.objects.create(id=1, name='11')
        self.schedule = Schedule.objects.create(
            day_of_week="Monday",
            start_time="08:00:00",
            end_time="09:00:00",
            class_name="Math",
            classroom=101,
            schedule=self.group
        )

    def test_get_schedule_list(self):
        url = 'http://127.0.0.1:8000/eduschedule/api/v1/schedule/1/'
        response = self.client.get(url)
        schedules = Schedule.objects.filter(schedule=self.group)
        serializer = SсheduleSerializer(schedules, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ScheduleViewSetTestCase(APITestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/eduschedule/api/v1/schedule/id/1/'
        self.group = Group.objects.create(id=1, name='11')
        self.schedule = Schedule.objects.create(
            day_of_week="Monday",
            start_time="08:00:00",
            end_time="09:00:00",
            class_name="Math",
            classroom=101,
            schedule=self.group
        )

    def test_get_schedule_by_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data['day_of_week'], 'Monday')

class MarkDetailViewTests(APITestCase):

    def setUp(self):
        self.mark = Mark.objects.create(value=8, subject='Math')

    def test_get_mark_detail(self):
        url = 'http://127.0.0.1:8000/eduschedule/api/v1/marks/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], self.mark.value)
        self.assertEqual(response.data['subject'], self.mark.subject)

    def test_update_mark(self):
        url = 'http://127.0.0.1:8000/eduschedule/api/v1/marks/1/'
        data = {'value': 9, 'subject': 'Math'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mark.refresh_from_db()
        self.assertEqual(self.mark.value, data['value'])
        self.assertEqual(self.mark.subject, data['subject'])

    def test_delete_mark(self):
        url = 'http://127.0.0.1:8000/eduschedule/api/v1/marks/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mark.objects.filter(id=self.mark.id).exists())

class StudentMarkDetailViewTests(APITestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/eduschedule/api/v1/marks/1/create'
        self.group = Group.objects.create(id=1, name='11')
        self.student = Student.objects.create(id=1, name='student', group=self.group)
        self.mark = Mark.objects.create(value=5, subject='Math')
        self.student.marks.add(self.mark)

    # def test_create_student_mark(self):
    #     data = {'subject': 'math', 'value': 9}
    #     response = self.client.post(self.url, data=data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
