from django.forms import forms, ModelForm
from .models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre :', 'description': 'Description :', 'image': 'Couverture :'}


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        labels = {'headline': 'Titre :', 'body': 'Critique :', 'rating': 'Note :'}
