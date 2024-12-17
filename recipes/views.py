from django.shortcuts import render
from django.urls import reverse_lazy
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

        if sort == 'oldest':
            queryset = queryset.order_by('created_at')  
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
