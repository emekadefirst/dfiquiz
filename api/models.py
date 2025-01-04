from django.db import models


class Candidate(models.Model):
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

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    passed = models.PositiveIntegerField()
    failed = models.PositiveIntegerField()
    overall =  models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.overall = self.passed + self.failed
        super().save(*args, **kwargs)
