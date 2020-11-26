from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    REASON=[
        ('no-show', '노쇼'),
        ('accept', '승인'),
        ('cancel', '취소'),
        ('etc', '기타')
    ]
    reason = forms.ChoiceField(widget = forms.RadioSelect, choices=REASON, initial='accept', required=True)
    others = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '집중 고객으로 등록하려는 이유를 자세히 적어주세요.'}))
    
    class Meta:
        model = Customer
        fields = ('reason', 'others')
