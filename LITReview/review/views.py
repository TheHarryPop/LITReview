from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse

from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('flux')
            else:
                pass
                # message d'erreur de mot de passe ou utilisateur inexistant
    else:
        form = AuthenticationForm()
    infos = {'page_title': 'Connexion', 'form': form}
    return render(request, 'review/connexion.html', infos)


def logout_user(request):
    logout(request)
    return redirect(reverse(connexion))


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('logout')
    else:
        form = UserCreationForm()
    infos = {'page_title': 'Registration', 'form': form}
    return render(request, 'review/registration.html', infos)


def flux(request):
    user = request.user
    if user.is_active:
        tickets = Ticket.objects.all()

        reviews = Review.objects.all()

        infos = {'page_title': 'Flux', 'tickets': tickets, 'reviews': reviews}
        return render(request, 'review/flux.html', infos)
    else:
        return redirect(connexion)


def subscription(request):
    infos = {'page_title': 'Subscription'}
    return render(request, 'review/subscription.html', infos)


def ticket(request):
    user = request.user
    if user.is_active:
        if request.method == 'GET':
            form = TicketForm()
            infos = {'page_title': 'Ticket', 'form': form}
            return render(request, 'review/ticket.html', infos)
        elif request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                obj = form.save()
                obj.user = user
                obj.save()
                return redirect('flux')
    else:
        return redirect(connexion)


def review(request):
    user = request.user
    if user.is_active:
        if request.method == 'GET':
            form = ReviewForm()
            infos = {'page_title': 'Review', 'form': form}
            return render(request, 'review/review.html', infos)
        elif request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                obj = form.save()
                obj.user = user
                obj.save()
                return redirect('flux')
    else:
        return redirect(connexion)


def review_response(request, ticket_id):
    instance_ticket = Ticket.objects.get(pk=ticket_id)
    form = ReviewForm(ticket=instance_ticket)
    infos = {'page_title': 'Review Response', 'form': form}
    return render(request, 'review/review_response.html', infos)


def personal_posts(request):
    return HttpResponse("Personal posts")


def edit_review(request, review_id):
    return HttpResponse("Edit review %s" % review_id)


def edit_ticket(request, ticket_id):
    return HttpResponse("Edit ticket %s" % ticket_id)