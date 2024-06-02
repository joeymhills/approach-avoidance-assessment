from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegisterParticipantForm
from .models import Participant, Trial, Response
from django.views.decorators.csrf import csrf_exempt
import random

# Register Participant View
def register_participant(request):
    if request.method == 'POST':
        form = RegisterParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return redirect('participant_success', subject_id=participant.subject_id)
    else:
        form = RegisterParticipantForm()
    return render(request, 'register_participant.html', {'form': form})

# Success View after Registration
def participant_success(request, subject_id):
    return render(request, 'participant_success.html', {'subject_id': subject_id})

# Manage Participants View
def manage_participants(request):
    participants = Participant.objects.all()
    return render(request, 'manage_participants.html', {'participants': participants})

# Participant Details View
def participant_detail(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    return render(request, 'participant_detail.html', {'participant': participant})

# Edit Participant View
def edit_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    if request.method == 'POST':
        form = RegisterParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_detail', participant_id=participant.subject_id)
    else:
        form = RegisterParticipantForm(instance=participant)
    return render(request, 'edit_participant.html', {'form': form})

# Delete Participant View
def delete_participant(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    if request.method == 'POST':
        participant.delete()
        return redirect('manage_participants')
    return render(request, 'delete_participant.html', {'participant': participant})

# Start Experiment View
def start_experiment(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    trials = list(Trial.objects.all())
    random.shuffle(trials)

    request.session['participant_id'] = participant.id
    request.session['trials'] = [trial.id for trial in trials]
    request.session['current_trial_index'] = 0

    return redirect('run_trial')

# Run Trial View
def run_trial(request):
    if 'current_trial_index' not in request.session:
        return redirect('start_experiment', participant_id=request.session['participant_id'])

    current_trial_index = request.session['current_trial_index']
    trial_ids = request.session['trials']
    
    if current_trial_index >= len(trial_ids):
        return redirect('experiment_complete')

    trial = get_object_or_404(Trial, id=trial_ids[current_trial_index])
    fixation_time = random.randint(800, 2000)  # Example fixation time
    
    return render(request, 'experiment.html', {'stimulus': trial.stimuli, 'fixation_time': fixation_time})

# Save Response View
@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        participant = get_object_or_404(Participant, id=request.session['participant_id'])
        current_trial_index = request.session['current_trial_index']
        trial_ids = request.session['trials']
        trial = get_object_or_404(Trial, id=trial_ids[current_trial_index])
        
        response_time = float(request.POST['response_time'])
        response_key = request.POST['response_key']

        correct_response = 'Y' if trial.valence == 1 else 'N'
        accuracy = 1 if response_key == correct_response else 0

        Response.objects.create(
            participant=participant,
            trial=trial,
            response_time=response_time,
            accuracy=accuracy
        )
        
        request.session['current_trial_index'] += 1

        return redirect('run_trial')

# Experiment Complete View
def experiment_complete(request):
    return render(request, 'experiment_complete.html')