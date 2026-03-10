"""
WSGI config for she_report project.
"""
from django.core.wsgi import get_wsgi_application
import os

# PyMySQL patch — must be before Django loads
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'she_report.settings')


application = get_wsgi_application()
