from rest_framework.routers import DefaultRouter
from basic import viewsets

router = DefaultRouter()
router.register('employee', viewsets.EmployeeViewSet)

urlpatterns = router.urls
