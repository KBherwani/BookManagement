from django import forms

from Books.models import Book, Comment


class BooksForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'application/pdf'}))

    class Meta:
        model = Book
        fields = \
            ['name', 'author', 'price', 'founded', 'frontpic', 'short_desc',
             'file']
        widgets = {
            "founded": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},

            )}


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'message',
                'cols': '30',
                'rows': '10',
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['content']
