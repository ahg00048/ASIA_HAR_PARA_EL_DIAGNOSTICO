from rest_framework.routers import DefaultRouter
from ASIA_HAR_SERVER_CORE.api.views import PatientViewSet
from ASIA_HAR_SERVER_CORE.api.views import UserViewSet


router = DefaultRouter()

router.register('users', UserViewSet, 'users')
# router.register('users/{}')
# router.register('users/{}/patients')
# router.register('users/{}/patients/{}')

urlpatterns = router.urls
