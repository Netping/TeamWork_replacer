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


def replace_ids(domain, token, task):
    """
    Replace in task title:
        - %id% with unique task number;
        - %idf% with unique parent task number, current if haven't parent.

    Args:
        - domain - teamwork address without http/https and slashs;
        - token - token for authentication on teamwork server;
        - task - task object, recieved on webhook, dict.

    return task title with raplaces str
    """
    tasks = dict()
    task_id = task['task']['id']
    if task['task']['parentId']:
        while True:
            taskinfo = requests.get(
                'https://{}/tasks/{}.json'.format(domain, parent_id),
                auth=(token, '')).json()
            if not taskinfo['todo-item']['parentTaskId']:
                parent_id = taskinfo['todo-item']['id']
                break
    else:
        parent_id = task_id
    return task['task']['name'].replace('\%idf\%', parent_id).replace(
        '\%id\%', task_id)

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
                    text = text.replace('>' + link + '<', '>' + title + '<')
                    
                    #print(text)
                    
            log.info('Заменено %i ссылок' % len(links))
            
            #print(len(links))
            
            text_task = ''.join(text_array_new) + text
            
            #print(text_task)

            if 'task' in event:
                try:
                    title = replace_ids(event)
                except Exception as e:
                    title = event['task']['name']
                    errors.exception(
                        ('Ошибка при подстановке номеров '
                         'текущей и родительской задач - {}').format(e))
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
                requests.put('https://{}/comments/{}.json'.format(domain, event['comment']['id']),
                             json={'comment': {'body': text, 'content-type': event['comment']['contentType']}},
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
