from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GRADATION_CHOICES = [
        ('teacher', 'teacher'),
        ('student', 'student')
    ]
    gradation = models.CharField(max_length=20, choices=GRADATION_CHOICES, default='student')

    def __str__(self):
        return f'{self.username}'


class Leaf(models.Model):
    THEORY = 'THEORY'
    PRACTICE = 'PRACTICE'
    PROJECT = 'PROJECT'
    STATUS_CHOICES = [
        (THEORY, 'THEORY'),
        (PRACTICE, 'PRACTICE'),
        (PROJECT, 'PROJECT')
    ]
    name = models.CharField(max_length=63, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    type = models.CharField(max_length=10,choices=STATUS_CHOICES, default=THEORY)


    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('leaf_detail', kwargs={'id': self.id})


class Course(models.Model):

    ONLINE = 'online'
    OFFLINE = 'offline'
    BLENDED = 'blended'
    FORMAT_CHOICES = [
        (ONLINE, 'Online'),
        (OFFLINE, 'Offline'),
        (BLENDED, 'Blended'),
    ]

    UKRAINIAN = 'ru'
    ENGLISH = 'en'
    LANGUAGE_CHOICES = [
        (UKRAINIAN, 'Ukrainian'),
        (ENGLISH, 'English')
    ]

    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    leafs = models.ManyToManyField(Leaf, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=1.00)
    duration_in_days = models.PositiveIntegerField(null=True, blank=True, default=10)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default=ONLINE)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'id': self.id})


class UserCourses(models.Model):
    STARTED = 'ST'
    COMPLETED = 'CP'
    REJECTED = 'RJ'
    STATUS_CHOICES = [
        (STARTED, 'STARTED'),
        (COMPLETED, 'COMPLETED'),
        (REJECTED, 'REJECTED')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STARTED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course'),
        ]

    def save(self, *args, **kwargs):
        logs = CoursesLogs(course=self.course, user=self.user, status=self.status)
        logs.save()
        if self.status == self.COMPLETED:
            diploma = Diplomas(course=self.course, user=self.user)
            diploma.save()
        super().save(*args, **kwargs)


class UserLeaf(models.Model):
    NOT_INTERESTED = 5
    INTERESTED = 1
    LEARNING = 2
    LEARNED = 3
    VALIDATED = 4
    STATUS_CHOICES = [
        (NOT_INTERESTED, 'NOT_INTERESTED'),
        (INTERESTED, 'INTERESTED'),
        (LEARNING, 'LEARNING'),
        (LEARNED, 'LEARNED'),
        (VALIDATED, 'VALIDATED'),

    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    leafs = models.ForeignKey(Leaf, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_INTERESTED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'leafs'], name='unique_user_leaf'),
        ]

    def __str__(self):
        return f'{self.leafs.name}'


class LeafKeypoint(models.Model):
    text = models.CharField(max_length=255)
    leaf = models.ForeignKey(Leaf, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text) + ":  (" + str(self.leaf) + ")"


class Diplomas(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.course.name}'


class CoursesLogs(models.Model):
    STARTED = 'ST'
    COMPLETED = 'CP'
    REJECTED = 'RJ'
    STATUS_CHOICES = [
        (STARTED, 'STARTED'),
        (COMPLETED, 'COMPLETED'),
        (REJECTED, 'REJECTED')
    ]
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.course.name}'
