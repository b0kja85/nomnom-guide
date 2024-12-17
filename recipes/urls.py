from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name="recipes-home"),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name="recipes-detail"),
    path('recipe/create', views.RecipeCreateView.as_view(), name="recipes-create"),
    path('recipe/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipes-update"),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),

    # Voting URLs
    path('recipe/<int:pk>/upvote/', views.upvote_recipe, name="upvote-recipe"),
    path('recipe/<int:pk>/downvote/', views.downvote_recipe, name="downvote-recipe"),
]