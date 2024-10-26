from rest_framework import serializers
from .models import DanhMuc, Sach, NguoiDung, PhieuMuon, ChiTietPhieuMuon, BinhLuan, Thich, ChiaSe

class DanhMucSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhMuc
        fields = '__all__'

class SachSerializer(serializers.ModelSerializer):
    tenDanhMuc = serializers.CharField(source='danhMuc.tenDanhMuc',read_only=True)
    anhSach_url = serializers.SerializerMethodField()
    anhSach = serializers.ImageField(write_only=True, required=False)

    def get_anhSach_url(self, instance):
        if instance.anhSach:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(instance.anhSach.url)
            return instance.anhSach.url
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['anhSach_url'] = self.get_anhSach_url(instance)
        return rep

    class Meta:
        model = Sach
        fields = '__all__'


class NguoiDungSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    avatar = serializers.ImageField(write_only=True, required=False)
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def get_avatar_url(self, instance):
        if instance.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(instance.avatar.url)
            return instance.avatar.url
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar_url'] = self.get_avatar_url(instance)
        return rep

    def create(self, validated_data):
        avatar = validated_data.pop('avatar', None)
        password = validated_data.pop('password')
        nguoi_dung = NguoiDung(**validated_data)
        nguoi_dung.set_password(password)
        if avatar:
            nguoi_dung.avatar = avatar
        nguoi_dung.save()
        return nguoi_dung

    class Meta:
        model = NguoiDung
        fields = ['id', 'first_name', 'last_name','nam_sinh', 'email', 'phone', 'username', 'password', 'avatar', 'avatar_url',
                  'is_staff', 'is_superuser','chucVu']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }

class PhieuMuonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='docGia.first_name', read_only=True)
    last_name = serializers.CharField(source='docGia.last_name', read_only=True)
    tenSach = serializers.CharField(source='sach.tenSach', read_only=True)

    class Meta:
        model = PhieuMuon
        fields = '__all__'

    def get_tenSach(self, obj):
        return [
            chi_tiet.phieuMuon.sach.tenSach for chi_tiet in obj.chi_tiet_phieu_muon.all()
            if chi_tiet.phieuMuon.sach is not None and chi_tiet.phieuMuon.sach.is_active  # Check for None and active status
        ]

class ChiTietPhieuMuonSerializer(serializers.ModelSerializer):
    sach_id = serializers.CharField(source='phieuMuon.sach.id', read_only=True)
    tenSach = serializers.CharField(source='phieuMuon.sach.tenSach', read_only=True)
    docGia_id = serializers.CharField(source='phieuMuon.docGia.id', read_only=True)
    phieuMuon_id = serializers.CharField(source='phieuMuon.id', read_only=True)
    ngayMuon = serializers.CharField(source='phieuMuon.ngayMuon', read_only=True)
    ngayTraDuKien = serializers.CharField(source='phieuMuon.ngayTraDuKien', read_only=True)
    first_name = serializers.CharField(source='phieuMuon.docGia.first_name', read_only=True)
    last_name = serializers.CharField(source='phieuMuon.docGia.last_name', read_only=True)
    phone = serializers.CharField(source='phieuMuon.docGia.phone', read_only=True)
    anhSach_url = serializers.SerializerMethodField()
    anhSach = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = ChiTietPhieuMuon
        fields = '__all__'

    def get_anhSach_url(self, instance):
        # Access the sach through the phieuMuon relation
        if instance.phieuMuon and instance.phieuMuon.sach and instance.phieuMuon.sach.anhSach:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(instance.phieuMuon.sach.anhSach.url)
            return instance.phieuMuon.sach.anhSach.url
        return None

    def create(self, validated_data):
        return super().create(validated_data)


class BinhLuanSerializer(serializers.ModelSerializer):
    user = NguoiDungSerializer(read_only=True)  # Include user details
    sach = SachSerializer(read_only=True)  # Include book details

    class Meta:
        model = BinhLuan
        fields = ['id', 'user', 'sach', 'content', 'created_at', 'updated_at']


class ThichSerializer(serializers.ModelSerializer):
    user = NguoiDungSerializer(read_only=True)
    sach = SachSerializer(read_only=True)
    anhSach_url = serializers.SerializerMethodField()
    anhSach = serializers.ImageField(write_only=True, required=False)
    tenTacGia= serializers.CharField(source='sach.tenTacGia', read_only=True)

    def get_anhSach_url(self, instance):
        if instance.sach and instance.sach.anhSach:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(instance.sach.anhSach.url)
            return instance.sach.anhSach.url
        return None

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Thich
        fields = ['id','thich', 'user', 'sach', 'created_at', 'updated_at','anhSach','anhSach_url']


class ChiaSeSerializer(serializers.ModelSerializer):
    user = NguoiDungSerializer(read_only=True)  # Include user details
    sach = SachSerializer(read_only=True)  # Include book details

    class Meta:
        model = ChiaSe
        fields = ['id', 'user', 'sach', 'message', 'created_at', 'updated_at']