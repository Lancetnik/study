from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import NonDeletableUser


class UserCreationForm(forms.ModelForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = NonDeletableUser
        fields = ('login', 'email', 'phone_number', 'is_superuser', 'is_confirmed')


@admin.register(NonDeletableUser)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = list(UserCreationForm._meta.fields)

    detail_list_display = [i.name for i in NonDeletableUser._meta.fields]
    detail_list_display.remove('id')

    ordering = ('email',)
    list_filter = ('email',)

    add_fieldsets = (
        (None, {
            'fields': list_display
        }),
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': detail_list_display
        }),
    )
