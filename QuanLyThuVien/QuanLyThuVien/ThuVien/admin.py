from django.contrib import admin
from .models import DanhMuc, Sach, NguoiDung, Thich, BinhLuan, ChiaSe, PhieuMuon, ChiTietPhieuMuon


class MyApartAdminSite(admin.AdminSite):
    site_header = "LIBRARY MANAGEMENT SYSTEM"

admin_site = MyApartAdminSite(name='myAdmin')

admin_site.register(DanhMuc)
admin_site.register(Sach)
admin_site.register(NguoiDung)
admin_site.register(PhieuMuon)
admin_site.register(ChiTietPhieuMuon)
admin_site.register(Thich)
admin_site.register(BinhLuan)
admin_site.register(ChiaSe)
