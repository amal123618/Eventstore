from django.urls import path
from eventmanagement import views


urlpatterns = [
  path('event/<int:event_id>/', views.event_dashboard, name='event_dashboard'),
  path('event/create/', views.create_event, name='create_event'),
  path('event/<int:event_id>/add-guest/', views.add_guest, name='add_guest'),
  path('rsvp/<uuid:token>/', views.guest_rsvp, name='guest_rsvp'),

]
