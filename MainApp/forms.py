from django.forms import ModelForm, Textarea, TextInput, IntegerField
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code']
        labels = {
            "name": "", "lang": ""
        }
        widgets = {
            'name': TextInput(attrs={"class":"red", "placeholder": "Название"})
        }
