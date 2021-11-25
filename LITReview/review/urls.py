from django.urls import path

from . import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('logout', views.logout_user, name='logout'),
    path('registration', views.registration, name='registration'),
    path('flux', views.flux, name='flux'),
    path('subscription', views.subscription, name='subscription'),
    path('unsubscribe/<int:followed_user_id>', views.unsubscribe, name='unsubscribe'),
    path('ticket', views.ticket, name='ticket'),
    path('review', views.review, name='review'),
    path('review/<int:ticket_id>', views.review, name='review'),
    path('personal_posts', views.personal_posts, name='personal_posts'),
    path('edit_review', views.edit_review, name='edit_review'),
    path('edit_ticket/<int:ticket_id>', views.edit_ticket, name='edit_ticket'),
]
