from shift_calculation import calculate_shift_hours
import pandas as pd


def correct_schedule_distribution(forecast_df, movable_schedule_df, fixed_schedule_df):
    """
    Корректирует общее распределение смен, стараясь приблизить расписание к прогнозу по общим часам.
    Возвращает лог изменений.
    """
    shift_changes = []

    # Объединяем оба расписания для анализа общего числа часов
    full_schedule_df = pd.concat([movable_schedule_df, fixed_schedule_df])

    # Группируем по дате и суммируем часы
    scheduled_hours_per_day = (
        full_schedule_df.groupby('Дата')['Значение']
        .apply(lambda shifts: sum(calculate_shift_hours(s) for s in shifts))
    )

    forecast_hours_per_day = forecast_df['Прогноз']

    # Вычисляем отклонения
    daily_deltas = (scheduled_hours_per_day - forecast_hours_per_day).fillna(0)

    # Считаем среднюю нехватку/перераспределение
    total_forecast = forecast_hours_per_day.sum()
    total_scheduled = scheduled_hours_per_day.sum()
    delta_total = total_scheduled - total_forecast

    shift_changes.append(f"Прогноз всего: {total_forecast:.2f} ч | Запланировано всего: {total_scheduled:.2f} ч | Δ: {delta_total:.2f} ч")

    # Если нужно, можно добавить распределение отклонения равномерно по дням
    average_delta = delta_total / len(forecast_df)

    shift_changes.append(f"Среднее отклонение по дням: {average_delta:.2f} ч")

    # Пока просто логируем дисбаланс — перераспределение делается в shift_redistribution
    for date, delta in daily_deltas.items():
        shift_changes.append(f"{date.strftime('%Y-%m-%d')} — отклонение: {delta:.2f} ч")

    return shift_changes
