# SM Platform Backend

منصة التقديمات الاجتماعية - Backend API

## المميزات

- 🔐 مصادقة باستخدام OTP عبر SMS
- 📱 JWT Authentication
- 📤 إدارة التقديمات (Submissions)
- 🏷️ نظام الفئات (Categories)
- 📸 رفع الصور (Images)
- 🗄️ قاعدة بيانات MySQL

## المتطلبات

- Python 3.10+
- MySQL 5.7+
- Git

## التثبيت

### 1. استنساخ المشروع

```bash
git clone https://github.com/mhd-wissam/SM-Platform.git
cd SM-Platform
```

### 2. إنشاء بيئة افتراضية

```bash
python -m venv venv
```

### 3. تفعيل البيئة الافتراضية

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 5. إعداد قاعدة البيانات

قم بإنشاء قاعدة بيانات MySQL:

```sql
CREATE DATABASE sm_platform_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. إعداد الإعدادات

قم بتعديل ملف `SM_platform/settings.py` وأضف معلومات قاعدة البيانات:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sm_platform_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 7. تشغيل Migrations

```bash
python manage.py migrate
```

### 8. إضافة الفئات

```bash
python manage.py add_categories
```

### 9. إنشاء Superuser (للدخول إلى Admin)

```bash
python manage.py createsuperuser
```

### 10. تشغيل السيرفر

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/auth/send-otp/` - إرسال كود OTP
- `POST /api/auth/verify-otp/` - التحقق من كود OTP
- `POST /api/auth/refresh-token/` - تحديث Access Token
- `GET /api/auth/profile/` - بيانات المستخدم الحالي

### Categories

- `GET /api/categories/` - قائمة الفئات

### Submissions

- `GET /api/submissions/` - قائمة التقديمات
- `POST /api/submissions/` - إنشاء تقديم جديد
- `GET /api/submissions/{id}/` - تفاصيل تقديم
- `PUT /api/submissions/{id}/` - تحديث تقديم
- `DELETE /api/submissions/{id}/` - حذف تقديم

## استخدام Postman

يمكنك استيراد ملف `SM_Platform_Postman_Collection.json` في Postman لاختبار API.

## هيكل المشروع

```
SM_platform_backend/
├── SM_platform/          # إعدادات المشروع الرئيسية
│   ├── settings.py       # إعدادات Django
│   ├── urls.py           # URLs الرئيسية
│   └── wsgi.py           # WSGI configuration
├── submissions/          # تطبيق Submissions
│   ├── models.py         # النماذج
│   ├── views.py          # Views
│   ├── serializers.py    # Serializers
│   ├── urls.py           # URLs
│   ├── admin.py          # Django Admin
│   └── management/       # Management Commands
│       └── commands/
│           └── add_categories.py
├── media/                # ملفات الميديا (الصور)
│   ├── submissions/      # صور التقديمات
│   └── invoices/         # صور الفواتير
├── requirements.txt      # المتطلبات
└── README.md            # هذا الملف
```

## الأمان

⚠️ **مهم:** لا ترفع ملف `settings.py` الذي يحتوي على معلومات حساسة (مثل كلمة مرور قاعدة البيانات) إلى GitHub. استخدم متغيرات البيئة (Environment Variables) في الإنتاج.

## المساهمة

1. Fork المشروع
2. أنشئ branch جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى Branch (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

## الرخصة

هذا المشروع مفتوح المصدر.

## التواصل

للاستفسارات والدعم، يرجى فتح Issue في GitHub.

