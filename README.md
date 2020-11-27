# TeamWork_replacer
Documentation: https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork 

## Тесты
Для проверки подстановок в файле replacer_test.py написаны тесты.
Рекомендуется для каждой новой функции или при обнаружении нового бага сперва писать тест.

### Модульные тесты
Запуск
```bash
cd script
# Тесты ссылок на Teamwork
python -m unittest test_teamwork_replacer.py
# Тесты ссылок на Confluence
python -m unittest test_confluence_replacer.py
# Комбинированные тесты ссылок
python -m unittest test_combo_links.py
# Тесты подстановок значений по шаблону
python -m unittest test_values_replacer.py
```

### Тест на устойчивость
Сервис запускается с любыми не рабочими параметрами, но допустимыми параметрами.
Например, в качестве адреса Teamwork и Confluence передаем 127.0.0.1. Для номера порта и уровня логирования указывается только число: для порта любой доступный, с учетом ограничения доступности части из них только root; для логов одно из допустимых, но лучше 10, чтобы получить наибольшее кол-во сообщений.
Пример:
```bash
python main.py --teamwork-domain netping.teamwork.com --teamwork-token token --confluence-domain netping.atlassian.net --confluence-login login --confluence-token token --host "0.0.0.0" --log-level 10
```
Далее запускаем проверку запросов
```bash
python test_request.py --host 127.0.0.1 --port 8431
```
Используется тот же интерпритатор, так как test_request.py требует для работы библиотеки requests.

Скрипт выполняет два запроса:
- первый с нормальными данными, но поскольку изначально запущенному сервису указаны неверные параметры, то получить данные по найденным ссылкам нельзя;
- второй с ошибочными данными. В получаемом json на верхнем уровне должен быть ключ task(для задач) или comment(для комментариев). В данном же запросе прилетает wrong_type.

В консоль должны быть выведены две строки, подтверждающие, что сервер, хоть и не смог обработать ни один из запросов, не упал и смог ответитьза запрос(статус 200):
```bash
<Response [200]>
<Response [200]>
```
