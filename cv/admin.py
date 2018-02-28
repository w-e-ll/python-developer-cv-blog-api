from django.contrib import admin
from . models import *


class Main_Qualifications_Admin(admin.TabularInline):
    model = Main_Qualifications
    extra = 1


class News_Admin(admin.TabularInline):
    model = News
    extra = 1


class Side_Projects_Admin(admin.TabularInline):
    model = Side_Projects
    extra = 1


class Job_Experience_Admin(admin.TabularInline):
    model = Job_Experience
    extra = 1


class Education_Admin(admin.TabularInline):
    model = Education
    extra = 1


class Profile_Admin(admin.ModelAdmin):
    inlines = [Main_Qualifications_Admin,
               Job_Experience_Admin,
               Education_Admin,
               News_Admin,
               Side_Projects_Admin,
               # Portfolio_Admin,
               # Skills_Admin
               ]
    save_on_top = True

    def has_add_permission(self, request):
        count = Profile.objects.all().count()
        if count == 0:
            return True
        return False


admin.site.register(Profile, Profile_Admin)
