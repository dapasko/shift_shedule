from shift_calculation import calculate_shift_hours
import pandas as pd


def redistribute_shifts(forecast_dict, movable_schedule_df, fixed_schedule_df, max_iter=100000):
    """
    Итеративно перераспределяет рабочие смены для соответствия прогнозу.

    :param forecast_dict: dict{date: часы прогноза}
    :param movable_schedule_df: DataFrame со сменами, которые можно двигать
    :param fixed_schedule_df: DataFrame со сменами, которые нельзя двигать
    :param max_iter: максимальное число итераций
    :return: (updated_schedule_df, shift_changes, moves_log)
    """
    # Объединяем расписания
    full_df = pd.concat([movable_schedule_df.copy(), fixed_schedule_df.copy()], ignore_index=True)
    # Добавляем столбец часов
    full_df['_hours'] = full_df['Значение'].apply(calculate_shift_hours)

    # Функция для вычисления дельт
    def compute_deltas(df):
        scheduled = df.groupby('Дата')['_hours'].sum().to_dict()
        return {date: forecast_dict.get(date, 0) - scheduled.get(date, 0) for date in forecast_dict}

    deltas = compute_deltas(full_df)
    shift_changes = [f"{d.strftime('%Y-%m-%d')} — исходное отклонение: {delta:.2f} ч" for d, delta in deltas.items()]
    moves_log = []

    # Итеративная балансировка
    for _ in range(max_iter):
        # выбираем день с макс |дельта|
        day_worst, delta_worst = max(deltas.items(), key=lambda x: abs(x[1]))
        if abs(delta_worst) < 0.5:
            break

        if delta_worst < 0:
            # избыток на day_worst, ищем день с наибольшим дефицитом
            day_def, delta_def = max(deltas.items(), key=lambda x: x[1])
            if delta_def <= 0:
                break
            # выбираем малую смену для переноса
            candidates = full_df[(full_df['Дата'] == day_worst) &
                                (full_df['WFM ID'].isin(movable_schedule_df['WFM ID']))]
            candidates = candidates[candidates['_hours'] > 0]
            if candidates.empty:
                break
            cand = candidates.sort_values('_hours').iloc[0]
            idx = cand.name
            # перенос
            full_df.at[idx, 'Дата'] = day_def
            moves_log.append(f"WFM ID {cand['WFM ID']}: {day_worst.strftime('%Y-%m-%d')} → {day_def.strftime('%Y-%m-%d')}")
        else:
            # дефицит на day_worst, ищем день с наибольшим избытком
            day_surp, delta_surp = min(deltas.items(), key=lambda x: x[1])
            if delta_surp >= 0:
                break
            candidates = full_df[(full_df['Дата'] == day_surp) &
                                (full_df['WFM ID'].isin(movable_schedule_df['WFM ID']))]
            candidates = candidates[candidates['_hours'] > 0]
            if candidates.empty:
                break
            cand = candidates.sort_values('_hours').iloc[0]
            idx = cand.name
            full_df.at[idx, 'Дата'] = day_worst
            moves_log.append(f"WFM ID {cand['WFM ID']}: {day_surp.strftime('%Y-%m-%d')} → {day_worst.strftime('%Y-%m-%d')}")

        deltas = compute_deltas(full_df)

    # Финальные дельты
    final_deltas = compute_deltas(full_df)
    shift_changes.append("\nИтоговые отклонения после балансировки:")
    for d, delta in final_deltas.items():
        shift_changes.append(f"{d.strftime('%Y-%m-%d')} — отклонение: {delta:.2f} ч")

    updated_schedule_df = full_df.drop(columns=['_hours'])
    return updated_schedule_df, shift_changes, moves_log
