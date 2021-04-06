from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Выводит список тем"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

    # Функция получает значение, совпавшее с выражением (?P<topic_id>\d+), и сохраняет его в topic_id:
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    # функция get() используется для получения темы (по аналогии с тем, как мы это делали в оболочке Django)
    topic = Topic.objects.get(id=topic_id)
    # далее загружаются записи, связанные с данной темой, и они упорядочиваются по значению date_added:
    # знак «минус» перед date_added сортирует результаты в обратном порядке,
    # то есть самые последние записи будут находиться на первых местах.
    # Тема и записи сохраняются в словаре context
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    # который передается шаблону topic html
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Определяет новую тему"""
    # Если метод запроса отличен от POST, вероятно, используется запрос GET, поэтому необходимо
    # вернуть пустую форму (даже если это запрос другого типа, это все равно безопасно).
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        # Мы создаем экземпляр TopicForm , сохраняем его в переменной form
        # и отравляем форму шаблону в словаре context
        form = TopicForm()
    # Если используется метод запроса POST, выполняется блок else,
    # который обрабатывает данные, отправленные в форме
    else:
        # Отправлены данные POST; обработать данные.
        # создаем экземпляр TopicForm  и передаем ему данные, введенные пользователем, хранящиеся
        # в request.POST. Возвращаемый объект form содержит информацию, отправленную пользователем.
        form = TopicForm(request.POST)
        # Функция is_valid() проверяет, что все обязательные поля были заполнены
        # (все поля формы по умолчанию являются обязательными), 
        # а введенные данные соответствуют типам полей
        if form.is_valid():
            # Если все данные действительны,можно вызвать метод save()
            form.save()
            # используем вызов reverse() для получения URL-адреса страницы topics и передаем
            # его функции HttpResponseRedirect(), перенаправляющей браузер пользователя на страницу topics.
            # На этой странице пользователь видит только что введенную им тему в общем списке тем
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    # мы получаем объект записи, который пользователь хочет изменить, и тему, связанную с этой записью.
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # в блоке if создается экземпляр EntryForm с аргументом instance=entry
    # Этот аргумент приказывает Django создать форму, заранее заполненную информацией из существующего объекта записи.
    # Пользователь видит свои существующие данные и может отредактировать их.
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # При обработке запроса POST передаются аргументы instance = entry и data=request.POST,
        # чтобы приказать Django создать экземпляр формы на основании информации существующего объекта записи,
        # обновленный данными из request.POST. 
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        # Если данные корректны, следует вызов save() без аргументов
        if form.is_valid():
            form.save()
        # Далее происходит перенаправление на страницу темы,
        # и пользователь видит обновленную версию отредактированной им записи.
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)