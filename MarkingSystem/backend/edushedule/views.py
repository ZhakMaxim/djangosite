from django.http import HttpResponseBadRequest, HttpResponse
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import *

from .serializers import *
from .models import *

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'message': 'User successfully registered!',
            }
            return Response(response, status=status_code)


class UserAuthorizationView(APIView):
    serializer_class = UserAuthorizationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        print(request.data)

        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'login': serializer.data['login'],
                'status': serializer.data['status'],
                'student_id': serializer.data['student'],
                'group': serializer.data['group'],
                'group_id': serializer.data['group_id'],
                'name': serializer.data['name'],
            }
            return Response(response, status=status_code)

class UserListView(APIView):
    serializer_class = UserListSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        response = {
            'users': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventListSerializer
    queryset = Event.objects.all()
    #permission_classes = (IsAuthenticated,)


class EventPhotoView(View):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return HttpResponseBadRequest("Event does not exist")

        if not event.photo:
            return HttpResponseBadRequest("Event photo does not exist")

        # Открываем файл с фотографией события и возвращаем его содержимое
        with open(event.photo.path, 'rb') as photo_file:
            return HttpResponse(photo_file.read(), content_type='image/jpeg')


class StudentListView(APIView):
    serializer_class = StudentListSerializer
    # queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = Student.objects.all()
        serializer = StudentListSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)


class StudentMarksListView(viewsets.ModelViewSet):
    serializer_class = StudentListSerializer
    queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        return self.queryset.filter(group_id=group_id)

class StudentMarkDetailView(APIView):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        serializer = MarkSerializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        student_id = self.kwargs.get('pk')

        if isinstance(request.data, list):
            marks = []
            for mark_data in request.data:
                mark_value = mark_data.get('value')
                mark_subject = mark_data.get('subject')
                mark = Mark(value=mark_value, subject=mark_subject)
                mark.save()
                marks.append(mark)

            student = get_object_or_404(Student, id=student_id)
            student.marks.add(*marks)
        else:
            mark_value = request.data.get('value')
            mark_subject = request.data.get('subject')
            mark = Mark(value=mark_value, subject=mark_subject)
            mark.save()
            student = get_object_or_404(Student, id=student_id)
            student.marks.add(mark)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentListSerializer
    queryset = Student.objects.all()

class MarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer


class ScheduleListView(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = SсheduleSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        return self.queryset.filter(schedule_id=group_id)

class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = SсheduleSerializer
    queryset = Schedule.objects.all()