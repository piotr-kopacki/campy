from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Camera

# Custom Mixins
class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

# Custom Forms
class CustomUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass

class CustomUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass

# Custom Inline editing
class CameraInline(admin.TabularInline):
    model = Camera
    extra = 0

# Register your models here.
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'live')

admin.site.unregister(User)
@admin.register(User)
class EmailRequiredUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = ((None, {
        'fields': ('username', 'email', 'password1', 'password2'), 
        'classes': ('wide',)
    }),)
    inlines = (CameraInline,)

