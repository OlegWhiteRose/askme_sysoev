<h2 align="center">ДЗ3</h2>
<h3>Базы данных:</h3>
<p>все бд архивированны, чтобы не превысить макс. размер файла в git</p>
<h6>Датасеты:</h6>
<p>Находятся в data/datasets, нужны для генерации реальных пользователей и вопросов</p>
<h6>Обычные бд:</h6>
<p>Находятся в корневом каталоге дзшки, это сохраненные sql бд real и fake пользователей</p>
<p>Используется PostgreSQL, с вот такой вот настройкой в Django: </p>
<p>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
</p>
<h3>Генератор данных:</h3>
<p>Назван так, как показано в ТЗ</p>
<h6>Генерация реальных пользователей:</h6>
<p>python3 manage.py fill_db (ratio) real</p>
<p>генератор скажет, если реальных пользователей недостаточно</p>
<p>
	<div style="color:red">Внимание!!!</div>
	<div>Для генерации реальных пользователей нужно распаковать датасеты</div>
</p>
<h6>Генерация фейковых пользователей:</h6>
<p>python3 manage.py fill_db (ratio) fake</p>
<h3>Источники:</h3>
<h6>Датасеты брал отсюда:</h6>
<p><a href="https://www.kaggle.com/datasets/sharmanshik/some-recent-questions-from-otvetmailru">База ответов mail.ru</a></p>
<p><a href="https://github.com/dkulagin/kartaslov/blob/master/dataset/orfo_and_typos/orfo_and_typos.L1_5%2BPHON.csv">Просто словарик каких-то слов</a></p>
