from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import DreamEntry
from .forms import DreamEntryForm


@login_required
def dream_list(request):
    dreams = DreamEntry.objects.filter(user=request.user)

    return render(request, 'dreams/dream_list.html', {
        'dreams': dreams
    })


@login_required
def dream_create(request):
    if request.method == 'POST':
        form = DreamEntryForm(request.POST)

        if form.is_valid():
            dream = form.save(commit=False)
            dream.user = request.user
            dream.save()
            form.save_m2m()

            messages.success(request, 'Dream entry saved successfully.')
            return redirect('dream_list')
    else:
        form = DreamEntryForm()

    return render(request, 'dreams/dream_form.html', {
        'form': form,
        'page_title': 'Record a Dream'
    })


@login_required
def dream_update(request, pk):
    dream = get_object_or_404(
        DreamEntry,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = DreamEntryForm(request.POST, instance=dream)

        if form.is_valid():
            form.save()
            messages.success(request, 'Dream entry updated successfully.')
            return redirect('dream_list')
    else:
        form = DreamEntryForm(instance=dream)

    return render(request, 'dreams/dream_form.html', {
        'form': form,
        'page_title': 'Edit Dream'
    })


@login_required
def dream_delete(request, pk):
    dream = get_object_or_404(
        DreamEntry,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        dream.delete()
        messages.success(request, 'Dream entry deleted successfully.')
        return redirect('dream_list')

    return render(request, 'dreams/dream_confirm_delete.html', {
        'dream': dream
    })