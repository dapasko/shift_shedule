import pandas as pd


def export_schedule_to_excel(updated_schedule_df, original_schedule_df, output_file_path):
    """
    Экспортирует скорректированное расписание в Excel-файл, сохраняя все исходные колонки и формат.

    :param updated_schedule_df: DataFrame с новыми значениями столбца 'Значение' для каждой строки расписания.
    :param original_schedule_df: Исходный DataFrame, чтобы сохранить все колонки (WFM ID, Делаем переносы и т.д.).
    :param output_file_path: Путь к выходному Excel-файлу.
    """
    # Копируем исходный DataFrame, чтобы не потерять структуру
    result_df = original_schedule_df.copy()

    # Обновляем столбец 'Значение' в результирующем DataFrame
    # Предполагается, что updated_schedule_df содержит столбцы ['WFM ID', 'Значение']
    result_df = result_df.merge(
        updated_schedule_df[['WFM ID', 'Значение']],
        on='WFM ID',
        how='left',
        suffixes=('', '_new')
    )

    # Если есть новое значение, заменяем старое
    result_df['Значение'] = result_df['Значение_new'].combine_first(result_df['Значение'])
    result_df.drop(columns=['Значение_new'], inplace=True)

    # Экспорт в Excel
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False)

    print(f"Расписание экспортировано в {output_file_path}")
