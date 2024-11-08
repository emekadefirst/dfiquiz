from django.contrib import admin
from .models import Quiz, Question, Option, CandidateAttempt, ExamSession


class QuizAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "examiner", "created_at"]
    search_fields = ["name", "examiner__name"]
    list_filter = ["created_at", "examiner"]
    ordering = ["created_at"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "quiz", "question"]
    search_fields = ["question", "quiz__name"]
    list_filter = ["quiz"]


class OptionAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "option", "is_correct"]
    search_fields = ["option", "question__question"]
    list_filter = ["is_correct"]


class CandidateAttemptAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "question", "selected_option", "score"]
    search_fields = ["candidate__name", "question__question"]
    list_filter = ["score"]


class ExamSessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "start_time",
        "end_time",
        "quiz",
        "number_of_question",
        "pass_mark",
    ]
    search_fields = ["code", "quiz__name"]
    list_filter = ["start_time", "quiz"]
    ordering = ["-start_time"]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(CandidateAttempt, CandidateAttemptAdmin)
admin.site.register(ExamSession, ExamSessionAdmin)
