from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import User

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'address', 'phone', 'city']  # Include customer field


class Post_Products_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets={
            'detail':forms.Textarea(
                attrs={
                    'class': 'custom-textarea blur-detail'
                    }),
            'category':forms.SelectMultiple(
                attrs={
                    'class': 'custom-textarea blur-detail'
                    }),
            'price':forms.NumberInput(
                attrs={
                    'class': 'custom-text blur-detail'
                    }),
            'digital':forms.Select(
                choices=[(True, 'Yes'), (False, 'No')],
                attrs={
                    'class': 'custom-text blur-detail','style': 'height:30px'
                    }),
            'seller':forms.Textarea(
                attrs={
                    'class': 'custom-text blur-detail'
                    }),
            'Hotline':forms.Textarea(
                attrs={
                    'class': 'custom-text blur-detail'
                    }), 
            'name':forms.Textarea(
                attrs={
                    'class': 'custom-text blur-detail'
                    }), 
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'custom-file-input',
                    'style': 'border: 2px solid #ffffff; padding: 5px;'
                    })
            }

class Post_Blog(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','image','video','poster','likes']
        widgets={
            'title':forms.TextInput(
                attrs={
                    'class': 'custom-text2 blur-detail'
                    }), 
            'body':forms.Textarea(
                attrs={
                    'class': 'custom-textarea2 blur-detail'
                    }),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'custom-file-input2',
                    'style': 'border: 2px solid #ffffff; padding: 5px;'
                    }),
            'video': forms.ClearableFileInput(
                attrs={
                    'class': 'custom-file-input3',
                    'style': 'border: 2px solid #ffffff; padding: 5px;'
                    })
         }
       


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.post = self.post
        comment.save()

    class Meta:
        model = Comment
        fields = ["body"]



class ReplyForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.parent_comment = kwargs.pop('parent_comment', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        reply = super().save(commit=False)
        reply.author = self.author
        reply.parent_comment = self.parent_comment
        reply.save()

    class Meta:
        model = Reply
        fields = ["content"]
        

   

    