from django.db import models
from django.contrib.auth import get_user_model

#勤怠管理model
class SubmitAttendance(models.Model):

    class Meta:
        db_table = 'attend'
        verbose_name = '勤怠管理'
        verbose_name_plural = '勤怠管理'
    
    
    IN_OUT = (
        (1, '出勤'),
        (0, '退勤'),
    )
    staff = models.ForeignKey(get_user_model(), verbose_name="スタッフ", on_delete=models.CASCADE, default=None)
    in_out = models.IntegerField(verbose_name='出勤/退勤', choices=IN_OUT, default=None)
    time = models.TimeField(verbose_name="打刻時間")
    date = models.DateField(verbose_name='打刻日')

#打刻エラーmodel
class SubmitError(models.Model):
    class Meta:
        db_table = 'submit_err'
        verbose_name = 'エラー'
        verbose_name_plural = 'エラー'
    ERR_CAUSE = (
        (1, '打刻忘れ'),
        (2, '打刻ミス')
    )
    staff = models.ForeignKey(get_user_model(), verbose_name="スタッフ", on_delete=models.CASCADE, default=None)
    err_cause = models.IntegerField(verbose_name='ERR_CAUSE', choices=ERR_CAUSE, default=None)

#働き過ぎを記録するmodel
class OverWorkTime(models.Model):
    class Meta:
        db_table = 'OverWork'
        verbose_name = '働きすぎリスト'
        verbose_name_plural = '働きすぎリスト'
    staff = models.ForeignKey(get_user_model(), verbose_name="スタッフ", on_delete=models.CASCADE, default=None)
    date_time_in = models.DateTimeField(verbose_name="出勤時間")
    date_time_out = models.DateTimeField(verbose_name="退勤時間")
    worktime = models.CharField(verbose_name="労働時間", max_length=5)

#打刻忘れを記録するmodel
class SubmitForget(models.Model):
    class Meta:
        db_table = 'DakokuForget'
        verbose_name = '打刻忘れリスト'
        verbose_name_plural = '打刻忘れリスト'
    IN_OUT = (
        (1, '出勤'),
        (0, '退勤'),
    )
    staff = models.ForeignKey(get_user_model(), verbose_name="スタッフ", on_delete=models.CASCADE, default=None)
    in_out = models.IntegerField(verbose_name='出勤/退勤', choices=IN_OUT, default=None)
    date_time_forget = models.DateTimeField(verbose_name="忘れた打刻時間")
