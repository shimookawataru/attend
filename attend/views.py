from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SubmitAttendance, SubmitError, OverWorkTime
from .forms import SubmitAttendanceForm, SubmitErrForm, SubmitForgetForm
from datetime import datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic
from .sqlite_test import KintaiCheck, labor_time
# from django.contrib.formtools.preview import FormPreview
# Create your views here.

#打刻情報を入力するページへ遷移
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        form = SubmitAttendanceForm
        user = request.user
        object_list = SubmitAttendance.objects.filter(staff_id=user.id).order_by("id").reverse().all()
        in_out_list = ["退勤", "出勤"]
        context = {
            'form': form,
            "user": user,
            "chokkin_date": object_list[:5],
            "in_out_list":in_out_list
        }
        return render(request, 'attend/index.html', context)
index = IndexView.as_view()

#打刻エラーの原因ページへ遷移
class ErrView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form_err = SubmitErrForm
        context = {
            'form_err': form_err,
            "user": user
        }
        return render(request, 'attend/push_err.html', context)

Err = ErrView.as_view()

#打刻忘れの時刻を記入するページへ遷移
class ForgetView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form_forget = SubmitForgetForm
        context = {
            "hoge" : "hoge",
            'form_forget': form_forget,
            "user": user
        }
        return render(request, 'attend/result_err.html', context)

forget = ForgetView.as_view()

#打刻結果をpostする。
class ResultView(View):
    def post(self, request):
        form = SubmitAttendanceForm(request.POST)
        now = datetime.now()
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        obj = form.save(commit=False)
        obj.in_out = request.POST["in_out"]
        obj.staff = request.user
        obj.date = datetime.now().date()
        obj.time = datetime.now().replace(microsecond=0).time()
        obj.save()
        kintai_bool, td_bool = KintaiCheck(obj.staff.id)
        comment_add = False
        if td_bool:
            comment = "打刻エラー: 前回の打刻から5分経過していないので、打刻が認められません。"
            #最新のレコードを削除
            SubmitAttendance.objects.filter(id=obj.id, staff_id=obj.staff.id).delete()
        elif kintai_bool:
            if request.POST["in_out"] == '1':
                comment = str(month) + "月" + str(day) +"日" + str(hour) + "時" + str(minute) + "分\n" + "出勤確認しました。今日も頑張りましょう！"
            else:
                work_time, in_time, out_time, overwork = labor_time(obj.staff.id)
                if work_time == "unknown":
                    comment = "打刻エラー: 出勤打刻をしてください。"
                    #最新のレコードを削除
                    SubmitAttendance.objects.filter(id=obj.id, staff_id=obj.staff.id).delete()
                else:
                    comment = str(month) + "月" + str(day) +"日" + str(hour) + "時" + str(minute) + "分\n" + "退勤確認しました。\n"\
                        "労働時間は" + str(work_time.seconds // 3600) + "時間"+ str((work_time.seconds % 3600) // 60) + "分です。"\
                                            + "お疲れ様でした\(^o^)/！"
                if overwork:
                    work_time = str(work_time.seconds // 3600) + ":"+ str((work_time.seconds % 3600) // 60)
                    obj_over = OverWorkTime.objects.create(
                        staff = obj.staff,
                        date_time_in = str(in_time),
                        date_time_out = str(out_time),
                        worktime = work_time
                    )
                    obj_over.save()
                    comment_add = "働きすぎです。超過労働リストに登録されました。"
        else:
            in_out_list = ["退勤", "出勤"]
            comment = "打刻エラー: " + str(in_out_list[int(obj.in_out) - 1]) + "打刻を忘れているか打刻ミスをしています。"
            form_err = SubmitErrForm
            context = {
                'form_err': form_err,
                'comment': comment
                }
            return render(request, 'attend/push_err.html', context)
        context = {
                'comment': comment,
                'comment_add': comment_add
            }
        return render(request, 'attend/result.html', context)
result = ResultView.as_view()

#打刻エラーの原因をpostする
class ResultErrView(View):
    def post(self, request):
        form_err = SubmitErrForm(request.POST)
        obj_err = form_err.save(commit=False)
        obj_err.staff = request.user
        obj_err.err_cause = request.POST["err_cause"]
        in_out_list = ["退勤", "出勤"]
        if request.POST["err_cause"] == '2':
            obj = SubmitAttendance.objects.all().filter(staff_id=obj_err.staff.id).order_by("id").reverse()[0]
            obj.in_out = str(abs(int(obj.in_out) -1))
            #最新のレコードを削除
            SubmitAttendance.objects.all().filter(staff_id=obj_err.staff.id).order_by("id").reverse()[0].delete()
            obj.save()
            select = 2
            comment = str(in_out_list[int(obj.in_out)]) + "打刻が完了しました。"
            context = {
            "select": select,
            "comment": comment
            }
        else:
            select = 1
            form_forget = SubmitForgetForm
            comment = "忘れていた打刻時間を記入して、管理者に報告してください。"
            context = {
                "select": select,
                "comment": comment,
            'form_forget': form_forget
            }
        return render(request, 'attend/result_err.html', context)
result_err = ResultErrView.as_view()

#打刻を忘れた時刻をpostする
class ResultForgetView(View):
    def post(self, request):
        form_forget = SubmitForgetForm(request.POST)
        obj_forget = form_forget.save(commit=False)
        obj_forget.staff = request.user
        obj = SubmitAttendance.objects.all().filter(staff_id=obj_forget.staff.id).order_by("id").reverse()[0]
        obj_forget.in_out = str(abs(int(obj.in_out) -1))
        obj_forget.date_time_forget = request.POST["date_time_forget"]
        obj_forget.save()
        comment = "送信されました。" + "打刻忘れを管理者に報告してください。"
        context = {
            "comment": comment
        }
        return render(request, 'attend/result_forget.html', context)
result_forget = ResultForgetView.as_view()