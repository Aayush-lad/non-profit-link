from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .forms import CustomUserChangeForm, CustomUserCreationForm, LoginRegisterForm
from .models import Item, Org, OrgContactInfo, OrgInfo, OrgLocation


# inlines for Org
class OrgContactInfoInline(admin.TabularInline):
    model = OrgContactInfo


class OrgInfoInline(admin.TabularInline):
    model = OrgInfo


class OrgLocationInline(admin.TabularInline):
    model = OrgLocation


class ItemInline(admin.TabularInline):
    model = Item


# admin registers
@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    inlines = [OrgContactInfoInline, OrgInfoInline, OrgLocationInline, ItemInline]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Org
    ordering = ("-org_name",)


@admin.register(OrgContactInfo)
class OrgContactInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(OrgInfo)
class OrgInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(OrgLocation)
class OrgLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class OrgItemAdmin(admin.ModelAdmin):
    pass
