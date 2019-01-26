from django.db import models


class Analysis(models.Model):
    id = models.Index
    text = models.CharField(max_length=30)
    mean = models.FloatField(default=0)
    median = models.FloatField(default=0)
    worst = models.FloatField(default=0)
    best = models.FloatField(default=0)
    std = models.FloatField(default=0)
    date_of_analysis = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class AnalysisPending(models.Model):
    id = models.Index
    text = models.CharField(max_length=30)
    date_of_submitting = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class OneDayResult(models.Model):
    date = models.DateField()
    mean = models.FloatField(default=0)
    median = models.FloatField(default=0)
    worst = models.FloatField(default=0)
    best = models.FloatField(default=0)
    std = models.FloatField(default=0)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)


class TwitterAuth(models.Model):
    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    access_token_secret = models.CharField(max_length=200)
    error = models.CharField(max_length=200, null=True, blank=False)
