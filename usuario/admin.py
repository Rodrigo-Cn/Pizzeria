from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'nome', 'cpf', 'telefone', 'tipo', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'nome', 'cpf', 'telefone', 'tipo', 'email')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'nome', 'cpf', 'telefone', 'tipo', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'tipo',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf', 'telefone', 'tipo', 'email')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions',)}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'nome', 'cpf', 'telefone', 'tipo', 'email', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ('username', 'nome', 'cpf', 'telefone', 'email',)
    ordering = ('username',)

# Unregister the original User admin if needed
from django.contrib.auth import get_user_model
admin.site.unregister(get_user_model())
admin.site.register(CustomUser, CustomUserAdmin)
