from django import forms
from django.forms import ModelForm
from .models import Room, Topic, Message, User
from django.contrib.auth.forms import UserCreationForm


class TailwindFormMixin:
    """Apply the shared `.input` component class to every visible widget so
    looped `{{ field }}` rendering matches the hand-written Tailwind inputs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = widget.attrs.get("class", "")
            if isinstance(widget, forms.CheckboxInput):
                continue
            if isinstance(widget, forms.FileInput):
                widget.attrs["class"] = (css + " block w-full text-sm text-gray-600 dark:text-zinc-300").strip()
            else:
                widget.attrs["class"] = (css + " input").strip()


class MyUserCreationForm(TailwindFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(TailwindFormMixin, ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(TailwindFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'name', 'email', 'bio']


class TopicForm(TailwindFormMixin, ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
