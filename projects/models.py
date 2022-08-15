from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
def upload_to(instance, filename):
    return 'quiz_pic/{filename}'.format(filename=filename)

class Project(models.Model):
    """
    Used to store AfricaN3 projects.

    """
    title = models.CharField(max_length=20,
                               blank=False,
                               help_text=_("Enter the title of the project "
                                           "you want displayed"),
                               verbose_name=_("Title"))

    description =  models.CharField(max_length=30,
                               blank=False,
                               help_text=_("Enter a short description of the project"),
                               verbose_name=_("Description"))

    image_url = models.ImageField(_("Image"), default='projects/project_default.jpg', upload_to=upload_to)

    project_url = models.URLField(_("Project Link"), blank=True, null=True, help_text=_("A link to get more info about the project"))

    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")