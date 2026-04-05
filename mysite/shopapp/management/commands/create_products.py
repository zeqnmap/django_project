from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write("create products")

        products_names = [
            "laptop",
            'desktop',
            'smartphone'
        ]
        for products_name in products_names:
            product, created = Product.objects.get_or_create(name=products_name)
            self.stdout.write(f"created product {product.name}")

        self.stdout.write(self.style.SUCCESS("create products"))