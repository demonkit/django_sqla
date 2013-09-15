# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from books.models import Book
from utils.decorators import check_user


@login_required
@check_user
def index(request, user, num_per_page=1, page_no=20):
    books = Book.get_book_list(user, page_no=page_no, num_per_page=num_per_page)
    return render_to_response("index.html", context_instance=RequestContext(request, {"books": books}))
