
from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('',HotelViewSet.as_view({'get':'list','post':'create'}),name='hotel_list'),
    path('<int:pk>/',HotelViewSet.as_view({'get':'retrieve',
                                             'put':'update',
                                             'delete':'destroy'}),name='hotel_detail'),

    path('users/',UserProfileViewSet.as_view({'get':'list','post':'create'}),name='user_list'),
    path('users<int:pk>/',UserProfileViewSet.as_view({'get':'retrieve',
                                             'put':'update',
                                             'delete':'destroy'}),name='user_detail'),

    path('room', RoomViewSet.as_view({'get': 'list', 'post':'create'}), name = 'room_list'),
    path('room/<int:pk>/', RoomViewSet.as_view({'get': 'retrieve',
                                                    'put': 'update',
                                                    'delete':'destroy'}), name = 'room_detail'),

    path('booking', BookingViewSet.as_view({'get': 'list', 'post':'create'}), name = 'booking_list'),
    path('booking/<int:pk>/', BookingViewSet.as_view({'get': 'retrieve',
                                          'put': 'update',
                                          'delete':'destroy'}), name = 'booking_detail'),

    path('review', ReviewViewSet.as_view({'get': 'list', 'post':'create'}), name = 'review_list'),
    path('review/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve',
                                          'put': 'update',
                                          'delete':'destroy'}), name = 'review_detail'),



]