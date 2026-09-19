from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма публикации."""

    class Meta:
        model = Post
        fields = (
            'title', 'text', 'pub_date', 'category',
            'location', 'image', 'is_published',
        )


class CommentForm(forms.ModelForm):
    """Форма комментария."""

    class Meta:
        model = Comment
        fields = ('text',)
