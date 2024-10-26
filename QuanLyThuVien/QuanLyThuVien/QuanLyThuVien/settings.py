from pathlib import Path
import cloudinary.api
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-4l8)pl&9nu4@b-22rk(4n6)o)0@in__@ke$g$$qj+0lc=6%_ug'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.9']

cloudinary.config(
    cloud_name="dmjydfpev",
    api_key="153344775849929",
    api_secret="soU85tUSegDS6ZqoM1l6jERP7Ug",
    secure=True
)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.1.9:3000",
]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ThuVien',
    'rest_framework',
    'cloudinary',
    'oauth2_provider',
    'drf_yasg',
    'corsheaders',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'QuanLyThuVien.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'QuanLyThuVien.wsgi.application'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'quanlithuvien',
    'USER': 'root',
    'PASSWORD': 'Diemhang662',
    'HOST': ''
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

AUTH_USER_MODEL = 'ThuVien.NguoiDung'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CLIENT_ID = 'N0mM3SSvaoWPwqvsDox8q6vDzcigFVIBEwQbXShE'
CLIENT_SECRET = 'Gmkimw3up56qby9IgYgLFswu2hSwrOATTFDKbxBGaOEOzjqfUL0ot4pCOoAuomCimIrVWw52y4genRFXsSjjrGGAtwm6KxjKosU3h2IBVEByZXuHZ0u4So9KenGT5gRq'

VNPAY_TMN_CODE = 'C3DQBPKK'
VNPAY_HASH_SECRET_KEY = 'WJPF0X7HRIT5A0KY9IHC6JXIHSPDMGCZ'
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # Sandbox URL
VNPAY_RETURN_URL = 'http://localhost:8000/payment_return/'  # Change based on your project

