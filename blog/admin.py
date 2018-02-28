from django.contrib import admin
from django import forms
# Integrating the model to can import and export the data via admin dashboard.
# See this docs: https://goo.gl/QR3Qqp
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from suit.widgets import AutosizedTextarea
from blog.models import *


class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author


class AuthorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AuthorResource
    list_display = ('user', 'website', 'about')
    search_fields = ['user__username', 'user__email', 'about']
    list_filter = ['user__active', 'user__staff', 'user__admin']


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TagResource
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class TagAdminForm(forms.ModelForm):
    meta_description = forms.CharField(required=False, widget=AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}))

    class Meta:
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()

    def save(self, commit=True):
        post = super(TagAdminForm, self).save(commit=False)
        if commit:
            post.save()

        if post.pk:
            post.tags.set(self.cleaned_data['tags'])
            self.save_m2m()
        return post


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CategoryAdmin(admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdminForm(forms.ModelForm):
    meta_description = forms.CharField(required=False, widget=AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}))

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()

    def save(self, commit=True):
        post = super(CategoryAdminForm, self).save(commit=False)
        if commit:
            post.save()

        if post.pk:
            post.categories.set(self.cleaned_data['categories'])
            self.save_m2m()
        return post


class PostResource(resources.ModelResource):

    class Meta:
        model = Post


class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PostResource
    form = CategoryAdminForm
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'created', 'modified', 'publish')
    search_fields = ['title', 'content', 'author__user__username']
    list_filter = ['publish', 'author__user__username', 'created']


class PageResource(resources.ModelResource):

    class Meta:
        model = Page


class PageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PageResource
    list_display = ('title', 'author', 'created', 'modified', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'author__user__username']
    list_filter = ['publish', 'author__user__username', 'created']
    list_per_page = 20


class GalleryResource(resources.ModelResource):

    class Meta:
        model = Gallery


class GalleryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = GalleryResource
    list_display = ('check_if_image', 'title', 'created', 'modified')
    search_fields = ['title']
    list_filter = ['created']
    list_per_page = 20


class VisitorResource(resources.ModelResource):

    class Meta:
        model = Visitor


class VisitorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VisitorResource
    list_display = ('post', 'ip', 'created', 'modified')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Visitor, VisitorAdmin)
