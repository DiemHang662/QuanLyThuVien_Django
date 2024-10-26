from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone


class NguoiDung(AbstractUser):
    CHUC_VU_CHOICES = [
        ('nhan_vien', 'Nhân viên'),
        ('doc_gia', 'Độc giả'),
    ]

    avatar = CloudinaryField('avatar', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    nam_sinh = models.IntegerField(null=True, blank=True)
    chucVu = models.CharField(
        max_length=255,
        choices=CHUC_VU_CHOICES,
        default='doc_gia'  # Default role is 'Độc giả'
    )
    soLuongMuon = models.IntegerField(default=0)
    soLuongTra = models.IntegerField(default=0)
    soLuongQuaHan = models.IntegerField(default=0)

    def __str__(self):
        role_display = dict(self.CHUC_VU_CHOICES).get(self.chucVu, 'Người dùng')
        return f"{role_display}: {self.username}"

    # Override the save method to assign is_superuser and is_staff based on chucVu
    def save(self, *args, **kwargs):
        if self.chucVu == 'nhan_vien':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = True  # 'Độc giả' is a staff member, but not a superuser

        super(NguoiDung, self).save(*args, **kwargs)

# Category model
class DanhMuc(models.Model):
    tenDanhMuc = models.CharField(max_length=255)

    def __str__(self):
        return self.tenDanhMuc

# Book model
class Sach(models.Model):
    tenSach = models.CharField(max_length=255)
    tenTacGia = models.CharField(max_length=255)
    nXB = models.CharField(max_length=255)
    namXB = models.IntegerField()
    soLuong = models.IntegerField()
    soSachDangMuon = models.IntegerField(default=0)
    danhMuc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, related_name="books")
    anhSach = CloudinaryField('anhSach', null=True, blank=True)
    totalBorrowCount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.tenSach

    def borrow_book(self):
        if self.soLuong > 0:
            self.soLuong -= 1
            self.soSachDangMuon += 1
            self.totalBorrowCount += 1
            self.save()

    def return_book(self):
        if self.soSachDangMuon > 0:
            self.soLuong += 1
            self.soSachDangMuon -= 1
            self.save()

class PhieuMuon(models.Model):
    docGia = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    sach = models.ForeignKey(Sach, on_delete=models.SET_NULL, null=True, related_name="phieu_muon")
    ngayMuon = models.DateField(default=timezone.now)
    ngayTraDuKien = models.DateField()

    def __str__(self):
        return f"Phiếu mượn sách #{self.sach.tenSach} - {self.id} - {self.docGia.username} - Ngày mượn: {self.ngayMuon} - Ngày trả dự kiến: {self.ngayTraDuKien}"

class ChiTietPhieuMuon(models.Model):
    STATUS_CHOICES = (
        ('borrowed', 'Đang mượn'),
        ('returned', 'Đã trả'),
        ('late', 'Trễ hạn'),
    )

    phieuMuon = models.ForeignKey(PhieuMuon, on_delete=models.CASCADE, related_name="chi_tiet_phieu_muon")
    ngayTraThucTe = models.DateField(null=True, blank=True)
    tinhTrang = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')
    tienPhat = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    ghiChu = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        sach = None
        if self.phieuMuon:
            sach = self.phieuMuon.sach

        if not self.pk:
            if sach:
                sach.borrow_book()
        if self.ngayTraThucTe:
            if self.ngayTraThucTe > self.phieuMuon.ngayTraDuKien:
                days_late = (self.ngayTraThucTe - self.phieuMuon.ngayTraDuKien).days
                self.tienPhat = days_late * 3000
                self.tinhTrang = 'late'
            else:
                self.tinhTrang = 'returned'

            if sach:
                sach.return_book()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phieuMuon.sach.tenSach} - {self.phieuMuon.docGia.username}"

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Interaction(BaseModel):
    user = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    sach = models.ForeignKey(Sach, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.sach.tenSach}'

    class Meta:
        abstract = True

class BinhLuan(Interaction):
    content = models.CharField(max_length=255)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.sach.tenSach}: {self.content}'

class Thich(Interaction):
    thich = models.CharField(max_length=10, default='like')

    class Meta:
        unique_together = ('user', 'sach')

    def __str__(self):
        return f'Like by {self.user.username} on {self.sach.tenSach}'


# Share model
class ChiaSe(Interaction):
    message = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Share by {self.user.username} on {self.sach.tenSach} with message: {self.message}'