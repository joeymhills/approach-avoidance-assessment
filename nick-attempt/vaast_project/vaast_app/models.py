from django.db import models

class Participant(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    extra_metadata = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Participant {self.subject_id}"


class Trial(models.Model):
    block_order = models.IntegerField()  # e.g., 1 = compatible first, 2 = incompatible first
    block_name = models.CharField(max_length=50)
    stimuli = models.CharField(max_length=255)
    valence = models.IntegerField()  # e.g., 1 = positive, 2 = negative
    random_fixation = models.IntegerField()  # e.g., random fixation time in ms
    movement = models.IntegerField()  # e.g., 1 = approach, 2 = avoidance

    def __str__(self):
        return f"Trial {self.id}: {self.stimuli}"


class Response(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE)
    response_time = models.FloatField()  # e.g., response time in ms
    accuracy = models.IntegerField()  # 1 = correct, 0 = incorrect

    def __str__(self):
        return f"Response {self.id} by Participant {self.participant.subject_id}"