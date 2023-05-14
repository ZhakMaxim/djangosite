from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, login, password, student, status, **kwargs):
        user = self.model(
            login=login,
            password=password,
            student=student,
            status=status,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'edushedule'
    login = models.CharField(max_length=255, unique=True)
    STATUS_CHOICES = (
        ("teacher", "учитель"),
        ("admin", "администрация"),
        ("student", "ученик"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    student = models.ForeignKey('Student', on_delete=models.DO_NOTHING)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login

    def get_full_name(self):
        return self.login

class Mark(models.Model):
    value = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.subject

class Student(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=255)
    marks = models.ManyToManyField(Mark)
    group = models.ForeignKey('Group', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(default=None, null=True)
    description = models.CharField(max_length=5000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    day_of_week = models.CharField(max_length=50)
    start_time = models.CharField(max_length=6)
    end_time = models.CharField(max_length=6)
    class_name = models.CharField(max_length=100)
    classroom = models.IntegerField()
    schedule = models.ForeignKey('Group', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.class_name

class Group(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name