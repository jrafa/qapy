from fabric.api import local


def run():
    local('python manage.py runserver')


def lint():
    local('pylint --load-plugins pylint_django app/')


def test():
    local('python manage.py test')