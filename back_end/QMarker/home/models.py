from django.db import models

class Questions(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    mark = models.FloatField()

    def __str__(self):
        return self.question


class MarkingAlgo(models.Model):
    qId = models.IntegerField()
    mark = models.FloatField()
    point = models.FloatField()
    system = models.IntegerField()
    teacher_avg = models.FloatField()
    weight = models.IntegerField()


    def __str__(self):
        return self.qId
