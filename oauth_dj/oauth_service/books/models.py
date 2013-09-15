from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()

    def __unicode__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)
    outline = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User)
    authors = models.ManyToManyField(Author)

    def __unicode__(self):
        return self.title

    @staticmethod
    def get_book_list(user, page_no, num_per_page):
        books = Book.objects.filter(users__id=user.pk)
        pages = Paginator(books, per_page=num_per_page)
        try:
            return pages.page(page_no)
        except PageNotAnInteger:
            return pages.page(1)
        except EmptyPage:
            return pages.page(pages.num_pages)
