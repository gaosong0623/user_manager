"""
WSGI config for user_manager project.（user_manager项目的WSGI配置。）
It exposes the WSGI callable as a module-level variable named ``application``.
（它将WSGI可调用公开为一个名为' ' application ' ' '的模块级变量。）

For more information on this file, see（有关此文件的更多信息，请参见）
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_manager.settings")

application = get_wsgi_application()
