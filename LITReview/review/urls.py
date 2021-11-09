from django.urls import path

from . import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('logout', views.logout_user, name='logout'),
    path('registration', views.registration, name='registration'),
    path('flux', views.flux, name='flux'),
    path('subscription', views.subscription, name='subscription'),
    path('ticket', views.ticket, name='ticket'),
    path('review', views.review, name='review'),
    path('review_response', views.review_response, name='review response'),
    path('personal_posts', views.personal_posts, name='personal_posts'),
    path('edit_review', views.edit_review, name='edit_review'),
    path('edit_ticket', views.edit_ticket, name='edit_ticket'),
]
