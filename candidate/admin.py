from django.contrib import admin
from .models import Candidate


class CandidateAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "full_name", "candidate_id", "email", "is_active"]
    search_fields = ["username", "full_name", "candidate_id", "email"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    ordering = ["username"]


admin.site.register(Candidate, CandidateAdmin)
