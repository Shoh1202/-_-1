from django.db import models


class PerevalAdded(models.Model):
    beauty_title = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField()

    user_email = models.EmailField()
    user_fam = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_otc = models.CharField(max_length=255, blank=True)
    user_phone = models.CharField(max_length=50)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    height = models.IntegerField()

    winter = models.CharField(max_length=20, blank=True)
    summer = models.CharField(max_length=20, blank=True)
    autumn = models.CharField(max_length=20, blank=True)
    spring = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.beauty_title}{self.title}'


class PerevalImage(models.Model):
    pereval = models.ForeignKey(
        PerevalAdded,
        on_delete=models.CASCADE,
        related_name='images'
    )
    data = models.TextField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title