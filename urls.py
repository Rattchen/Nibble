from django.urls import path
from .views import IndexView, BoardView,CardView, Profileiew

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('board/', IndexView.as_view(), name='board_nothing'),
    path('board/<int:pk>', BoardView.as_view(), name='board'),
]