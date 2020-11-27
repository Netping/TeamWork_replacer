import unittest

from main import replace_ids, replace_links
from main import get_confluence_regexp, get_teamwork_regexp


class TestTeamworkReplacer(unittest.TestCase):
    def test_teamwork_replace_in_task_description(self):
        text = '''
    Согласно требованиям к ПО: https://netping.teamwork.com/#/tasks/27726545
'''
        sample = '''
    Согласно требованиям к ПО: [ОБЩИЕ ТРЕБОВАНИЯ К СЕРВИСУ Netping Email forwader](https://netping.teamwork.com/#/tasks/27726545)
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda article_id: 'ОБЩИЕ ТРЕБОВАНИЯ К СЕРВИСУ Netping Email forwader', True)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/tasks/27810426</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_stuff(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/tasks/27810426 stuff</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a> stuff
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_lost_slash(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#tasks/27810426</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_cid(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/tasks/27810426?c=1234567</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_project(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/projects/1234/tasks/27810426</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_project_lost_stuff(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#projects/1234/tasks/27810426</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_project_full(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/projects/1234/tasks/27810426?c=1234567</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_in_comment_project_full_lost_slash(self):
        text = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#projects/1234/tasks/27810426?c=1234567</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">Заголовок задачи 27810426</a>
 <br>
</div>
'''
        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda task_id: f'Заголовок задачи {task_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_teamwork_replace_big_test(self):
        titles = {
            '27810426': '[IPRJ:24474707] Развернуть версию скрипта 3.1 в production',
            '26751310': '[HARDWARE] Что делать со старыми BOMами ?',
            '27841428': '!!!Согласовать!!! Внести изменения в инструкцию',
            '27858526': 'Добавить функционал для Jenkins',
            '27317457': 'Оплатить счет от ООО "МИКРОЛИТ"',
            '27844997': '[IPRJ:24474707] скрипт замены ссылок не работает',
        }
        text = '''
<div>
<a href="https://netping.teamwork.com/#/projects/536953/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/projects/536953/tasks/27810426">https://netping.teamwork.com/#/projects/536953/tasks/27810426</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/25424552" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/25424552">https://netping.teamwork.com/#/tasks/25424552</a>
<br />
<a href="https://netping.teamwork.com/#tasks/26751310" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/26751310">https://netping.teamwork.com/#tasks/26751310</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27841428" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27841428">https://netping.teamwork.com/#tasks/27841428</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27858526" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27858526">https://netping.teamwork.com/#tasks/27858526</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27317457?c=11956257" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27317457?c=11956257">https://netping.teamwork.com/#tasks/27317457?c=11956257</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/tasks/27810426</a>
<br />
<a href="https://netping.teamwork.com/#/people/306580/time" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/people/306580/time">https://netping.teamwork.com/#/people/306580/time</a>
<br />
<a href="https://netping.teamwork.com/#/projects/538299/tasks" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/projects/538299/tasks">https://netping.teamwork.com/#/projects/538299/tasks</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27844997" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27844997">https://netping.teamwork.com/#/tasks/27844997</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">https://netping.teamwork.com/#/tasks/27810426</a>
<br />
<a href="https://netping.teamwork.com/#/people/306580/time" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/people/306580/time">https://netping.teamwork.com/#/people/306580/time</a>
<br />
<a href="https://netping.teamwork.com/#/projects/538299/tasks" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/projects/538299/tasks">https://netping.teamwork.com/#/projects/538299/tasks</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27844997" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27844997">https://netping.teamwork.com/#/tasks/27844997</a>
<br />
<a href="https://netping.teamwork.com/#tasks/26751310" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/26751310">https://netping.teamwork.com/#tasks/26751310</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27841428" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27841428">https://netping.teamwork.com/#tasks/27841428</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27858526" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27858526">https://netping.teamwork.com/#tasks/27858526</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27317457?c=11956257" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27317457?c=11956257">https://netping.teamwork.com/#tasks/27317457?c=11956257</a>
</div>
'''
        sample = '''
<div>
<a href="https://netping.teamwork.com/#/projects/536953/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/projects/536953/tasks/27810426">[IPRJ:24474707] Развернуть версию скрипта 3.1 в production</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/25424552" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/25424552">https://netping.teamwork.com/#/tasks/25424552</a>
<br />
<a href="https://netping.teamwork.com/#tasks/26751310" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/26751310">[HARDWARE] Что делать со старыми BOMами ?</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27841428" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27841428">!!!Согласовать!!! Внести изменения в инструкцию</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27858526" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27858526">Добавить функционал для Jenkins</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27317457?c=11956257" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27317457?c=11956257">Оплатить счет от ООО "МИКРОЛИТ"</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">[IPRJ:24474707] Развернуть версию скрипта 3.1 в production</a>
<br />
<a href="https://netping.teamwork.com/#/people/306580/time" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/people/306580/time">https://netping.teamwork.com/#/people/306580/time</a>
<br />
<a href="https://netping.teamwork.com/#/projects/538299/tasks" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/projects/538299/tasks">https://netping.teamwork.com/#/projects/538299/tasks</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27844997" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27844997">[IPRJ:24474707] скрипт замены ссылок не работает</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27810426" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27810426">[IPRJ:24474707] Развернуть версию скрипта 3.1 в production</a>
<br />
<a href="https://netping.teamwork.com/#/people/306580/time" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/people/306580/time">https://netping.teamwork.com/#/people/306580/time</a>
<br />
<a href="https://netping.teamwork.com/#/projects/538299/tasks" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/projects/538299/tasks">https://netping.teamwork.com/#/projects/538299/tasks</a>
<br />
<a href="https://netping.teamwork.com/#/tasks/27844997" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#/tasks/27844997">[IPRJ:24474707] скрипт замены ссылок не работает</a>
<br />
<a href="https://netping.teamwork.com/#tasks/26751310" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/26751310">[HARDWARE] Что делать со старыми BOMами ?</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27841428" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27841428">!!!Согласовать!!! Внести изменения в инструкцию</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27858526" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27858526">Добавить функционал для Jenkins</a>
<br />
<a href="https://netping.teamwork.com/#tasks/27317457?c=11956257" target="_blank" rel="noopener" data-mce-href="https://netping.teamwork.com/#tasks/27317457?c=11956257">Оплатить счет от ООО "МИКРОЛИТ"</a>
</div>
'''
        def get_title(article_id):
            if article_id == '25424552':
                raise Exception('Ошибка получения информации о задаче c id {}'.format(article_id))
            return titles[article_id]

        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda article_id: get_title(str(article_id)), False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'
