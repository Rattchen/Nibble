from django.urls import path
from .views import IndexView, BoardView,CardView, ProfileDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('board/', IndexView.as_view(), name='board_nothing'),
    path('board/<int:pk>', BoardView.as_view(), name='board'),
    path('card/<int:pk>', CardView.as_view(), name='card'),
    path('profile/<str:handle>', ProfileDetailView.as_view(), name='profile'),
]