import os
import re
import configparser
import logging
import traceback
import requests
from bottle import post, request, run

VERSION = '2.1'

#print('script started')

config = configparser.ConfigParser()
config.read('config.ini')

errors = logging.getLogger("errors")
log = logging.getLogger("main")

log_level = int(config['general']['log_level'])

errors.setLevel(log_level)
log.setLevel(log_level)

FH = logging.FileHandler("log.txt", encoding='utf8')
ERRORS_FH = logging.FileHandler("errors.txt", encoding='utf8')
log.addHandler(FH)
errors.addHandler(ERRORS_FH)

FORMATTER = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
FH.setFormatter(FORMATTER)
ERRORS_FH.setFormatter(FORMATTER)


def replace_ids(text, task_id, parent_id, config):
    """
    Replace in task title:
        - %id% with unique task number;
        - %idf% with unique parent task number, current if haven't parent.

    Args:
        - task - task object, recieved on webhook, dict;
        - config - config from ini file, dict;

    return task title with raplaces str
    """
    domain = config['teamwork']['domain']
    token = config['teamwork']['token']
    content_type = {'Content-Type': 'application/json'}

    if parent_id:
        while True:
            taskinfo = requests.get(
                'https://{}/tasks/{}.json'.format(domain, parent_id),
                auth=(token, '')).json()
            if not taskinfo['todo-item']['parentTaskId']:
                break
            parent_id = taskinfo['todo-item']['parentTaskId']
    else:
        parent_id = task_id
        
    return task['task']['name'].replace('\%idf\%', parent_id).replace(
        '\%id\%', task_id)


def replace_confluence_links(text, config, task):
    """
    Replace url to Confluence with article title.
    Working only with cloud confluence.

    Args:
        - text - processing text, str;
        - config - config from ini file, dict;
        - is_task - processing text from task description(True)
                    or from comment(False), boolean;

    return processed text, str.
    """
    domain = config['confluence']['domain']
    login = config['confluence']['login']
    token = config['confluence']['token']
    content_type = {'Content-Type': 'application/json'}

    regexp = r'(?P<link>[^(\"\']http[s]{,1}://%s/wiki/spaces/[a-zA-Z0-9]+/pages/(?P<content_id>[0-9]+)[/\w]*)' % domain.replace('.', '\.')

    links = dict()
    for link, content_id in re.findall(regexp, text):
        link = link.strip().strip('\n')
        if link not in links:
            content = requests.get(
                'https://netping.atlassian.net/wiki/rest/api/content/{}'.format(content_id),
                auth=(login, token)).json()
            links[link] = content['title']

    for link, title in links:
        if task:
            text = text.replace(link, f'[{title}]({link})')
        else:
            text = text.replace('>' + link + '<', '>' + title + '<')

    return text


try:
    @post('/webhook')
    def calback():
        domain = config['teamwork']['domain']
        token = config['teamwork']['token']
        content_type = {'Content-Type': 'application/json'}
        event = request.json

        log.debug('Входящий хук - {}'.format(event))
        
        #print('Входящий хук - {}'.format(event))
        
        #print(event)

        if 'task' in event:
            text = event['task']['description']
        elif 'comment' in event:
            text = event['comment']['body']

        text = ' ' + text # фикс регулярки
        
        #print(text)

        #regexp = r'[^(\"\']http[s]{,1}://%s/[#/]{,2}tasks/[0-9]{,15}' % domain.replace('.', '\.')
        
        regexp = r'[^(\"\']http[s]{,1}://%s/[#/]{,3}tasks/[0-9]{,15}[\?c=[0-9]{,15}]{,1}' % domain.replace('.', '\.')
        
        #print(regexp)
        
        links = re.findall(regexp, text)

        log.debug('Нашли в нём все ссылки - {}'.format(links))
        
        #print(links)
        
        text_array_new = []

        if links != []:
            for link in links:
                try:
                    link = link.strip()
                    #print(link)
                    link = link.replace('<', '').replace('>', '')
                    #print(link)
                    taskid = re.findall(r'tasks/[0-9]{,15}', link)[0]
                    #print(taskid)
                    taskid = re.findall(r'[0-9]{1,15}', taskid)[0]
                    #print(taskid)
                    taskinfo = requests.get('https://{}/tasks/{}.json'.format(domain, taskid),
                                            auth=(token, '')).json()

                    log.debug('Получили информацию о задаче c id {} - {}'.format(taskid, taskinfo))
                    
                    #print(taskinfo)

                    title = taskinfo['todo-item']['content']
                    
                    #print(title)
                    
                    title = title.rstrip()
                    
                    #print(title)
                    
                    if 'task' in event:
                        title = f'[{title}]({link})'
                        
                        ##print(title)
                        
                        pos = text.find(link)
                        
                        pos_end = pos + len(link)
                        
                        text_with_first_link = text[0:pos_end]
                        
                        #print(text_with_first_link)
                        
                        other_part_of_text = pos_end
                        
                        text_end = len(text)
                        
                        text_after_link = text[other_part_of_text:text_end]
                        
                        #print(text_after_link)
                        
                        text_with_first_link = text_with_first_link.replace(link, title)
                        
                        #print(text_with_first_link)
                        
                        text_array_new.append(text_with_first_link)
                        
                        #print(text_array_new)
                        
                        text = text_after_link
                        
                        #print(text)
                        
                        #text = text.replace(link, title, 1)
                        
                        ##print(text)

                        # ~ title = ' ' + event['task']['name']
                        # ~ links = re.findall(regexp, title)
                        # ~ for link in links:
                            # ~ taskid = re.findall(r'tasks/[0-9]{,15}', link)[0]
                            # ~ taskid = re.findall(r'[0-9]{1,15}', taskid)[0]
                            # ~ taskinfo = requests.get('https://{}/tasks/{}.json'.format(domain, taskid),
                                                    # ~ auth=(token, '')).json()
                            # ~ t = taskinfo['todo-item']['content']
                            # ~ t = f'[{t}]({link})'
                            # ~ title = title.replace(link, t)

                    elif 'comment' in event:
                        temp = text.replace('>' + link + '<', '>' + title + '<')
                        if text == temp:
                        errors.error(
                            ('Ошибка при подстановке ссылки {}\nИсходный текст: {}\nОбработанный: {}').format(link, text, temp))
                        text = temp
                        
                        #print(text)
                except Exception as e:
                    errors.exception(
                        ('Ошибка при подстановке ссылки {} - {}').format(link, e))
                    errors.exception(traceback.format_exc())
                    
            log.info('Заменено %i ссылок' % len(links))
            
            #print(len(links))
            
            text_task = ''.join(text_array_new) + text
            
            #print(text_task)

            if 'task' in event:
                try:
                    title = replace_ids(task['task']['name'], task['task']['id'],
                                        task['task']['parentId'], config)
                except Exception as e:
                    title = event['task']['name']
                    errors.exception(
                        ('Ошибка при подстановке номеров '
                         'текущей и родительской задач - {}').format(e))
                    errors.exception(traceback.format_exc())

                try:
                    text_task = replace_confluence_links(text_task, config, True)
                except Exception as e:
                    errors.exception(
                        ('Ошибка при подстановке названий статей '
                         'из Confluence - {}').format(e))
                    errors.exception(traceback.format_exc())

                requests.put('https://{}/tasks/{}.json'.format(domain, event['task']['id']),
                             json={
                                 'todo-item': {
                                     'description': text_task,
                                     'content': title,
                                 }},
                             headers=content_type,
                             auth=(token, ''))

            elif 'comment' in event:
                try:
                    text = replace_confluence_links(text, config, False)
                except Exception as e:
                    errors.exception(
                        ('Ошибка при подстановке названий статей '
                         'из Confluence - {}').format(e))
                    errors.exception(traceback.format_exc())

                requests.put('https://{}/comments/{}.json'.format(domain, event['comment']['id']),
                             json={'comment': {
                                 'body': text,
                                 'notify': 'true',
                                 'content-type': event['comment']['contentType']
                                 }},
                             headers=content_type,
                             auth=(token, ''))

    if __name__ == '__main__':
        print('Script started. Version ' + VERSION)
        log.info('Поднимаем сервер')

        host = config['route']['host']
        port = int(config['route']['port'])
        run(host=host, port=port)

except Exception as e:
    print('При выполнении кода произошла ошибка - %s' % str(e))
    traceback.print_exc()
    errors.exception('При выполнении кода произошла ошибка - %s' % str(e))
    errors.exception(traceback.format_exc())
finally:
    print('Script ended.')
