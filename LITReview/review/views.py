from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages

from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm


def connexion(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        infos = {'page_title': 'Connexion', 'form': form}
        return render(request, 'review/connexion.html', infos)
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('flux')
        else:
            messages.error(request, "Utilisateur inexistant ou mot de passe incorrect")
            return redirect('connexion')


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
        tickets_list = []
        for ticket_data in tickets:
            for review_data in reviews:
                if ticket_data.id == review_data.ticket_id:
                    tickets_list.append(ticket_data)
        infos = {'page_title': 'Flux', 'tickets': tickets, 'reviews': reviews, 'tickets_list': tickets_list}
        return render(request, 'review/flux.html', infos)
    else:
        return redirect(connexion)


def subscription(request):
    user = request.user
    if user.is_active:
        if request.method == 'GET':
            form = UserFollowsForm()
            user_follows = UserFollows.objects.filter(user=request.user)
            followers = UserFollows.objects.filter(followed_user=request.user)
            infos = {'page_title': 'Abonnements', 'user_follows': user_follows, 'followers': followers, 'form': form}
            return render(request, 'review/subscription.html', infos)
        elif request.method == 'POST':
            form = UserFollowsForm(request.POST, request.FILES)
            if form.is_valid():
                followed_user = form.cleaned_data['followed_user']
                if followed_user is not None:
                    if user != followed_user:
                        data_check = UserFollows.objects.filter(user=user).filter(followed_user=followed_user)
                        if not data_check:
                            form.instance.user = request.user
                            form.save()
                            messages.success(request, 'Vous êtes maintenant abonné à cet utilisateur')
                            return redirect('subscription')
                        else:
                            messages.error(request, "Vous suivez déjà cet utilisateur")
                            return redirect('subscription')
                    else:
                        messages.error(request, "Vous ne pouvez pas suivre votre propre profil")
                        return redirect('subscription')
                elif followed_user is None:
                    messages.error(request, "Vous devez sélectionner un utilisateur")
                    return redirect('subscription')
    else:
        return redirect(connexion)


def unsubscribe(request, followed_user_id):
    user = request.user
    followed_user = get_object_or_404(User, id=followed_user_id)
    user_follows = UserFollows.objects.filter(followed_user=followed_user).filter(user=user)
    if user_follows:
        user_follows.delete()
    return redirect('subscription')


def ticket(request):
    user = request.user
    if user.is_active:
        if request.method == 'GET':
            form = TicketForm()
            infos = {'page_title': 'Ticket', 'form': form}
            return render(request, 'review/ticket.html', infos)
        elif request.method == 'POST':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.user = user
                form.save()
                return redirect('flux')
    else:
        return redirect(connexion)


def edit_ticket(request, ticket_id):
    user = request.user
    instanced_ticket = Ticket.objects.get(pk=ticket_id)
    if user.is_active:
        if request.method == 'GET':
            form = TicketForm(instance=instanced_ticket)
            infos = {'page_title': 'Ticket', 'form': form, 'instanced_ticket': instanced_ticket}
            return render(request, 'review/edit_ticket.html', infos)
        elif request.method == 'POST':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                data_ticket = Ticket.objects.get(pk=ticket_id)
                data_ticket.title = form.cleaned_data['title']
                data_ticket.description = form.cleaned_data['description']
                if form.cleaned_data['image']:
                    data_ticket.image = form.cleaned_data['image']
                data_ticket.save()
                return redirect('flux')
    else:
        return redirect(connexion)


def delete_ticket(request, ticket_id):
    user = request.user
    data_ticket = Ticket.objects.filter(id=ticket_id).filter(user=user)
    if data_ticket:
        data_ticket.delete()
    return redirect('flux')


def review(request, ticket_id=None):
    user = request.user
    if user.is_active:
        instanced_ticket = Ticket.objects.get(pk=ticket_id) if ticket_id is not None else None
        if instanced_ticket is None:
            if request.method == 'GET':
                ticket_form = TicketForm()
                review_form = ReviewForm()
                infos = {'page_title': 'Review', 'ticket_form': ticket_form, 'review_form': review_form,
                         'range': range(6)}
                return render(request, 'review/review.html', infos)
            elif request.method == 'POST':
                ticket_form = TicketForm(request.POST, request.FILES)
                review_form = ReviewForm(request.POST)
                if ticket_form.is_valid() and review_form.is_valid():
                    ticket_form.instance.user = user
                    ticket_obj = ticket_form.save()
                    review_form.instance.user = user
                    review_form.instance.ticket = Ticket.objects.get(pk=ticket_obj.pk)
                    review_form.save()
                    return redirect('flux')
        else:
            if request.method == 'GET':
                review_form = ReviewForm()
                infos = {'page_title': 'Review', 'instanced_ticket': instanced_ticket, 'review_form': review_form,
                         'range': range(6)}
                return render(request, 'review/review.html', infos)
            elif request.method == 'POST':
                review_form = ReviewForm(request.POST)
                if review_form.is_valid():
                    if review_form.is_valid():
                        review_form.instance.user = request.user
                        review_form.instance.ticket = Ticket.objects.get(pk=ticket_id)
                        review_form.save()
                        return redirect('flux')
    else:
        return redirect(connexion)


def edit_review(request, review_id):
    user = request.user
    instanced_review = Review.objects.get(pk=review_id)
    if user.is_active:
        if request.method == 'GET':
            form = ReviewForm(instance=instanced_review)
            infos = {'page_title': 'Review', 'form': form, 'range': range(6), 'instanced_review': instanced_review}
            return render(request, 'review/edit_review.html', infos)
        elif request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                data_review = Review.objects.get(pk=review_id)
                data_review.headline = form.cleaned_data['headline']
                data_review.body = form.cleaned_data['body']
                data_review.rating = form.cleaned_data['rating']
                data_review.save()
                return redirect('flux')
    else:
        return redirect(connexion)


def delete_review(request, review_id):
    user = request.user
    data_review = Review.objects.filter(id=review_id).filter(user=user)
    if data_review:
        data_review.delete()
    return redirect('flux')


def personal_posts(request):
    user = request.user
    if user.is_active:
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()
        tickets_list = []
        for ticket_data in tickets:
            for review_data in reviews:
                if ticket_data.id == review_data.ticket_id:
                    tickets_list.append(ticket_data)
        data_ticket = Ticket.objects.filter(user=user)
        data_review = Review.objects.filter(user=user)
        infos = {'page_title': 'Posts Personnels', 'data_ticket': data_ticket, 'data_review': data_review,
                 'tickets_list': tickets_list}
        return render(request, 'review/personal_posts.html', infos)
    else:
        return redirect(connexion)
