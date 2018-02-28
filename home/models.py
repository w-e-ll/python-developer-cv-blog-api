from django.db import models
from redactor.fields import RedactorField


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Home(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RedactorField()
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # this will be an error in /admin
    # def get_absolute_url(self):
    #    return reverse("page_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "My Home Page"
