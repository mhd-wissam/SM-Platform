# إضافة الفئات (Categories) إلى قاعدة البيانات

هناك ثلاث طرق لإضافة الفئات إلى قاعدة البيانات:

## الطريقة 1: استخدام Django Admin (الأسهل)

1. قم بإنشاء superuser إذا لم يكن موجوداً:
```bash
python manage.py createsuperuser
```

2. شغّل السيرفر:
```bash
python manage.py runserver
```

3. افتح المتصفح واذهب إلى: `http://127.0.0.1:8000/admin/`

4. سجّل الدخول باستخدام بيانات superuser

5. ستجد قسم "الفئات" حيث يمكنك إضافة فئات جديدة يدوياً

## الطريقة 2: استخدام Management Command (الأسرع)

قم بتشغيل الأمر التالي لإضافة الفئات الافتراضية:

```bash
python manage.py add_categories
```

لحذف جميع الفئات الحالية وإضافة فئات جديدة:

```bash
python manage.py add_categories --clear
```

### الفئات الافتراضية المضافة:
- كهرباء (Electricity)
- مياه (Water)
- صرف صحي (Sewage)
- إنترنت (Internet)
- هاتف (Phone)
- طرق (Roads)
- إنارة (Lighting)
- أخرى (Other)

## الطريقة 3: استخدام Fixtures (للمشاريع الكبيرة)

قم بتحميل البيانات من ملف JSON:

```bash
python manage.py loaddata initial_categories
```

ملاحظة: تأكد من وجود ملف `submissions/fixtures/initial_categories.json`

---

## تعديل الفئات الافتراضية

يمكنك تعديل الفئات الافتراضية في الملف:
- `submissions/management/commands/add_categories.py` (للمنطق)
- `submissions/fixtures/initial_categories.json` (للفيxtures)

