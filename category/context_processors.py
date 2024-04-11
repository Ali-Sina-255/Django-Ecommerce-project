from . models import Category

def category_list(self):
    categories = Category.objects.all()
    return dict(categories=categories)