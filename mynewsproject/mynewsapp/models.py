from django.db import models

class NewsArticle(models.Model):
    publication_date = models.DateField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    news_link = models.URLField()

    class Meta:
        verbose_name = "Статья новостей"  # Измените имя модели на "Статья новостей"

    def __str__(self):
        return self.title

