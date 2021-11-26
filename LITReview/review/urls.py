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
    path('edit_ticket/<int:ticket_id>', views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>', views.delete_ticket, name='delete_ticket'),
    path('review', views.review, name='review'),
    path('review/<int:ticket_id>', views.review, name='review'),
    path('edit_review/<int:review_id>', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>', views.delete_review, name='delete_review'),
    path('personal_posts', views.personal_posts, name='personal_posts'),


]
