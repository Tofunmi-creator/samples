from django import forms 
from django.forms import ModelForm, Form


class bookinfo(Form):
    topic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter the name of a topic here'}), required=False)
    book_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter the name of a book here'}), required=False)
    class Meta:                
        fields = ('topic','book_name')
    

class topicsn(Form):
    topic_sn= forms.IntegerField(required=False)
    
    class Meta:                
        fields = ('topic_sn',)
        
    def __init__(self, *args, **kwargs ):
        super(topicsn, self).__init__(*args, **kwargs)
        self.fields['topic_sn'].label='Topic Serial Number'
        self.fields['topic_sn'].widget.attrs['class']='form-control'
        self.fields['topic_sn'].widget.attrs['placeholder']='enter topic serial number here'