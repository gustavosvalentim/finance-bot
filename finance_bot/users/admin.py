from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.forms import ValidationError

from finance_bot.users.models import User, UserInteraction


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm

    readonly_fields = ('date_joined', 'last_login',)
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name', 'phone',)

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',)}),
    )

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
        ("Personal info", {'fields': ('first_name', 'last_name', 'phone',)}),
        ("Permissions", {'fields': ('is_active', 'is_superuser',)}),
    ]

    ordering = ('email',)

    inlines = []


class CustomUserInteractionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('user', 'interaction_type', 'interaction_data', 'created_at')
    search_fields = ('user__username', 'interaction_type', 'parent')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserInteraction, CustomUserInteractionAdmin)

admin.site.unregister(Group)
