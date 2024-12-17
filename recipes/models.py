from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Recipe(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  ingredients = models.TextField()
  instructions = models.TextField()
  image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  upvotes = models.ManyToManyField(User, related_name='upvoted_recipes', blank=True)
  downvotes = models.ManyToManyField(User, related_name='downvoted_recipes', blank=True)

  def upvote_count(self):
      return self.upvotes.count()

  def downvote_count(self):
      return self.downvotes.count()

  def get_absolute_url(self):
      return reverse("recipes-detail", kwargs={"pk": self.pk})

  def __str__(self):
    return self.title