<!-- @format -->

# LogScan

LogScan — консольная утилита на Python для анализа лог-файлов, поиска IPv4-адресов и SHA256-хэшей.

Программа проверяет найденные индикаторы через VirusTotal API или в тестовом Mock-режиме и сохраняет результаты в JSON или CSV.

## Структура проекта

```text
logscan/
├── main.py
├── requirements.txt
├── README.md
├── modules/
│   ├── log_parser.py
│   ├── virustotal.py
│   └── report_generator.py
├── logs/
│   └── sample.log
└── output/
```

Назначение основных файлов:

- `main.py` — запуск программы и обработка аргументов.
- `log_parser.py` — поиск IP-адресов и SHA256-хэшей.
- `virustotal.py` — проверка через VirusTotal API и Mock.
- `report_generator.py` — создание JSON и CSV-отчётов.
- `requirements.txt` — зависимости проекта.
- `logs/` — исходные лог-файлы.
- `output/` — отчёты и журнал работы программы.

## 1. Скачивание проекта

Для работы потребуется установленный Python.

Проверка версии:

```powershell
python --version
```

Скачать проект можно двумя способами.

### Способ 1. Через Git

Для этого необходим установленный Git.

Откройте PowerShell и выполните:

```powershell
git clone https://github.com/n1ckdevops/logscan.git
```

Git скачает репозиторий в папку `logscan`.

### Способ 2. Скачать ZIP

1. Откройте страницу репозитория на GitHub.
2. Нажмите `Code` → `Download ZIP`.
3. Распакуйте архив в удобное место.

## 2. Открытие проекта

После скачивания перейдите в папку проекта через терминал.

Если проект скачан через Git:

```powershell
cd logscan
```

Если проект скачан через ZIP, откройте терминал в распакованной папке или перейдите в неё через `cd`.

Проверьте содержимое:

```powershell
dir
```

В папке должны находиться `main.py`, `requirements.txt` и остальные файлы проекта.

**Важно:** все дальнейшие команды выполняются из папки, содержащей `main.py`.

## 3. Установка зависимостей

В терминале выполните:

```powershell
python -m pip install -r requirements.txt
```

Команда установит необходимые библиотеки, включая `requests` для работы с VirusTotal API.

## 4. Подготовка лог-файла

LogScan автоматически ищет в текстовых файлах:

- IPv4-адреса.
- SHA256-хэши.

Для первого запуска используйте готовый файл:

```text
logs/sample.log
```

Также можно создать собственные тестовые файлы.

**Пример файла с IP-адресом:**

```powershell
Set-Content logs/ip_test.log "8.8.8.8"
```

**Пример файла с SHA256-хэшем:**

```powershell
Set-Content logs/hash_test.log "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
```

Программа автоматически определяет найденные индикаторы. Отдельно выбирать IP или SHA256 не требуется.

## 5. Выбор режима проверки

LogScan поддерживает два режима работы.

### Mock — тестовый режим

Mock позволяет использовать программу без API-ключа и подключения к VirusTotal.

Результаты проверки заранее подготовлены и не являются реальными данными об угрозах.

Mock-функции находятся в:

```text
modules/virustotal.py
```

- `mock_check_ip()` — тестовая проверка IP.
- `mock_check_hash()` — тестовая проверка SHA256.

Если в терминале ранее был установлен API-ключ, удалите его из текущей сессии:

```powershell
Remove-Item Env:VT_API_KEY -ErrorAction SilentlyContinue
```

**Запуск в Mock-режиме:**

```powershell
python main.py -log-file logs/sample.log -format json -output output/report.json
```

### VirusTotal — настоящая проверка

Этот режим отправляет запросы к VirusTotal API.

**Шаг 1. Получите API-ключ**

1. Перейдите на https://www.virustotal.com/.
2. Создайте аккаунт или авторизуйтесь.
3. Откройте настройки аккаунта.
4. Найдите свой API-ключ.

**Шаг 2. Подключите API-ключ**

В PowerShell выполните:

```powershell
$secureKey = Read-Host "VirusTotal API key" -AsSecureString
$env:VT_API_KEY = [System.Net.NetworkCredential]::new("", $secureKey).Password
```

Введите API-ключ по запросу.

**Шаг 3. Проверьте подключение**

```powershell
python -c "import os; print(bool(os.getenv('VT_API_KEY')))"
```

Если вывод:

```text
True
```

Python видит переменную окружения. Это ещё не подтверждает успешную авторизацию в VirusTotal.

**Шаг 4. Запустите проверку IP**

```powershell
python main.py -log-file logs/ip_test.log -format json -output output/ip_report.json
```

**Или проверку SHA256**

```powershell
python main.py -log-file logs/hash_test.log -format json -output output/hash_report.json
```

Если API-ключ доступен, программа использует VirusTotal вместо Mock.

**Важно:**

- Не публикуйте API-ключ в GitHub.
- Не храните ключ непосредственно в исходном коде.
- Учитывайте ограничения запросов VirusTotal.
- Переменная, заданная через PowerShell таким способом, действует в текущей сессии терминала.

## 6. Запуск программы

Общая команда:

```powershell
python main.py -log-file ПУТЬ_К_ЛОГУ -format ФОРМАТ -output ПУТЬ_К_ОТЧЁТУ
```

Параметры:

| Аргумент    | Назначение             | По умолчанию            |
| ----------- | ---------------------- | ----------------------- |
| `-log-file` | Путь к лог-файлу       | Обязательный            |
| `-api-key`  | Ключ VirusTotal        | Переменная `VT_API_KEY` |
| `-format`   | Формат CSV или JSON    | csv                     |
| `-output`   | Путь сохранения отчёта | output/report.csv       |

### Пример запуска с JSON

```powershell
python main.py -log-file logs/sample.log -format json -output output/report.json
```

Программа прочитает `sample.log`, найдёт IP и SHA256, выполнит проверки и сохранит JSON-отчёт в папку `output`.

### Пример запуска с CSV

```powershell
python main.py -log-file logs/sample.log -format csv -output output/report.csv
```

### Короткий запуск

```powershell
python main.py -log-file logs/sample.log
```

В этом случае используется формат CSV и стандартный путь `output/report.csv`.

Режим проверки зависит от наличия API-ключа.

## 7. Просмотр результатов

Все отчёты сохраняются в папку, указанную параметром `-output`.

### JSON-отчёт

Для просмотра через PowerShell:

```powershell
Get-Content output/report.json
```

Пример записи с тестовыми данными:

```json
[
  {
    "type": "IP",
    "value": "8.8.8.8",
    "result": {
      "malicious": 2,
      "suspicious": 1,
      "harmless": 65,
      "undetected": 10
    },
    "date": "2026-11-11 12:00:00"
  }
]
```

Описание полей:

- `type` — тип индикатора: IP или HASH.
- `value` — найденный IP-адрес или SHA256.
- `result` — результаты проверки.
- `date` — дата формирования отчёта.

Если `result` равен `null`, результат проверки не был получен.

### CSV-отчёт

CSV содержит найденные индикаторы и статистику их проверки.

Файл можно открыть в Excel или текстовом редакторе.

### Журнал работы

LogScan записывает события и ошибки в `logscan.log`.

При стандартном пути отчёта журнал находится здесь:

```text
output/logscan.log
```

Для просмотра последних десяти записей:

```powershell
Get-Content output/logscan.log -Tail 10
```

В журнале фиксируются запуск программы, количество найденных индикаторов, выбранный режим, сохранение отчёта и ошибки файловых операций.

## 8. Справка

Для просмотра доступных аргументов выполните:

```powershell
python main.py -h
```
