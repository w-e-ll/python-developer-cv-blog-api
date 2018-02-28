from django.db import models
from django.urls import reverse
from redactor.fields import RedactorField
from django.db.models.signals import pre_save
from blog.utils.unique_slug import unique_slug_generator
from accounts.models import User


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(models.Model):
    user = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True, help_text="Upload your photo for Avatar")
    about = models.TextField()
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blog_posts_author', kwargs={'username': self.user.username})

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.title

    @property
    def get_total_posts(self):
        return Post.objects.filter(tags__pk=self.pk).count()

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    @property
    def get_total_posts(self):
        return Post.objects.filter(categories__pk=self.pk).count()

    def get_absolute_url(self):
        return reverse('blog_posts_category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)


class Post(TimeStampedModel):
    author = models.ForeignKey(on_delete=models.CASCADE, related_name='author_post', to='blog.Author')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    cover = models.ImageField(upload_to='gallery/covers/%Y/%m/%d', null=True, blank=True, help_text='Optional cover post')
    content = RedactorField()
    categories = models.ManyToManyField('Category')
    tags = models.ManyToManyField('Tag')
    keywords = models.CharField(max_length=200, null=True, blank=True, help_text='Keywords sparate by comma.')
    meta_description = models.TextField(null=True, blank=True)
    publish = models.BooleanField(default=True)
    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    @property
    def total_visitors(self):
        return Visitor.objects.filter(post__pk=self.pk).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ["-created"]


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=Post)


class Page(TimeStampedModel):
    author = models.ForeignKey(on_delete=models.CASCADE, related_name='author_page', to='blog.Author')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RedactorField()
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ["-created"]


class Gallery(TimeStampedModel):
    title = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='gallery/attachment/%Y/%m/%d')

    def __str__(self):
        return self.title

    def check_if_image(self):
        if self.attachment.name.split('.')[-1].lower() \
                in ['jpg', 'jpeg', 'gif', 'png']:
            return ('<img height="40" width="60" src="%s"/>' % self.attachment.url)
        return ('<img height="40" width="60" src="/static/icons/file-icon.png"/>')
    check_if_image.short_description = 'Attachment'
    check_if_image.allow_tags = True

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ['-created']


class Visitor(TimeStampedModel):
    post = models.ForeignKey(to='blog.Post', related_name='post_visitor', on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
        ordering = ['-created']
