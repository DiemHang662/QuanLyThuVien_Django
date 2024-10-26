# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .admin import admin_site
from . import views

router = DefaultRouter()
router.register('danhmuc', views.DanhMucViewSet, basename='danhmuc')
router.register('sach', views.SachViewSet, basename='sach')
router.register('nguoidung', views.NguoiDungViewSet, basename='nguoidung')
router.register('phieumuon', views.PhieuMuonViewSet, basename='phieumuon')
router.register('chitietphieumuon', views.ChiTietPhieuMuonViewSet, basename='chitietphieumuon')
router.register('thich', views.ThichViewSet, basename='thich')
router.register('binhluan', views.BinhLuanViewSet, basename='binhluan')
router.register('chiase', views.ChiaSeViewSet, basename='chiase')
router.register('payment', views.PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),  # API endpoints
    path('admin/', admin_site.urls),
    path('api/', include(router.urls)),
    path('payment/', views.payment_view, name='payment'),
]