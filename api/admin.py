from django.contrib import admin
from .models import Candidate, Quiz, Question, Option, Response


# Inline to add options within the question admin interface
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4# Display 2 empty option fields by default


# Inline to add questions within the quiz admin interface


# Admin for Quiz
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
  


# Admin for Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz")
    search_fields = ("text", "quiz__name")
    inlines = [OptionInline]


# Admin for Option
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("text", "is_correct", "question")
    search_fields = ("text", "question__text")


# Admin for Candidate
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone_number")


# Admin for Response
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("candidate", "question", "selected_option")
    search_fields = ("candidate__first_name", "candidate__last_name", "question__text")
