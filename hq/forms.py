from django.db.models.fields import DateTimeField
from django import forms
from django.forms import ModelForm, TextInput
from django.forms.fields import ChoiceField
from django.forms.models import ModelChoiceField, inlineformset_factory
from django.forms.widgets import DateInput, RadioSelect, Select, Textarea, TimeInput
from .models import *
from dal import autocomplete


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body','author','category', 'image')
        widgets = {
            'title': TextInput(attrs={'placeholder': '○○を手放しいたします。','style':"width: 100%;" }),
            'body': Textarea(attrs={'placeholder': '本文の内容','style':"width: 100%;" }),
            'author': TextInput(attrs={'type': 'hidden', 'value':'','id': 'author_id' }),
        }
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "タイトル"
        self.fields['body'].label = "本文"
        self.fields['category'].label = "カテゴリー別"

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields =['comment']
        widgets = {
            'comment': Textarea(attrs={'placeholder': '○○時に頂きたいですが…','style':"width: 100%;",'rows':4,}),
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = "コメント"

FACILITY_CHOICES = [
    ('三重大','三重大'),
    ('津駅','津駅'),
    ('',''),
]

class BookForm1(ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'email', 'phone', 'date', 'time', 'facility', )
        required = (
            # 'phone',
        )
        widgets = {
            'name': TextInput(attrs={'type': 'hidden', 'value':'','id': 'author_id', 'name':'name'}),
            'email': TextInput(attrs={'type': 'hidden', 'value':'','id': 'email_id', 'name':'email' }),
            'phone': TextInput(attrs={'type': 'hidden', 'value':'','id': 'phone_id', 'name':'phone' }),
            'date': DateInput(attrs={'type':'date', 'name':'date'}),
            'time': TimeInput(attrs={'type':'time', 'name':'time'}),
            'facility': Select(choices=FACILITY_CHOICES, attrs={'name':'time'}),
        }
    def __init__(self, *args, **kwargs):
        super(BookForm1, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['email'].label = ""
        self.fields['phone'].label = ""
        self.fields['date'].label = "日付"
        self.fields['time'].label = "時間帯"
        self.fields['facility'].label = "センター"

class BookSearchForm(ModelForm):
    name = ModelChoiceField(queryset=Book.objects.all())
    
    class Meta:
        model = Book
        fields = ['name','email', 'date', 'facility']
        
        widgets = {
            'name': TextInput(attrs={'name':'name'}),
            'email': TextInput(attrs={'name':'email' }),
            'date': DateInput(attrs={'type':'date', 'name':'date'}),
            'facility': Select(choices=FACILITY_CHOICES, attrs={'name':'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['email'].required = False
        self.fields['date'].required = False
        self.fields['facility'].required = False

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('__all__')
        widgets = {
            'name': autocomplete.ModelSelect2(url='customuser-autocomplete'),
        }


class CheckoutForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('__all__')
        widgets = {
            'street_address': TextInput(attrs={'placeholder':'三重大学'}),
            'apartment_address': TextInput(attrs={'placeholder':'寄宿舎B'}),
            'zip': TextInput(attrs={'placeholder':'514-0001', 'class':'form-control'}),
            # 'same_billing_address': forms.BooleanField(label= "請求書と同一住所",required=False),
            # 'save_info': forms.BooleanField(label= "住所記録", required=False),
        }
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['street_address'].label = "都道府県・市町村"
        self.fields['apartment_address'].label = "建物名"
        self.fields['zip'].label = "郵便番号"
        self.fields['payment_option'].label = "決済方法"