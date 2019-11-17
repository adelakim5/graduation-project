from django import forms
from .models import *
from decimal import Decimal
from django.core.validators import MinValueValidator
# from ckeditor.fields import RichTextField
# from ckeditor.widgets import CKEditorWidget


class FoodPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'식당 이름'}))
    image = forms.ImageField(widget=forms.FileInput())
    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex. 한식, 중식, 일식, 양식 등 대분류를 적어주세요.'}))
    category2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex. 피자, 닭갈비, 고기구이, 찌개 등 소분류를 적어주세요.'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'간단한 소개글 한 줄 적어주세요.'}))
    price = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={'placeholder':'1인당 최소요청금액을 정해주세요.'}))
    body =  forms.CharField(widget=forms.Textarea(attrs={'placeholder':'식당 정보, 예약시간, 예약금액 등 상세정보를 적어주세요.'}))

    class Meta:
        model = Food
        fields = ('title','image','category','category2','description','price','body', )
        

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )

