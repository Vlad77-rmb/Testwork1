from django.db import models
from django.urls import reverse, NoReverseMatch


class MenuItem(models.Model):
    name = models.CharField('Название', max_length=100)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский пункт',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    menu_name = models.CharField('Имя меню', max_length=100)
    url = models.CharField(
        'URL',
        max_length=255,
        blank=True,
        help_text='Можно указать как явный URL (/about/), так и именованный (about)'
    )
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_url(self):
        if not self.url:
            return '#'

        try:
            # Пробуем использовать как именованный URL
            return reverse(self.url)
        except NoReverseMatch:
            # Если не получилось, используем как обычный URL
            return self.url

    def is_active(self, current_path):
        url = self.get_url()
        return url != '#' and current_path.startswith(url)
# Create your models here.
