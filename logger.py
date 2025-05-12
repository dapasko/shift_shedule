def log_changes(shift_changes, log_file_path='shift_changes_log.txt'):
    """
    Записывает изменения перераспределения смен в лог-файл.

    :param shift_changes: Список изменений смен.
    :param log_file_path: Путь к файлу, куда будут записаны изменения.
    """
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for change in shift_changes:
            log_file.write(change + '\n')

def main():
    # Пример использования
    shift_changes = [
        "Изменение 1: Перенос смены с 2025-06-01 на 2025-06-02",
        "Изменение 2: Добавлена смена на 2025-06-02"
    ]
    log_changes(shift_changes)


if __name__ == "__main__":
    main()
