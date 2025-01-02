from .models import Category

def categories_links(request) :
    links = Category.objects.all()
    return {"categories_links" : links}