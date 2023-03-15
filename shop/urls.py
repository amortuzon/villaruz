from django.urls import path
from . views import *
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('terms/', views.termsPage, name='terms'),

    path('logout/', views.logoutUser, name="logout"),
    path('index/', views.indexPage, name='index'),
    path('', views.dashboardPage, name='dashboard'),
    path('user/', views.userPage, name="user_page"),
    path('profile/', views.profileSettings, name="profile"),
    path('reservation/<str:pk>/', views.createReservation, name='reservation'),
    path('update_reservation/<str:pk>/',
         views.updateReservation, name="update_reservation"),
    path('update_reservationadmin/<str:pk>/',
         views.updateReservationAdmin, name="update_reservationadmin"),
    path('update_message/<str:pk>/',
         views.updatemessage, name="update_message"),
    path('delete_reservation/<str:pk>/',
         views.deleteReservation, name="delete_reservation"),
    path('delete_reservationadmin/<str:pk>/',
         views.deleteReservationAdmin, name="delete_reservationadmin"),
    path('delete_messageadmin/<str:pk>/',
         views.deletemessageAdmin, name="delete_messageadmin"),
    path('delete_customer/<str:pk>/',
         views.deleteCustomer, name="delete_customer"),
    path('about/', views.aboutPage, name='about'),
    path('services/', views.servicesPage, name='services'),
    path('reservations/', views.reservationPage, name='reservations'),

    path('submit_message/<str:pk>/',
         views.submit_message, name='submit_message'),
    path('message_page/', views.messagePage, name='message_page'),
    path('allmessage_page/', views.allmessagePage, name='allmessage_page'),
    path('customer/', views.allCustomers, name='customer'),


    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_change', views.password_change, name='password_change'),

    path('password_reset', views.password_reset_request, name='password_reset'),

    path('reset/<uidb64>/<token>', views.passwordResetConfirm,
         name='password_reset_confirm'),

]
