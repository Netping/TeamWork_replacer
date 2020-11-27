import unittest

from main import replace_links, get_confluence_regexp, get_teamwork_regexp


class TestConfluenceReplacer(unittest.TestCase):
    def test_confluence_replace_in_task_description(self):
        text = '''
    Сервис: https://netping.atlassian.net/wiki/spaces/PROJ/pages/1720778753/PRJ7+NetPIng+Email+forwarder
'''
        sample = '''
    Сервис: [#PRJ7 NetPIng Email forwarder](https://netping.atlassian.net/wiki/spaces/PROJ/pages/1720778753/PRJ7+NetPIng+Email+forwarder)
'''
        text = replace_links(
            get_confluence_regexp('netping.atlassian.net'),
            text, lambda article_id: '#PRJ7 NetPIng Email forwarder', True)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_confluence_replace_in_comment(self):
        text = '''
<div>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork</a>
 <br>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">Заголовок статьи 1852866561</a>
 <br>
</div>
'''
        text = replace_links(
            get_confluence_regexp('netping.atlassian.net'),
            text, lambda article_id: f'Заголовок статьи {article_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_confluence_replace_in_comment_stuff(self):
        text = '''
<div>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork</a>
 <br>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork comment</a>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">Заголовок статьи 1852866561</a>
 <br>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1852866561/IPRJ+24474707+TeamWork">Заголовок статьи 1852866561</a> comment
</div>
'''
        text = replace_links(
            get_confluence_regexp('netping.atlassian.net'),
            text, lambda article_id: f'Заголовок статьи {article_id}', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_confluence_replace_in_another_comment_stuff(self):
        text = '''
<div>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38</a>
 <br>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38">https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38 comment</a>
</div>
'''
        sample = '''
<div>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38">#DKST 38 Функциональность встроенного ПО устройства</a>
 <br>
 <a href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38" target="_blank" rel="noopener" data-mce-href="https://netping.atlassian.net/wiki/spaces/PROJ/pages/1456242756/DKST+38">#DKST 38 Функциональность встроенного ПО устройства</a> comment
</div>
'''
        text = replace_links(
            get_confluence_regexp('netping.atlassian.net'),
            text, lambda article_id: f'#DKST 38 Функциональность встроенного ПО устройства', False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'

    def test_confluence_replace_big_test(self):
        titles = {
            '1456242756': '#DKST 38 Функциональность встроенного ПО устройства',
            '2405007428': '#DKST 57 Прототип landing page',
            '2006941751': '#DKST 57 Документация',
            '2079162593': '#DKST 64 Устройство 4/PWR в корпусе на DIN рейку',
            '1852866561': '[IPRJ:24474707] Скрипт подстановки для TeamWork',
        }
        text = '''
<div>
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
            get_confluence_regexp('netping.atlassian.net'),
            text, lambda article_id: titles[str(article_id)], False)
        assert text == sample, f'Ожидалось:\n{sample}\nПолучено:\n{text}'
