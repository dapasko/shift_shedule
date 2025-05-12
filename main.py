import pandas as pd
from data_loader import load_forecast_data, load_schedule_data
from shift_calculation import calculate_total_hours_for_day
from shift_redistribution import redistribute_shifts
from distribution_correction import correct_schedule_distribution
from logger import log_changes
from export_schedule import export_schedule_to_excel


def main():
    # Пути к файлам
    forecast_file_path = 'Forecast.xlsx'
    schedule_file_path = 'расписание.xlsx'

    # Загружаем данные
    forecast_df = load_forecast_data(forecast_file_path)
    movable_schedule_df, fixed_schedule_df = load_schedule_data(schedule_file_path)

    # Лог часов до перераспределения
    shift_changes = []
    for date in forecast_df.index:
        hours_before = calculate_total_hours_for_day(pd.concat([movable_schedule_df, fixed_schedule_df], ignore_index=True), date)
        needed = forecast_df.at[date, 'Прогноз']
        shift_changes.append(
            f"{date.strftime('%Y-%m-%d')}: нужно {needed:.2f} ч, запланировано до {hours_before:.2f} ч"
        )

    # Перераспределение смен
    forecast_dict = forecast_df['Прогноз'].to_dict()
    updated_schedule_df, redistribute_log, moves_log = redistribute_shifts(
        forecast_dict,
        movable_schedule_df,
        fixed_schedule_df
    )

    # Лог дефицитов/избытков после перераспределения (до анализа)
    shift_changes.append("\nПосле перераспределения (дефицит/избыток):")
    shift_changes += redistribute_log

    # Лог основных пересчетов часов по дням после перераспределения
    shift_changes.append("\nИтоговые часы после перераспределения:")
    for date in forecast_df.index:
        hours_after = calculate_total_hours_for_day(updated_schedule_df, date)
        needed = forecast_df.at[date, 'Прогноз']
        shift_changes.append(
            f"{date.strftime('%Y-%m-%d')}: нужно {needed:.2f} ч, запланировано после {hours_after:.2f} ч"
        )

    # Общая корректировка распределения (анализ)
    shift_changes.append("\nАнализ отклонений (после):")
    shift_changes += correct_schedule_distribution(forecast_df, updated_schedule_df[updated_schedule_df['WFM ID'].isin(movable_schedule_df['WFM ID'])], fixed_schedule_df)

    # Добавляем в лог информацию о конкретных переносах
    shift_changes.append("\nПереносы смен:")
    shift_changes.extend(moves_log)

    # Логирование всех изменений
    log_changes(shift_changes)

    # Экспорт итогового расписания
    output_file = 'расписание_результат.xlsx'
    full_original = pd.concat([movable_schedule_df, fixed_schedule_df], ignore_index=True)
    export_schedule_to_excel(updated_schedule_df, full_original, output_file)

if __name__ == '__main__':
    main()
