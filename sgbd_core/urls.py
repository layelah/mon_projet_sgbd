from django.urls import include, path
from rest_framework.routers import DefaultRouter
from exercises.views import ExerciseViewSet
from submissions.views import SubmissionViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)    # Endpoint: /api/exercises/
router.register(r'submissions', SubmissionViewSet) # Endpoint: /api/submissions/

urlpatterns = [
    path('api/', include(router.urls)),  # Toutes les routes API
]