from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from recipe_catalog.models import Recipe, Ingredient, RecipeIngredient

class RecipeContentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data that will be shared across all test methods"""
        # Create test ingredients
        cls.flour = Ingredient.objects.create(
            name='Flour', 
            weight=1000,  # 1 kg
            weight_ready=900,  # 900g after processing
            price=Decimal('2.50')
        )
        
        cls.water = Ingredient.objects.create(
            name='Water', 
            weight=1000,  # 1 liter
            weight_ready=1000,  # no change
            price=Decimal('0.10')
        )
        
        # Create multiple test recipes to test sorting and pagination
        recipes_data = [
            {'title': 'Cake', 'description': 'Sweet cake', 'cooking_time': '01:00:00'},
            {'title': 'Apple Pie', 'description': 'Delicious pie', 'cooking_time': '00:45:00'},
            {'title': 'Bread', 'description': 'Simple bread', 'cooking_time': '02:00:00'}
        ]
        
        cls.recipes = []
        for recipe_data in recipes_data:
            recipe = Recipe.objects.create(**recipe_data)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=cls.flour)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=cls.water)
            cls.recipes.append(recipe)

    def test_ingredient_creation(self):
        """Test correct creation of ingredient objects"""
        self.assertEqual(self.flour.name, 'Flour')
        self.assertEqual(self.flour.weight, 1000)
        self.assertEqual(self.flour.weight_ready, 900)
        self.assertEqual(self.flour.price, Decimal('2.50'))

    def test_recipe_creation(self):
        """Test correct creation of recipe objects"""
        recipe = self.recipes[0]
        self.assertTrue(isinstance(recipe, Recipe))
        self.assertTrue(recipe.ingredients.exists())

    def test_ingredients_alphabetical_order(self):
        """Test ingredients are sorted alphabetically in recipe details"""
        recipe = self.recipes[0]
        recipe_ingredients = recipe.ingredients.order_by('name')
        self.assertEqual(list(recipe_ingredients), [self.flour, self.water])

    def test_recipes_alphabetical_order(self):
        """Test recipes are sorted alphabetically on index page"""
        response = self.client.get(reverse('recipe_catalog:index'))
        recipes_in_context = response.context['recipes']
        
        # Check that recipes are sorted alphabetically
        sorted_titles = [recipe.title for recipe in recipes_in_context]
        self.assertEqual(sorted_titles, sorted(sorted_titles))

    def test_recipe_limit(self):
        """Test that no more than 10 recipes are displayed on the index page"""
        # Create additional recipes to test pagination
        for i in range(15):
            Recipe.objects.create(
                title=f'Additional Recipe {i}', 
                description='Test Description',
                cooking_time='00:30:00'
            )
        
        response = self.client.get(reverse('recipe_catalog:index'))
        recipes_in_context = response.context['recipes']
        self.assertTrue(len(recipes_in_context) <= 10)

    def test_recipe_image_upload(self):
        """Test image upload for a recipe"""
        image = SimpleUploadedFile(
            name='test_image.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        recipe = Recipe.objects.create(
            title='Image Test Recipe',
            description='Recipe with image',
            cooking_time='00:30:00',
            image=image
        )
        
        self.assertTrue(recipe.image)
        self.assertIn('recipe_images/', recipe.image.name)