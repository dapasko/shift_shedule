import pandas as pd


def load_forecast_data(forecast_file_path):
    """
    Загружает данные о прогнозе из Excel файла.

    :param forecast_file_path: Путь к файлу прогноза.
    :return: DataFrame с данными прогноза.
    """
    forecast_df = pd.read_excel(forecast_file_path)
    forecast_df['Дата'] = pd.to_datetime(forecast_df['Дата'], format='%Y-%m-%d')
    forecast_df.set_index('Дата', inplace=True)
    return forecast_df


def load_schedule_data(schedule_file_path):
    """
    Загружает данные о расписании сотрудников из Excel файла.

    :param schedule_file_path: Путь к файлу расписания.
    :return: DataFrame с данными расписания.
    """
    schedule_df = pd.read_excel(schedule_file_path)
    schedule_df['Дата'] = pd.to_datetime(schedule_df['Дата'], format='%Y-%m-%d')

    # Фильтрация на "можно двигать" и "нельзя двигать"
    movable_schedule_df = schedule_df[schedule_df['Делаем переносы'] != 'нельзя двигать']
    fixed_schedule_df = schedule_df[schedule_df['Делаем переносы'] == 'нельзя двигать']

    return movable_schedule_df, fixed_schedule_df


def main():
    # Укажите пути к вашим файлам Excel
    forecast_file_path = 'Forecast.xlsx'
    schedule_file_path = 'расписание.xlsx'

    forecast_df = load_forecast_data(forecast_file_path)
    movable_schedule_df, fixed_schedule_df = load_schedule_data(schedule_file_path)

    print("Данные о прогнозе загружены:")
    print(forecast_df.head())

    print("Данные о расписании (можно двигать):")
    print(movable_schedule_df.head())

    print("Данные о расписании (нельзя двигать):")
    print(fixed_schedule_df.head())


if __name__ == "__main__":
    main()
