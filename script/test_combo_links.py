import unittest

from main import replace_links, get_confluence_regexp, get_teamwork_regexp


class TestComboLinksReplacer(unittest.TestCase):
    def test_teamwork_confluence_replace(self):
        teamwork_titles = {
            '27810426': '[IPRJ:24474707] Развернуть версию скрипта 3.1 в production',
            '26751310': '[HARDWARE] Что делать со старыми BOMами ?',
            '27841428': '!!!Согласовать!!! Внести изменения в инструкцию',
            '27858526': 'Добавить функционал для Jenkins',
            '27317457': 'Оплатить счет от ООО "МИКРОЛИТ"',
            '27844997': '[IPRJ:24474707] скрипт замены ссылок не работает',
        }

        def get_teamwork_title(article_id):
            if article_id == '25424552':
                raise Exception('Ошибка получения информации о задаче c id {}'.format(article_id))
            return teamwork_titles[article_id]

        confluence_titles = {
            '1456242756': '#DKST 38 Функциональность встроенного ПО устройства',
            '2405007428': '#DKST 57 Прототип landing page',
            '2006941751': '#DKST 57 Документация',
            '2079162593': '#DKST 64 Устройство 4/PWR в корпусе на DIN рейку',
            '1852866561': '[IPRJ:24474707] Скрипт подстановки для TeamWork',
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
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page">https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57">https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN">https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page">https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57">https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN">https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN</a>
<br />
<div>
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
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38">#DKST 38 Функциональность встроенного ПО устройства</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page">#DKST 57 Прототип landing page</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57">#DKST 57 Документация</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN">#DKST 64 Устройство 4/PWR в корпусе на DIN рейку</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">[IPRJ:24474707] Скрипт подстановки для TeamWork</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">[IPRJ:24474707] Скрипт подстановки для TeamWork</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2405007428/DKST+57+landing+page">#DKST 57 Прототип landing page</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2006941751/DKST+57">#DKST 57 Документация</a>
<br />
<a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/2079162593/DKST+64+4+PWR+DIN">#DKST 64 Устройство 4/PWR в корпусе на DIN рейку</a>
<br />
<div>
'''

        text = replace_links(
            get_teamwork_regexp('netping.teamwork.com'),
            text, lambda article_id: get_teamwork_title(str(article_id)), False)

        text = replace_links(
            get_confluence_regexp('netping.atlassian.net'),
            text, lambda article_id: confluence_titles[str(article_id)], False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'