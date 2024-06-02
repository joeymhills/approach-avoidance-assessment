from django.contrib import admin
from .models import Participant, Trial, Response

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'extra_metadata', 'created_at', 'updated_at')
    search_fields = ('subject_id',)

@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ('block_order', 'block_name', 'stimuli', 'valence', 'random_fixation', 'movement')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('participant', 'trial', 'response_time', 'accuracy')
    search_fields = ('participant__subject_id',)