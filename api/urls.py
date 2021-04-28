from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"projects", views.ProjectViewSet, basename="project")
router.register(r"tickets", views.TicketViewSet, basename="ticket")
router.register(r"ticket-comments", views.TicketCommentViewSet,
                basename="ticket-comment")


urlpatterns = [
    path('current_user/', views.current_user),
    path('user/', views.UserList.as_view())
]

urlpatterns += router.urls
