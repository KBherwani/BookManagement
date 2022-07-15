import operator
from functools import reduce

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, \
    DetailView, FormView, ListView
from Books.forms import BooksForm, CommentForm
from Books.models import Book
from django.db.models import Q
from django.core.paginator import Paginator

from order.models import Cart, CartItem


class add_book(CreateView):
    form_class = BooksForm
    template_name = "addbook.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def form_invalid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.save()
        return redirect("book:booklist")


class BookList(ListView):
    paginate_by = 4
    template_name = "book_list.html"
    model = Book

    def get_context_data(self, **kwargs):

        context = super(BookList, self).get_context_data()
        search_keyword = self.request.GET.get('search')
        search_filter = ''
        if search_keyword:
            search_filter = Q(name__icontains=self.request.GET.get('search'))

        if self.request.GET.get('sort') == 'name':
            order = 'name'

        elif self.request.GET.get('sort') == 'price':
            order = 'price'

        elif self.request.GET.get('sort') == 'auth':
            order = '-author'
        else:
            order = '-id'
        if search_filter:
            books = Book.objects.filter(search_filter).order_by(order)
        else:
            books = Book.objects.order_by(order)
        paginator = Paginator(books, self.paginate_by)
        page_number = self.request.GET.get('page')
        books = paginator.get_page(page_number)

        cart_count = CartItem.objects.filter(cart=Cart.objects.get(user = self.request.user)).count() if Cart.objects.filter(user = self.request.user).exists() else 0
        context['books'] = books
        context['cart_count'] = cart_count
        return context


class UpdateBook(UpdateView):
    form_class = BooksForm
    model = Book
    template_name = "updateBook.html"
    success_url = reverse_lazy("book:booklist")

    def get(self, request, *args, **kwargs):
        class_obj = get_object_or_404(Book, id=kwargs.get('pk'))
        form = BooksForm(instance=class_obj)
        context = {}
        context["form"] = form
        context["data"] = class_obj
        'book:booklist'
        return render(request, self.template_name, context)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(UpdateBook, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        return super(UpdateBook, self).form_invalid(form)


class BookDetailView(DetailView):
    model = Book
    template_name = "DetailView.html"

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        cart_count = CartItem.objects.filter(cart=Cart.objects.get(user = self.request.user)).count() if Cart.objects.filter(user = self.request.user).exists() else 0

        comment = CommentForm()
        context = {}
        context["book"] = book
        context["comment"] = comment
        context["cart_count"] = cart_count

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        obj = form.save(commit=False)
        obj.book = self.get_object()
        obj.timestamp = timezone.now()
        obj.save()
        return self.get(request)

