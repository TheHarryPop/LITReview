from django.forms import ModelForm
from .models import Ticket, Review, UserFollows


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


class UserFollowsForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        labels = {'followed_user': "Nom d'utilisateur :"}

