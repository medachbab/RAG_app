import json
import os
from .models import Product, Review, Category
from django.contrib.auth.models import User
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
file_path = os.getenv('FILE_PATH')

def import_data_service():
    """
    Import products and reviews from a JSON file into the Django database.
    """
    try:
        # Get default user (admin) for product creation
        default_user = User.objects.get(username=os.getenv('ADMIN'))

        # Load data from JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        for item in data:
            # Create or get category
            category, _ = Category.objects.get_or_create(name=item['category'])

            # Create or get reviewers
            for review in item.get('reviews', []):
                reviewer, _ = User.objects.get_or_create(
                    defaults={
                        'username': review['reviewerName'],
                        'first_name': review['reviewerName'].split()[0],
                        'last_name': ' '.join(review['reviewerName'].split()[1:])
                    }
                )

            # Create product
            product = Product.objects.create(
                id=item['id'],
                title=item['title'],
                description=item['description'],
                category=category,
                price=item['price'],
                rating=item['rating'],
                stock=item['stock'],
                user=default_user,
                image=item['image'],
            )

            # Create reviews
            for review in item.get('reviews', []):
                Review.objects.create(
                    product=product,
                    rating=review['rating'],
                    comment=review['comment'],
                    reviewer=reviewer
                )

    except Exception as e:
        return str(e)

    return "Data imported successfully!"
