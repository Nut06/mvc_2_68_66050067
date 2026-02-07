from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Rumour, Report, User


# หน้ารวมข่าวลือ - แสดงข่าวลือทั้งหมด เรียงตามจำนวนรายงาน
def rumour_list(request):
    sort_by = request.GET.get('sort', 'reports')
    rumours = Rumour.objects.sorted_by(sort_by)
    
    context = {
        'rumours': rumours,
        'sort_by': sort_by,
    }
    return render(request, 'rumors/rumour_list.html', context)


# หน้ารายละเอียดข่าวลือ - แสดงรายละเอียด + จำนวนรายงาน
def rumour_detail(request, rumour_id):
    rumour = get_object_or_404(Rumour, rumour_id=rumour_id)
    
    context = {
        'rumour': rumour,
        'reports': rumour.report_set.all(),
        'general_users': User.objects.general_users(),
        'verifiers': User.objects.verifiers(),
    }
    return render(request, 'rumors/rumour_detail.html', context)


# หน้าสรุปผล - แสดงข่าว panic และ verified
def summary(request):
    context = {
        'panic_rumours': Rumour.objects.panic(),
        'verified_true': Rumour.objects.verified_true(),
        'verified_false': Rumour.objects.verified_false(),
    }
    return render(request, 'rumors/summary.html', context)




def add_report(request, rumour_id):
    if request.method == 'POST':
        rumour = get_object_or_404(Rumour, rumour_id=rumour_id)
        user_id = request.POST.get('user_id')
        action_type = request.POST.get('action_type')  # report หรือ verify
        
        try:
            user = User.objects.get(user_id=user_id)
            
            # ตรวจสอบว่าข่าวถูก verify แล้วหรือไม่
            if rumour.is_verified:
                messages.error(request, 'ไม่สามารถดำเนินการกับข่าวที่ถูกตรวจสอบแล้วได้')
                return redirect('rumors:rumour_detail', rumour_id=rumour_id)
            
            # แยก logic ตาม role
            if user.role == 'verifier':
                # ผู้ตรวจสอบ - verify ข่าว
                verification = request.POST.get('verification')
                is_true = (verification == 'true')
                rumour.verify(verified_by=user, is_true=is_true)
                messages.success(request, f'ยืนยันข่าวเป็น {"จริง" if is_true else "เท็จ"} สำเร็จ!')
            else:
                # ผู้ใช้ทั่วไป - รายงานข่าว
                report_type = request.POST.get('report_type')
                Report.objects.create(
                    reporter=user,
                    rumour=rumour,
                    report_type=report_type
                )
                messages.success(request, 'รายงานสำเร็จ!')
            
        except IntegrityError:
            messages.error(request, 'คุณได้รายงานข่าวนี้ไปแล้ว')
        except User.DoesNotExist:
            messages.error(request, 'ไม่พบผู้ใช้')
        except ValueError as e:
            messages.error(request, str(e))
    
    return redirect('rumors:rumour_detail', rumour_id=rumour_id)
