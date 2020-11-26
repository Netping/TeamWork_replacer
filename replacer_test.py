import unittest

from main import replace_ids, replace_links
from main import get_confluence_regexp, get_teamwork_regexp


class TestReplacer(unittest.TestCase):
    def test_replace_ids(self):
        text = 'Asd %idf% -> %id% feg'
        sample = 'Asd 2345 -> 1234 feg'
        text = replace_ids(text, 1234, lambda task_id: 2345)
        assert text == sample

    def test_replace_ids_wrong_sample(self):
        text = 'Asd %idf% -> %id% feg'
        sample = 'Asd 2345 -> 12343 feg'
        text = replace_ids(text, 1234, lambda task_id: 2345)
        assert text != sample

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

# if __name__ == "__main__":
#     unittest.main()
