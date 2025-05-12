from datetime import datetime, timedelta

def calculate_shift_hours(shift_type):
    """
    Подсчитывает количество рабочих часов для каждого типа смены.

    :param shift_type: Тип смены (например, '09:00-18:00', '22:00-07:00').
    :return: Количество рабочих часов с учётом коэффициентов.
    """
    if not isinstance(shift_type, str):
        return 0.0

    shift_type = shift_type.strip()

    # Нерабочие значения
    if shift_type in ['Отпуск', 'Больничный', 'День группы']:
        return 0.0

    # Явные шаблоны
    if shift_type == '09:00-18:00':
        return 7.66
    elif shift_type == '12:00-00:00':
        return 11.33
    elif shift_type == '04:30-15:00':
        return 4.0
    elif shift_type == '22:00-07:00':
        return 11.33

    # Расчёт по времени
    if '-' not in shift_type:
        return 0.0

    try:
        start_time, end_time = shift_type.split('-')
        start_dt = datetime.strptime(start_time, '%H:%M')
        end_dt = datetime.strptime(end_time, '%H:%M')
    except ValueError:
        return 0.0

    if end_dt <= start_dt:
        end_dt += timedelta(days=1)

    total_hours = (end_dt - start_dt).total_seconds() / 3600

    # Округления к стандартным длительностям
    if abs(total_hours - 9) < 1:
        return 7.66
    elif abs(total_hours - 12) < 1:
        return 11.33
    elif abs(total_hours - 4.5) < 1:
        return 4.0

    return total_hours


def calculate_total_hours_for_day(schedule_df, date):
    """
    Подсчитывает общее количество рабочих часов для конкретного дня.

    :param schedule_df: DataFrame с расписанием.
    :param date: Дата, для которой нужно подсчитать часы.
    :return: Общее количество рабочих часов для данного дня.
    """
    scheduled_shifts = schedule_df[schedule_df['Дата'] == date]
    total_hours = 0.0

    for _, row in scheduled_shifts.iterrows():
        shift_type = row['Значение']
        total_hours += calculate_shift_hours(shift_type)

    return total_hours
