"""
Teamwork replacer

Replace urls to another tasks on teamwork
and urls to articles om confluence with their titles.
"""

import argparse
import re
import logging
import traceback
import requests
from bottle import Bottle, request


VERSION = '3.9'

formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')

log = logging.getLogger("main")
log_handler = logging.FileHandler("log.txt", encoding='utf8')
log_handler.setFormatter(formatter)
log.addHandler(log_handler)

errors = logging.getLogger("errors")
errors_handler = logging.FileHandler("errors.txt", encoding='utf8')
errors_handler.setFormatter(formatter)
errors.addHandler(errors_handler)


def get_teamwork_regexp(domain):
    """
    Generate regexp for parsing urls to Teamwork for domain.

    Args:
        - domain -- Teamwork domain without protocols and uri.
                    Example, netping.teamwork.com
    """
    # return (r'(?P<link>[^(\"\']http[s]{,1}://%s/'
    #         r'[#/]{,3}[projects/[0-9]{,15}]?tasks/(?P<id>[0-9]{,15})'
    #         r'[\?c=[0-9]{,15}]{,1})') % (domain.replace(r'.', r'\.'))
    return (r'(?P<link>[^(\"\']http[s]?://%s/'
            r'#?/?(projects/[0-9]+/)?tasks/(?P<id>[0-9]+)'
            r'(\?c=[0-9]+)?)') % (domain.replace(r'.', r'\.'))


def get_confluence_regexp(domain):
    """
    Generate regexp for parsing urls to Confluence for domain.

    Args:
        - domain -- Confluence domain without protocols and uri.
                    Example, netping.atlassian.net
    """
    return (r'(?P<link>[^(\"\']http[s]{,1}://%s'
            r'/wiki/spaces/[a-zA-Z0-9]+/pages/(?P<id>[0-9]+)'
            r'[/\w\.\,\+\-\_]*)') % (domain.replace(r'.', r'\.'))


def argument_parser():
    """
    Get CLI arguments parser

    return parser, argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description=f'Teamwork replacer {VERSION}.')
    parser.add_argument('--teamwork-domain', type=str, required=True,
                        help='Teamwork domain. Example, smthn.teamwork.com')
    parser.add_argument('--teamwork-token', type=str, required=True,
                        help='Teamwork token')
    parser.add_argument('--confluence-domain', type=str, required=True,
                        help='Confluence domain. Example, smthn.atlassian.net')
    parser.add_argument('--confluence-login', type=str, required=True,
                        help='Confluence login')
    parser.add_argument('--confluence-token', type=str, required=True,
                        help='Confluence token')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help=('Server address to bind to. Pass 0.0.0.0 to '
                              'listens on all interfaces including the '
                              'external one. (default: 0.0.0.0)'))
    parser.add_argument('--port', type=int, default=8431,
                        help=('Server port to bind to. '
                              'Values below 1024 require root privileges. '
                              '(default: 8431)'))
    parser.add_argument('--log-level', type=int, default=10,
                        help=('Log level, integer value: 50 - critical, '
                              '40 - error, 30 - warning, 20 - info, '
                              '10 - debug, 0 - notset. (default: 10)'))
    return parser


def get_config():
    """
    Get parametrs from CLI

    return config, dict.
    """
    log.debug('Чтение параметров строки')
    args = argument_parser().parse_args()
    return {
        'general': {
            'log_level': args.log_level,
        },
        'teamwork': {
            'domain': args.teamwork_domain,
            'token': args.teamwork_token,
        },
        'confluence': {
            'domain': args.confluence_domain,
            'login': args.confluence_login,
            'token': args.confluence_token,
        },
        'route': {
            'host': args.host,
            'port': args.port,
        },
    }


def get_task_info(domain, token, task_id):
    """
    Get task info from Teamwork

    Args:
        - domain -- Teamwork domain without protocols and uri.
                    Example, netping.teamwork.com
        - token -- token for auth on Teamwork server
        - task_id -- task identifier

    Return full task info, dict.
    """
    log.info('Получение информации о задаче id:%s', str(task_id))
    task = requests.get(
        'https://{}/tasks/{}.json'.format(domain, task_id),
        auth=(token, '')).json()
    if task.get('error'):
        raise Exception(
            'Ошибка получения информации о задаче c id {} - {}'.format(
                task_id, task))
    log.debug('Получили информацию о задаче c id %s - %s',
              task_id, task)
    return task


def get_task_top_parent_id(domain, token, task_id):
    """
    Get top parent taks id.

    Args:
        - task_id -- processing task's id
    """
    log.info('Поиск родительской задачи id:%s', str(task_id))
    parent_id = task_id
    while True:
        taskinfo = get_task_info(domain, token, parent_id)
        if not taskinfo['todo-item']['parentTaskId']:
            break
        parent_id = taskinfo['todo-item']['parentTaskId']
    return parent_id


def update_task(domain, token, task_id, params):
    """
    Update task with identifier task_id with params

    Args:
        - domain -- Teamwork domain without protocols and uri.
                    Example, netping.teamwork.com
        - token -- token for auth on Teamwork server
        - task_id -- task identifier
        - params -- fields with new values for update.
                    Example, update task title(field description)
                    and body(field content):
                    {
                        'description': 'new text for body',
                        'content': 'new title',
                    }
    """
    log.info('Обновляем задачу id %s - %s', str(task_id), str(params))
    response = requests.put('https://{}/tasks/{}.json'.format(domain, task_id),
                            json={'todo-item': params},
                            headers={'Content-Type': 'application/json'},
                            auth=(token, '')).json()
    log.debug('Обновили задачу id %s - %s', str(task_id), str(response))
    return response


def update_comment(domain, token, comment_id, params):
    """
    Update comment with identifier comment_id with params

    Args:
        - domain -- Teamwork domain without protocols and uri.
                    Example, netping.teamwork.com
        - token -- token for auth on Teamwork server
        - comment_id -- comment identifier
        - params -- fields with new values for update.
                    Need content-type field in params if update text.
                    Usually content-type getting from current comment values.
                    Example, update comment text(field content):
                    {
                        'body': 'new text for body',
                        'content-type': 'HTML',
                    }
    """
    log.info('Обновляем комментарий id %s - %s', str(comment_id), str(params))
    response = requests.put('https://{}/comments/{}.json'.format(domain,
                                                                 comment_id),
                            json={'comment': params},
                            headers={'Content-Type': 'application/json'},
                            auth=(token, '')).json()
    log.debug('Обновили комментарий id %s - %s',
              str(comment_id), str(response))
    return response


def get_article_info(domain, login, token, article_id):
    """
    Get article info from Confluence.
    Working only with cloud confluence.

    Args:
        - domain -- Confluence domain without protocols and uri.
                    Example, netping.atlassian.net
        - login -- login for auth on Confluence server
        - token -- token for auth on Confluence server, not password!
        - article_id -- article identifier

    Return full article info, dict.
    """
    log.info('Получение информации о статье id:%s', str(article_id))
    article = requests.get(
        'https://{}/wiki/rest/api/content/{}'.format(domain, article_id),
        auth=(login, token))
    log.debug('Получили информацию о статье c id %s - %s',
              str(article_id), str(article))
    return article


def replace_ids(text, task_id, get_parent_id):
    """
    Replace in task title:
        - %id% with unique task number;
        - %idf% with unique parent task number, current if haven't parent.

    Args:
        - text -- original text
        - task_id -- task identifier
        - parent_id -- function for get task parent id

    return task title with raplaces str
    """
    log.info(('Замена шаблонов значениями: '
              'номер текущей задачи и верхней родительской'))
    parent_id = get_parent_id(task_id)
    replaces = (
        (r'%idf%', str(parent_id)),
        (r'%id%', str(task_id))
    )
    for rpl in replaces:
        text = text.replace(*rpl)
    return text


def replace_links(regexp, text, get_info, is_task):
    """
    Replace links by regexp with info getting by function get_info.

    Args:
        - regexp -- link regular expression, str;
        - text -- processing text, str;
        - get_info -- function for get info about content by id;
        - is_task -- processing text from task description(True)
                    or from comment(False), boolean.

    return processed text, str.
    """
    log.info('Замена ссылок')
    links = dict()
    regexp = re.compile(regexp)
    found = [(ln.group('link'), ln.group('id')) for ln in regexp.finditer(text)]
    log.info('Найденные ссылки - %s', str(found))
    for link, content_id in found:
        link = link.strip().strip('\n').strip('<').strip('>')
        if link not in links:
            try:
                links[link] = get_info(content_id)
            except Exception as exp:
                errors.error(
                    'Ошибка получения информации о сущности %s: %s',
                    str(content_id), str(exp))
                errors.error('Оригинальная ссылка: %s', str(link))
                errors.error(
                    'Ошибка получения информации о сущности %s: %s',
                    str(content_id), str(traceback.format_exc()))

    log.info('Ссылки с подставляемой информацией - %s', str(links))
    for link, title in links.items():
        if is_task:
            text = text.replace(link, f'[{title}]({link})')
        else:
            link = link.replace(r'.', r'\.').replace(r'+', r'\+').replace(
                r'?', r'\?').replace(r'=', r'\=')
            link_regexp = ((r'(<\s*a[\w\d\"\'\_\n\t\+/\\\.:\=\-\#\?\t\n\s]*>)'
                            r'([\w\d\"\'\_\n\t\+/\\\.:\=\-\#\?\t\n\s]*)?\s?') +
                           link + r'(\s.*)?' + r'(<\s*/\s*a\s*>)')
            text = re.sub(link_regexp, r'\2\1%s\4\3' % title, text)

    return text


def processing_task(config, task_id, title, text):
    """
    Proccessing task: replace urls and insert values by templates.

    Args:
        - config -- programs's settings from cli, dict
        - task_id -- receiving content's id, int/str
        - title -- content's title, str
        - text -- content's text, str

    Return none
    """
    log.info('Замена ссылок на Teamwork')
    text = replace_links(
        get_teamwork_regexp(config['teamwork']['domain']), text,
        lambda task_id: get_task_info(config['teamwork']['domain'],
                                      config['teamwork']['token'],
                                      task_id)['todo-item']['content'], True)

    log.info('Замена ссылок на Confluence')
    text = replace_links(
        get_confluence_regexp(config['confluence']['domain']), text,
        lambda article_id: get_article_info(config['confluence']['domain'],
                                            config['confluence']['login'],
                                            config['confluence']['token'],
                                            article_id)['title'], True)

    log.info('Подстановка значений по шаблону')
    title = replace_ids(title, task_id,
                        lambda task_id: get_task_top_parent_id(
                            config['teamwork']['domain'],
                            config['teamwork']['token'],
                            task_id))

    log.info('Обновление задачи id:%s', str(task_id))
    update_task(config['teamwork']['domain'],
                config['teamwork']['token'],
                task_id,
                {
                    'description': text,
                    'content': title,
                })


def processing_comment(config, task_id, comment_id, text, content_type):
    """
    Proccessing comment: replace urls and insert values by templates.

    Args:
        - config -- programs's settings from cli, dict
        - comment_id -- receiving content's id, int/str
        - text -- content's text, str
        - content_type -- content type need for update comment,
                          getting from request (comment.contentType), str

    Return none
    """
    log.info('Замена ссылок на Teamwork')
    text = replace_links(
        get_teamwork_regexp(config['teamwork']['domain']), text,
        lambda task_id: get_task_info(config['teamwork']['domain'],
                                      config['teamwork']['token'],
                                      task_id)['todo-item']['content'], False)

    log.info('Замена ссылок на Confluence')
    text = replace_links(
        get_confluence_regexp(config['confluence']['domain']), text,
        lambda article_id: get_article_info(config['confluence']['domain'],
                                            config['confluence']['login'],
                                            config['confluence']['token'],
                                            article_id)['title'], False)

    log.info('Получение информации о родительской задаче')
    task = get_task_info(config['teamwork']['domain'],
                         config['teamwork']['token'],
                         task_id)

    log.info('Обновление комментария id:%s', str(comment_id))
    update_comment(config['teamwork']['domain'],
                   config['teamwork']['token'],
                   comment_id,
                   {
                       'body': text,
                       'notify': '',
                       'content-type': content_type,
                   })

    log.info(('Обновление задачи родительской задачи, '
              'восстановление списка пользователей для уведомления'))
    update_task(config['teamwork']['domain'],
                config['teamwork']['token'],
                comment_id,
                {'commentFollowerIds': task['todo-item']['changeFollowerIds']})


def calback(config):
    """
    Base handler for processing requests:
        check type(task or comment) and call function for processing.

    Args:
        - config -- programs's settings from cli, dict
    """
    try:
        event = request.json
        log.debug('Входящий хук - %s', str(event))

        if 'task' not in event and 'comment' not in event:
            log.info(('Неизвестный тип, обработка невозможна. '
                      'Доступные типы: task, comment.'))
            errors.error(('Неизвестный тип, обработка невозможна. '
                          'Доступные типы: task, comment.'))
            errors.error('Запрос: %s', str(event))
            return

        if 'task' in event:
            processing_task(config,
                            event['task']['id'],
                            event['task']['content'],
                            event['task']['description'])
        else:
            processing_comment(config,
                               event['comment']['objectId'],
                               event['comment']['id'],
                               event['comment']['body'],
                               event['comment']['contentType'])
    except Exception as exp:
        errors.exception('Запрос: %s', str(request))
        errors.exception('Ошибка при обработке запроса - %s', str(exp))
        errors.exception(traceback.format_exc())


if __name__ == '__main__':
    try:
        settings = get_config()

        errors.setLevel(settings['general']['log_level'])
        log.setLevel(settings['general']['log_level'])

        app = Bottle()
        app.route('/webhook', ['POST'], lambda: calback(settings))

        print(f'Script started. Version {VERSION}')
        log.info('Поднимаем сервер %s', VERSION)

        app.run(host=settings['route']['host'],
                port=int(settings['route']['port']))
    except Exception as exp:
        print('При выполнении кода произошла ошибка - %s' % str(exp))
        traceback.print_exc()
        errors.exception('При выполнении кода произошла ошибка - %s', str(exp))
        errors.exception(traceback.format_exc())
    finally:
        print('Script ended.')
