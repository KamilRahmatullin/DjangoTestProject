from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'created_at')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        """
        Returns a dictionary mapping field names to the list of fields from which they are automatically populated.

        Parameters:
        - request: The request object.
        - obj: The object being edited, if applicable.

        Returns:
        A dictionary where the keys are field names and the values are lists of field names from which they are automatically populated.
        """
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'slug', 'price', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):
        """
        Returns a dictionary mapping field names to the list of fields from which they are automatically populated.

        Parameters:
        - request: The request object.
        - obj: The object being edited, if applicable.

        Returns:
        A dictionary where the keys are field names and the values are lists of field names from which they are automatically populated.
        """
        return {'slug': ('title',)}
