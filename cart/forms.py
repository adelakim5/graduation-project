from django import forms
from food.models import Food
# from decimal import Decimal
from .models import *

class AddToCartForm(forms.Form):
    # type = forms.ChoiceField(chocies=(
    #     [
    #         ('1', '예약'),
    #         ('2', '대기'),
    #     ]
    # ), initial='1', required=True)
    # # 상품 수량 설정 필드
    quantity = forms.IntegerField(initial=1)
    # # 수정 여부 확인 필드
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    # class Meta:
    #     model = Options
    #     fields = '__all__'






# class ItemToCart(forms.ModelForm):
#     people = forms.DecimalField(default=Decimal(0), max_digits=2, decimal_places=0)
    
#     class Meta:
#         model = Food
#         fields = ('peple', 'price', )
    
#      # price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder':'1인당 최소요청금액을 정해주세요.'}))