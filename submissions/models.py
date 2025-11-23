from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="رقم الهاتف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        db_table = 'Users'
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'

    @property
    def id(self):
        """Return user_id for JWT compatibility"""
        return self.user_id

    @property
    def is_authenticated(self):
        """Always return True for authenticated users"""
        return True

    @property
    def is_active(self):
        """Always return True for active users"""
        return True

    @property
    def is_staff(self):
        """Return False as this is not a staff user"""
        return False

    @property
    def is_superuser(self):
        """Return False as this is not a superuser"""
        return False

    def has_perm(self, perm, obj=None):
        """Return False as custom users don't have permissions"""
        return False

    def has_perms(self, perm_list, obj=None):
        """Return False as custom users don't have permissions"""
        return False

    def has_module_perms(self, app_label):
        """Return False as custom users don't have module permissions"""
        return False

    def __str__(self):
        return self.phone_number


class OtpCode(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    hashed_code = models.CharField(max_length=255, verbose_name="الكود المشفر")
    expires_at = models.DateTimeField(verbose_name="تاريخ الانتهاء")

    class Meta:
        db_table = 'OtpCodes'
        verbose_name = 'كود OTP'
        verbose_name_plural = 'أكواد OTP'

    def __str__(self):
        return f"{self.phone_number} - {self.expires_at}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name_ar = models.CharField(max_length=100, verbose_name="الاسم بالعربية")
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name="الاسم بالإنجليزية")

    class Meta:
        db_table = 'Categories'
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'

    def __str__(self):
        return self.name_ar


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', verbose_name="المستخدم")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id', verbose_name="الفئة")
    image_url = models.ImageField(upload_to='submissions/', verbose_name="صورة التقديم")
    notes = models.TextField(blank=True, null=True, verbose_name="الملاحظات")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="خط العرض")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="خط الطول")
    counter_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم العداد")
    consumption_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم الاستهلاك")
    invoice_image = models.ImageField(upload_to='invoices/', blank=True, null=True, verbose_name="صورة الفاتورة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        db_table = 'Submissions'
        verbose_name = 'تقديم'
        verbose_name_plural = 'التقديمات'

    def __str__(self):
        return f"تقديم {self.submission_id} - {self.user.phone_number}"
