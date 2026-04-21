from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Теги',
    )

    class Meta:
        model = Post
        fields = ('title', 'cover_image', 'body', 'tags', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок посту...'}),
            'body': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Напишіть свій пост...'}),
        }
        labels = {
            'title': 'Заголовок',
            'cover_image': 'Обкладинка',
            'body': 'Текст',
            'status': 'Статус',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Залишити коментар...',
            }),
        }
        labels = {'body': ''}
