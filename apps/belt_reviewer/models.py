from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "<User: {}{} {}>".format(self.first_name, self.last_name, self.created_at)

class Author(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    uploaded_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "<Author: {} {}>".format(self.name, self.created_at)

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Author, on_delete = None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "<Book: {} {} {}>".format(self.title, self.author, self.created_at)

class Review(models.Model):
    review_des = models.TextField()
    review_rating = models.SmallIntegerField(default = 0)
    book = models.ForeignKey(Book, on_delete = None, related_name = "reviews")
    user = models.ForeignKey(User, on_delete = None, related_name = "users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "<Review: {} {} {}>".format(self.book, self.user, self.created_at)

        
