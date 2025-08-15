from django.urls import path
from app.views import *

urlpatterns = [
    path('', index, name='home'),
    path('affordable-health-insurance', affordable_health_insurance, name='affordable-health-insurance'),
    path('supplement-insurance', supplement_insurance, name='supplement-insurance'),
    path('api/ai/agent/', api_for_ai_agent, name='api_for_ai_agent'),
]