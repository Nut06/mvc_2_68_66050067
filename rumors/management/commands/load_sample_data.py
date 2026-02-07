from django.core.management.base import BaseCommand
from rumors.models import User, Rumour, Report
from datetime import date


class Command(BaseCommand):
    help = 'Load sample data for Rumor Tracking System'

    def handle(self, *args, **options):
        # ลบข้อมูลเก่า
        Report.objects.all().delete()
        Rumour.objects.all().delete()
        User.objects.all().delete()

        # สร้าง Users (10 คน)
        users_data = [
            ('U001', 'สมชาย ใจดี', 'general_user'),
            ('U002', 'สมหญิง รักเรียน', 'general_user'),
            ('U003', 'วิชัย มานะ', 'general_user'),
            ('U004', 'มานี มีสุข', 'general_user'),
            ('U005', 'ปิยะ ศรีสุข', 'general_user'),
            ('U006', 'นิตยา ใจงาม', 'general_user'),
            ('U007', 'ประสิทธิ์ ดีมาก', 'general_user'),
            ('U008', 'สุนีย์ รักษ์ดี', 'general_user'),
            ('V001', 'ดร.วิเชียร ตรวจสอบ', 'verifier'),
            ('V002', 'ผศ.สุภาพ พิสูจน์', 'verifier'),
        ]
        
        users = []
        for user_id, name, role in users_data:
            user = User.objects.create(user_id=user_id, name=name, role=role)
            users.append(user)
            self.stdout.write(f'Created user: {name}')

        # สร้าง Rumours (8 ข่าว)
        rumours_data = [
            ('10000001', 'น้ำประปาปนเปื้อนสารพิษ', 'Facebook', 30, 'panic'),
            ('20000002', 'รัฐบาลจะขึ้นภาษีเป็น 20%', 'Twitter', 25, 'panic'),
            ('30000003', 'วัคซีนใหม่มีผลข้างเคียงร้ายแรง', 'LINE', 40, 'panic'),
            ('40000004', 'ราคาน้ำมันจะลดลง 50%', 'Facebook', 15, 'normal'),
            ('50000005', 'โรงเรียนจะหยุดยาว 2 เดือน', 'TikTok', 10, 'normal'),
            ('60000006', 'ธนาคารจะปิดตัว', 'Twitter', 5, 'verified_false'),
            ('70000007', 'มีการค้นพบแหล่งน้ำมันใหม่', 'News', 20, 'verified_true'),
            ('80000008', 'ระบบขนส่งมวลชนฟรีตลอดปี', 'LINE', 8, 'normal'),
        ]
        
        rumours = []
        for rumour_id, title, source, score, status in rumours_data:
            rumour = Rumour.objects.create(
                rumour_id=rumour_id,
                title=title,
                source=source,
                credibility_score=score,
                status=status
            )
            rumours.append(rumour)
            self.stdout.write(f'Created rumour: {title}')

        # สร้าง Reports (20+ รายงาน)
        reports_data = [
            # ข่าว panic 1 - 6 รายงาน
            ('U001', '10000001', 'distorted'),
            ('U002', '10000001', 'false'),
            ('U003', '10000001', 'inciting'),
            ('U004', '10000001', 'false'),
            ('U005', '10000001', 'distorted'),
            ('U006', '10000001', 'inciting'),
            # ข่าว panic 2 - 5 รายงาน
            ('U001', '20000002', 'inciting'),
            ('U002', '20000002', 'false'),
            ('U003', '20000002', 'distorted'),
            ('U004', '20000002', 'inciting'),
            ('U005', '20000002', 'false'),
            # ข่าว panic 3 - 7 รายงาน
            ('U001', '30000003', 'false'),
            ('U002', '30000003', 'false'),
            ('U003', '30000003', 'distorted'),
            ('U004', '30000003', 'inciting'),
            ('U005', '30000003', 'false'),
            ('U006', '30000003', 'distorted'),
            ('U007', '30000003', 'inciting'),
            # ข่าว normal - 3 รายงาน
            ('U001', '40000004', 'distorted'),
            ('U002', '40000004', 'false'),
            ('U003', '40000004', 'inciting'),
            # ข่าว normal - 2 รายงาน
            ('U001', '50000005', 'distorted'),
            ('U002', '50000005', 'false'),
        ]
        
        for reporter_id, rumour_id, report_type in reports_data:
            try:
                user = User.objects.get(user_id=reporter_id)
                rumour = Rumour.objects.get(rumour_id=rumour_id)
                # ข้ามถ้าข่าว verified
                if not rumour.is_verified:
                    Report.objects.create(
                        reporter=user,
                        rumour=rumour,
                        report_type=report_type
                    )
                    self.stdout.write(f'Created report: {reporter_id} -> {rumour_id}')
            except Exception as e:
                self.stdout.write(f'Skipped: {str(e)}')

        self.stdout.write(self.style.SUCCESS('✅ Sample data loaded successfully!'))
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Rumours: {Rumour.objects.count()}')
        self.stdout.write(f'Reports: {Report.objects.count()}')
