"""入力された時間をpandasで処理"""
import pandas as pd
import sqlite3
import datetime

#データベースから打刻情報を取得
def data_get(staff_id):
    with sqlite3.connect("db.sqlite3") as conn:
        df = pd.read_sql('select * from attend', con=conn)
    df_staff = df[df["staff_id"] == staff_id]
    date_time = []
    for date,time in zip(df_staff["date"], df_staff["time"]):
        date_time.append(date_time_combine(date, time))
    df_staff["date_time"] = date_time
    df_time_up = df_staff.sort_values('date_time', ascending=False)
    df_time_up.reset_index(drop=True, inplace=True)
    return df_time_up

#bool: 直近の打刻と今回の打刻の出退勤が一致していればFalse, そうでなければTrue
#bool_time: 直近の打刻と今回の打刻の時間差が5分以下ならTrue->打刻エラーへ
def KintaiCheck(staff_id):
    bool = True
    bool_time = False
    df_time_up = data_get(staff_id)
    if len(df_time_up["in_out"]) > 1:
        if df_time_up["in_out"][0] == df_time_up["in_out"][1]:
            bool = False
        td = df_time_up["date_time"][0] - df_time_up["date_time"][1]
        if int(td.total_seconds()) <= 300: #5 min
            bool_time = True
    return bool, bool_time

#日付と時間を統合
def date_time_combine(date, time):
    """date,time->str"""
    date1 = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    time1 = datetime.datetime.strptime(str(time), '%H:%M:%S').time()
    return datetime.datetime.combine(date1, time1)

#労働時間を計算
def labor_time(staff_id):
    overwork = False
    df_time_up = data_get(staff_id)
    if len(df_time_up["in_out"]) > 1:
        td = df_time_up["date_time"][0] - df_time_up["date_time"][1]
        if int(td.total_seconds()) >= 3600 * 7:  #7hours
            overwork = True
        return td, df_time_up["date_time"][1], df_time_up["date_time"][0], overwork
    else:
        unknown = "unknown"
        return unknown, unknown, unknown, overwork



if __name__ == "__main__":
    print(KintaiCheck(2))
