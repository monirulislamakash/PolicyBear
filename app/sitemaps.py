from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# IMPORTANT: You MUST import your actual models here to generate dynamic URLs.
# For example: from .models import Resource, Career

class StaticSitemap(Sitemap):
    """
    Sitemap for all static pages defined in your urlpatterns.
    """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        # A list of the URL names for all your static pages.
        return [
            'home',
            'affordable-health-insurance',
            'supplement-insurance',
            'about-us',
            'contact-us',
            'resources',
            'career',
            'PrivacyPolicy',
            'TermsofService',
            'disclaimer',
        ]

    def location(self, item):
        # Use reverse() to get the URL from the name.
        return reverse(item)


class ResourceSitemap(Sitemap):
    """
    Sitemap for dynamic resource detail pages.
    You must fill in the correct model and fields.
    """
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        # Replace 'Resource.objects.all()' with the correct queryset for your model.
        # This queryset determines which objects are included in the sitemap.
        # For example, filter by published status: Resource.objects.filter(is_published=True)
        # return Resource.objects.all()
        return [] # Placeholder

    def lastmod(self, obj):
        # Replace 'obj.last_modified' with the correct field for the last modification date.
        # This field is used for the <lastmod> tag in the sitemap.
        # return obj.last_modified
        return None # Placeholder

    def location(self, obj):
        # Use reverse to generate the URL for each object using its ID.
        # Ensure the URL name 'resourcesdtails' and keyword argument 'id' match your urls.py.
        return reverse('resourcesdtails', kwargs={'id': obj.id})


class CareerSitemap(Sitemap):
    """
    Sitemap for dynamic career detail pages.
    You must fill in the correct model and fields.
    """
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        # Replace 'Career.objects.all()' with the correct queryset for your model.
        # return Career.objects.all()
        return [] # Placeholder

    def lastmod(self, obj):
        # Replace 'obj.last_modified' with the correct field for the last modification date.
        # return obj.last_modified
        return None # Placeholder

    def location(self, obj):
        # Use reverse to generate the URL for each object using its ID.
        # Ensure the URL name 'careerdtails' and keyword argument 'id' match your urls.py.
        return reverse('careerdtails', kwargs={'id': obj.id})
