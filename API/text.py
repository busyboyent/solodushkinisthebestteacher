class Text:

    token_error = "проверьте токен и в случае необходимости обновите\n"
    command_error = (
        "проверьте корректность отправляемого запроса (обратитесь к help)\n"
    )
    help_start = ("для сброса token запустите программу с" +
                  " параметром reset\nпример: main.py reset\n\n" +
                  "для выбора хранилища введите его название в " +
                  "качестве параметра\nпример: main.py yandex\n" +
                  "или запустите программу и следуйте" +
                  " дальнейшим инструкциям\n\n" +
                  "список команд доступных после запуска:\n" +
                  "mkdir создать директорию Пример: mkdir; fold\n" +
                  "remove удалить файл/директорию" +
                  " Пример: remove; fold\n" +
                  "ls\n" +
                  "download скачать файл" +
                  " Пример: download; /path; filename\n" +
                  "upload загрузить файл " +
                  "Пример: upload; file; /path/filename\n" +
                  "lls\n" +
                  "catalog загрузить каталог" +
                  "Пример: catalog; folder\n" +
                  "exit Введите exit для выхода" +
                  "archive архивирует файл и заливает его на диск " +
                  "Пример: archive; file; /path/filename\n" +
                  "unpack разпаковывает архив\n" +
                  "\nSPECIAL FOR MAKS: archive; sky.py; /sky.zip\n" +
                  "upload; sky.py; /sky.py\n" +
                  "после этих команд можно проверить download\n" +
                  "download; /sky.py; sky1.py")
