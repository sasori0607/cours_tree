from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GRADATION_CHOICES = [
        ('teacher', 'Учитель'),
        ('student', 'Ученик')
    ]
    gradation = models.CharField(max_length=20, choices=GRADATION_CHOICES, default='student')

    def __str__(self):
        return f'{self.username}'


class Leaf(models.Model):
    name = models.CharField(max_length=63, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=1)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('leaf_detail', kwargs={'id': self.id})


class Course(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    leafs = models.ManyToManyField(Leaf, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=1)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'id': self.id})


class UserCourses(models.Model):
    STARTED = 'ST'
    COMPLETED = 'CP'
    REJECTED = 'RJ'
    STATUS_CHOICES = [
        (STARTED, 'Начат'),
        (COMPLETED, 'Закончен'),
        (REJECTED, 'Отказано')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STARTED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course'),
        ]


class UserLeaf(models.Model):
    STARTED = 'ST'
    COMPLETED = 'CP'
    REJECTED = 'RJ'
    STATUS_CHOICES = [
        (STARTED, 'Начат'),
        (COMPLETED, 'Закончен'),
        (REJECTED, 'Отказано')

    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    leafs = models.ForeignKey(Leaf, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STARTED)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'leafs'], name='unique_user_leaf'),
        ]



class LeafKeypoint(models.Model):
    text = models.CharField(max_length=255)
    leaf = models.ForeignKey(Leaf, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text) + ":  (" + str(self.leaf) + ")"