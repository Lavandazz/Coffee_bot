import logging
import os

log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)


def setup_logging():
    """ Main logger """
    log_file_path = os.path.join(log_folder, "py_log.log")  # путь к файлу

    # Убираем вызов basicConfig, чтобы настройки выполнялись через обработчики
    main_logger = logging.getLogger('main')  # Получаем глобальный логгер
    main_logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования

    if not main_logger.hasHandlers():
        # Консольный обработчик главного логера
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Файловый обработчик
        main_file_handler = logging.FileHandler(log_file_path, mode='w')
        main_file_handler.setLevel(logging.INFO)

        # Формат для логов
        main_formatter = logging.Formatter('%(levelname)s - %(asctime)s - [%(name)s] - '
                                           '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
        console_handler.setFormatter(main_formatter)
        main_file_handler.setFormatter(main_formatter)

        # Добавляем обработчики к логгеру
        main_logger.addHandler(console_handler)
        main_logger.addHandler(main_file_handler)

        # Логирование в самом конце, чтобы отобразить сообщение
        main_logger.info("Логирование настроено успешно.")

    return main_logger
