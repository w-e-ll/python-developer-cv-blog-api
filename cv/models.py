from django.db import models
from accounts.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile_author', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatar')
    job_name = models.CharField(max_length=200)
    detail_profile = models.TextField()
    repository = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=200)
    # my stuff
    debian = models.URLField()
    python = models.URLField()
    postgresql = models.URLField()
    bootstrap = models.URLField()
    # iframe_maps = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class News(models.Model):
    profile = models.ForeignKey(on_delete=models.CASCADE, related_name='news', to='cv.Profile')
    new_name = models.CharField(max_length=200)
    new_link = models.URLField()
    new_detail = models.CharField(max_length=200)
    new_detail_name = models.CharField(max_length=200)
    when_it_was_happend = models.CharField(max_length=100)


class Main_Qualifications(models.Model):
    profile = models.ForeignKey(on_delete=models.CASCADE, related_name='main_qualifications', to='cv.Profile')
    skill_name = models.CharField(max_length=200, null=True, blank=True)
    skill_detail_first_part = models.CharField(max_length=200)
    skill_detail_second_part = models.CharField(max_length=200)


class Job_Experience(models.Model):
    profile = models.ForeignKey(on_delete=models.CASCADE, related_name='job_experience', to='cv.Profile')
    profession_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_site = models.URLField()
    when_it_was_happend = models.CharField(max_length=100)
    job_detail = models.CharField(max_length=1000)


class Education(models.Model):
    profile = models.ForeignKey(on_delete=models.CASCADE, related_name='education', to='cv.Profile')
    when_it_was_happend = models.CharField(max_length=100)
    detail_education = models.CharField(max_length=200)
    education_name = models.CharField(max_length=200)


class Side_Projects(models.Model):
    profile = models.ForeignKey(on_delete=models.CASCADE, related_name='side_projects', to='cv.Profile')
    project_name = models.CharField(max_length=200)
    project_link = models.URLField()
    project_link_name = models.CharField(max_length=200)
    project_detail = models.CharField(max_length=200)
