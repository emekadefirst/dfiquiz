from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Candidate, Quiz, Question, Option, Response, Result, Session


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  #


# Admin for Quiz
@admin.register(Quiz)
class QuizAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# Admin for Question
@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("text", "quiz")
    search_fields = ("text", "quiz__name")
    inlines = [OptionInline]


# Admin for Option
@admin.register(Option)
class OptionAdmin(ModelAdmin):
    list_display = ("text", "is_correct", "question")
    search_fields = ("text", "question__text")


# Admin for Candidate
@admin.register(Candidate)
class CandidateAdmin(ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone_number")


# Admin for Response
@admin.register(Response)
class ResponseAdmin(ModelAdmin):
    list_display = ("candidate", "question", "selected_option")
    search_fields = ("candidate__first_name", "candidate__last_name", "question__text")


# Admin for Result
@admin.register(Result)
class ResultAdmin(ModelAdmin):
    list_display = ("id", "candidate_name", "session_code", "quiz_name", "score")
    search_fields = ("candidate__first_name", "candidate__last_name", "quiz__name")
    list_filter = ("quiz",)

    def candidate_name(self, obj):
        return f"{obj.candidate.first_name} {obj.candidate.last_name}"

    candidate_name.short_description = "Candidate"

    def quiz_name(self, obj):
        return obj.quiz.name

    quiz_name.short_description = "Quiz"


# Inline for candidates in Session
class CandidateInline(admin.TabularInline):
    model = Session.candidates.through
    extra = 1
    verbose_name = "Candidate"
    verbose_name_plural = "Candidates"


# Admin for Session
@admin.register(Session)
class SessionAdmin(ModelAdmin):
    list_display = (
        "id",
        "quiz_name",
        "code",
        "number_of_question",
        "start_time",
        "end_time",
        "created_at",
    )
    search_fields = ("quiz__name", "code")
    list_filter = ("quiz", "created_at")
    inlines = [CandidateInline]

    def quiz_name(self, obj):
        return obj.quiz.name

    quiz_name.short_description = "Quiz"

    def get_queryset(self, request):
        # Ensure we prefetch related fields for better performance
        return (
            super()
            .get_queryset(request)
            .select_related("quiz")
            .prefetch_related("candidates")
        )
