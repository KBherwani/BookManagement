from django.urls import path
from Books.views import *

app_name = "book"

urlpatterns = [
    path('add/', add_book.as_view(), name="addbook"),
    path('', BookList.as_view(), name="booklist"),
    path("update/<int:pk>/", UpdateBook.as_view(), name="updateBook"),
    path("<int:pk>/", BookDetailView.as_view(), name="detailView"),




]
