from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from app.views import *
from app.sitemaps import StaticSitemap # Removed unused sitemap imports for now
# You can re-import these when you define them in sitemaps.py:
# from app.sitemaps import ResourceSitemap, CareerSitemap

# Define a dictionary of your sitemap classes.
sitemaps = {
    'static': StaticSitemap,
    # Uncomment these and add your models when you are ready:
    # 'resources': ResourceSitemap,
    # 'careers': CareerSitemap,
}

urlpatterns = [
    # Static pages
    path('', index, name='home'),
    path('affordable-health-insurance', affordable_health_insurance, name='affordable-health-insurance'),
    path('supplement-insurance', supplement_insurance, name='supplement-insurance'),
    path('about-us', about_us, name='about-us'),
    path('contact-us', contact_us, name='contact-us'),
    path('resources', resources, name='resources'),
    path('career', career, name='career'),
    path('privacy-policy', PrivacyPolicy, name="PrivacyPolicy"),
    path('terms-conditions', TermsofService, name="TermsofService"),
    path('disclaimer', disclaimer, name="disclaimer"),

    # Dynamic pages
    path('resources/dtails/<slug:slug>', resourcesdtails, name='resourcesdtails'),
    path('career/details-page/<int:int>', careerdtails, name='careerdtails'),
    path('career/submit/details-page/<int:id>', careersubmitdtails, name='careersubmitdtails'),

    # Sitemaps and Robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    # Bot Endpoints
    path("ask", ask, name="ask"),
    path("diag", diag, name="diag"),
    path("gpt_echo", gpt_echo, name="gpt_echo"),
    # APT Endpoints
    path('api/ai/agent/', api_for_ai_agent, name='api_for_ai_agent'),
]