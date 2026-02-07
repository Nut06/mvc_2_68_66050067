from django.db import models
from django.db.models import Count


# Manager สำหรับ User
class UserManager(models.Manager):
    def general_users(self):
        return self.filter(role='general_user')
    
    def verifiers(self):
        return self.filter(role='verifier')


# ผู้ใช้งานระบบ
class User(models.Model):
    ROLE_CHOICES = [
        ('general_user', 'ผู้ใช้ทั่วไป'),
        ('verifier', 'ผู้ตรวจสอบ'),
    ]
    
    user_id = models.CharField(max_length=10, primary_key=True, verbose_name='รหัสผู้ใช้')
    name = models.CharField(max_length=100, verbose_name='ชื่อ')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='general_user', verbose_name='บทบาท')

    objects = UserManager()

    class Meta:
        verbose_name = 'ผู้ใช้งาน'
        verbose_name_plural = 'ผู้ใช้งาน'

    def __str__(self):
        return f"{self.user_id} - {self.name}"


# Manager สำหรับ Rumour
class RumourManager(models.Manager):
    def sorted_by(self, sort_type):
        if sort_type == 'score':
            return self.order_by('-credibility_score')
        return self.annotate(report_count_num=Count('report')).order_by('-report_count_num')
    
    def panic(self):
        return self.filter(status='panic')
    
    def verified_true(self):
        return self.filter(status='verified_true')
    
    def verified_false(self):
        return self.filter(status='verified_false')


# ข่าวลือ
class Rumour(models.Model):
    STATUS_CHOICES = [
        ('normal', 'ปกติ'),
        ('panic', 'Panic'),
        ('verified_true', 'ยืนยันว่าจริง'),
        ('verified_false', 'ยืนยันว่าเท็จ'),
    ]
    
    rumour_id = models.CharField(max_length=8, primary_key=True, verbose_name='รหัสข่าวลือ')
    title = models.CharField(max_length=255, verbose_name='หัวข้อข่าว')
    source = models.CharField(max_length=255, verbose_name='แหล่งที่มา')
    created_date = models.DateField(auto_now_add=True, verbose_name='วันที่สร้าง')
    credibility_score = models.IntegerField(default=0, verbose_name='คะแนนความน่าเชื่อถือ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name='สถานะ')

    PANIC_THRESHOLD = 5  # จำนวนรายงานที่ทำให้เข้าสู่ panic

    objects = RumourManager()

    class Meta:
        verbose_name = 'ข่าวลือ'
        verbose_name_plural = 'ข่าวลือ'
        ordering = ['-credibility_score']

    def __str__(self):
        return f"{self.rumour_id} - {self.title}"

# นับจำนวนรายงาน
    @property
    def report_count(self):
        return self.report_set.count()

# ตรวจสอบว่าถูก verify แล้วหรือไม่
    @property
    def is_verified(self):
        return self.status in ['verified_true', 'verified_false']

# ตรวจสอบและเปลี่ยนสถานะเป็น panic ถ้าเกิน threshold
    def check_panic_status(self):
        if self.report_count >= self.PANIC_THRESHOLD and self.status == 'normal':
            self.status = 'panic'
            self.save()

# ผู้ตรวจสอบ verify ข่าวลือ
    def verify(self, verified_by, is_true):
        if verified_by.role != 'verifier':
            raise ValueError("เฉพาะผู้ตรวจสอบเท่านั้นที่สามารถ verify ข่าวได้")
        
        if is_true:
            self.status = 'verified_true'
        else:
            self.status = 'verified_false'
        self.save()


# การรายงานข่าว
class Report(models.Model):
    TYPE_CHOICES = [
        ('distorted', 'บิดเบือน'),
        ('inciting', 'ปลุกปั่น'),
        ('false', 'ข้อมูลเท็จ'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ผู้รายงาน')
    rumour = models.ForeignKey(Rumour, on_delete=models.CASCADE, verbose_name='ข่าวลือ')
    report_date = models.DateField(auto_now_add=True, verbose_name='วันที่รายงาน')
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='ประเภทรายงาน')

    class Meta:
        verbose_name = 'รายงาน'
        verbose_name_plural = 'รายงาน'
        unique_together = ['reporter', 'rumour']  # ผู้ใช้รายงานข่าวเดียวกันซ้ำไม่ได้

    def __str__(self):
        return f"{self.reporter} รายงาน {self.rumour}"

    def save(self, *args, **kwargs):
        """ตรวจสอบก่อนบันทึก และอัปเดตสถานะ"""
        # ตรวจสอบว่าข่าวถูก verify แล้วหรือไม่
        if self.rumour.is_verified:
            raise ValueError("ไม่สามารถรายงานข่าวที่ถูกตรวจสอบแล้วได้")
        
        super().save(*args, **kwargs)
        
        # ตรวจสอบสถานะ panic หลังบันทึก
        self.rumour.check_panic_status()
