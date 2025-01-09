from django.db import models
import random
import string
from django.utils.timezone import now

class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )

    def __str__(self):
        return self.text


class Response(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Check if the selected option is correct, and update the count accordingly
        if self.selected_option.is_correct:
            self.count = 1  # Correct option, set count to 1
        else:
            self.count = 0  # Incorrect option, set count to 0
        super().save(*args, **kwargs)  # Call the parent save method to persist the instance

    class Meta:
        unique_together = ("candidate", "question")

    def __str__(self):
        return f"{self.candidate} - {self.question} - {self.selected_option} - Correct: {self.count}"


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    candidates = models.ManyToManyField(Candidate)
    code = models.CharField(max_length=15, null=True, unique=True, blank=True)
    number_of_question = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.quiz if self.quiz else 'No Quiz'}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        """Generate a unique 10-character alphanumeric code."""
        while True:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not Session.objects.filter(code=code).exists():
                return code


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    session_code = models.ForeignKey(Session, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()


