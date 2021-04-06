from django import forms
from .models import Topic, Entry

    # определяется класс с именем TopicForm, наследующий от forms.
    # ModelForm. Простейшая версия ModelForm состоит из вложенного класса Meta,
    # который сообщает Django, на какой модели должна базироваться форма
    # и какие поля на ней должны находиться
class TopicForm(forms.ModelForm):
    class Meta:
        # форма создается на базе модели Topic, а на ней размещается только поле text
        model = Topic
        # Код приказывает Django не генерировать подпись для текстового поля:
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # Включая атрибут widgets, вы можете переопределить виджеты,
        # выбранные Django по умолчанию. Приказывая Django использовать элемент forms.
        # Textarea, мы настраиваем виджет ввода для поля 'text', чтобы ширина текстовой
        # области составляла 80 столбцов вместо значения по умолчанию 40
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}