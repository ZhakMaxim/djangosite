from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from edushedule.models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'login',
            'password',
            'status',
            'student',
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UserAuthorizationSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=128,)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    student = serializers.CharField(read_only=True)
    group = serializers.CharField(read_only=True)
    group_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        login = data['login']
        password = data['password']
        user = authenticate(login=login, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)
            f_user = User.objects.get(login=login)
            validation = {
                 'access': access_token,
                 'refresh': refresh_token,
                 'login': f_user.login,
                 'status': f_user.status,
                 'student': f_user.student.id,
                 'group_id': f_user.student.group_id,
                 'group': f_user.student.group,
                 'name':  f_user.student.name,
            }
            return validation
        except user.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'login',
            'status',
        )

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'photo',
            'description',
            'date',
        )

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = (
            'value',
            'subject',
        )

class StudentListSerializer(serializers.ModelSerializer):
    marks = MarkSerializer(many=True, read_only=True)
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = (
            'id',
            'group_name',
            'name',
            'marks',
        )

    def get_group_name(self, obj):
        return obj.group.name

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name',
        )

class SсheduleSerializer(serializers.ModelSerializer):
    name = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'