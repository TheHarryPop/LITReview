from django.forms import forms, ModelForm
from .models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre du livre :', 'description': 'Description :', 'image': 'Couverture :'}


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        labels = {'headline': 'Titre de la critique :', 'body': 'Critique :', 'rating': 'Note :'}
