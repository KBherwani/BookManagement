from django.core.validators import MinValueValidator
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Add new Book models.
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(1,
                    message="Price cannot be 0 or any negative value")])
    founded = models.DateField()
    frontpic = models.ImageField()
    short_desc = models.TextField(max_length=300)
    file = models.FileField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, related_name='comment_content',
                             on_delete=models.CASCADE)
    content = models.TextField()

#
# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, related_name='replies',
#                                 on_delete=models.CASCADE)
#     book = models.ForeignKey(Book,on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     reply = models.TextField()
#
#     @property
#     def get_replies(self):
#         return self.replies.all()
