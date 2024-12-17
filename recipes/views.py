from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models
from django.db.models import Q

class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    paginate_by = 5  # Show 5 recipes per page

    def get_queryset(self):
        """
        Filter recipes based on the search query and sorting order.
        """
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort', 'newest')  

        queryset = models.Recipe.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        # Apply sorting
        if sort == 'oldest':
            queryset = queryset.order_by('created_at')  
        elif sort == 'most_upvotes':
            queryset = queryset.order_by('-upvotes')  
        elif sort == 'most_downvotes':
            queryset = queryset.order_by('-downvotes') 
        else:  
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add search query, sort order, and page object to the context.
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['sort'] = self.request.GET.get('sort', 'newest')  
        return context

class RecipeDetailView(DetailView):
    model = models.Recipe

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('user-profile')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'ingredients', 'instructions', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'description', 'ingredients', 'instructions', 'image']

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def upvote_recipe(request, pk):
    """Handles upvoting a recipe."""
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    # Remove downvote if already present
    if user in recipe.downvotes.all():
        recipe.downvotes.remove(user)

    # Toggle upvote
    if user in recipe.upvotes.all():
        recipe.upvotes.remove(user)  # If already upvoted, remove the upvote
    else:
        recipe.upvotes.add(user)  # Otherwise, add the upvote

    return JsonResponse({'upvotes': recipe.upvote_count(), 'downvotes': recipe.downvote_count()})


@login_required
def downvote_recipe(request, pk):
    """Handles downvoting a recipe."""
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    # Remove upvote if already present
    if user in recipe.upvotes.all():
        recipe.upvotes.remove(user)

    # Toggle downvote
    if user in recipe.downvotes.all():
        recipe.downvotes.remove(user)  # If already downvoted, remove the downvote
    else:
        recipe.downvotes.add(user)  # Otherwise, add the downvote

    return JsonResponse({'upvotes': recipe.upvote_count(), 'downvotes': recipe.downvote_count()})