import uuid
from django.db import models
from django.utils import timezone
from candidate.models import Candidate
from examiner.models import Examiner


def exam_code():
    return f"CBT--{str(uuid.uuid4())[:8]}"


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Option(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    options = models.ManyToManyField(Option)

    def __str__(self):
        return self.question

    def __str__(self):
        return self.question

    def __str__(self):
        return self.option


class CandidateAttempt(models.Model):
    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  
            if self.selected_option.is_correct:
                self.score += 1
        super(CandidateAttempt, self).save(*args, **kwargs)

class ExamSession(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not started')
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
    ]
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=25, default=exam_code, editable=False, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.PositiveIntegerField(null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    candidate = models.ManyToManyField(Candidate)
    number_of_question = models.PositiveIntegerField()
    pass_mark = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]

    def is_time_limit_exceeded(self):
        if self.quiz.time_limit:
            time_spent = (timezone.now() - self.start_time).total_seconds() / 60
            return time_spent > self.quiz.time_limit
        return False
