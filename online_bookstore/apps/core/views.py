# views.py in the 'core' app

from django.views.generic import TemplateView

from online_bookstore.apps.book.models import Book


class HomePageView(TemplateView):
    template_name = 'base/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch featured books from the database
        featured_books = Book.objects.filter(featured=True)
        context['featured_books'] = featured_books

        return context
