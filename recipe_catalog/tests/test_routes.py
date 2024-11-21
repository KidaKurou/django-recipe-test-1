from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus
from recipe_catalog.models import Recipe, Ingredient, RecipeIngredient
from datetime import timedelta

class RouteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test ingredient
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient', 
            weight=100, 
            weight_ready=80, 
            price=10.50
        )
        
        # Create test recipe
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            cooking_time=timedelta(minutes=30)
        )
        
        # Link ingredient to recipe
        RecipeIngredient.objects.create(
            recipe=self.recipe, 
            ingredient=self.ingredient
        )

    def test_index_route(self):
        """Test index page route accessibility"""
        response = self.client.get(reverse('recipe_catalog:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'recipe_catalog/index.html')

    def test_about_route(self):
        """Test about page route accessibility"""
        response = self.client.get(reverse('recipe_catalog:about'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'recipe_catalog/about.html')

    def test_recipe_detail_route(self):
        """Test specific recipe detail page route"""
        response = self.client.get(reverse('recipe_catalog:recipe_detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'recipe_catalog/recipe.html')

    def test_nonexistent_recipe_route(self):
        """Test route for non-existent recipe"""
        non_existent_id = Recipe.objects.count() + 999
        response = self.client.get(reverse('recipe_catalog:recipe_detail', kwargs={'pk': non_existent_id}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)