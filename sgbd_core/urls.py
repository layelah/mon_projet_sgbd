from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from exercises.views import ExerciseViewSet
from submissions.views import SubmissionViewSet
from users.views import CustomUserCreateView

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Remplacer la vue de création d'utilisateur de Djoser
    path('auth/users/', CustomUserCreateView.as_view(), name='user-create'),
    # Gardez ces lignes après votre vue personnalisée pour que les autres routes fonctionnent
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]