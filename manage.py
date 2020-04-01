#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_manager.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        #以上导入可能由于其他原因而失败。确保
        # 问题是Django为了避免掩蔽其他的东西而丢失了
        # Python 2上的异常。
        try:
            import django
        except ImportError:
            raise ImportError(
                #“不能导入Django。你确定安装了吗?”
                #“在您的PYTHONPATH环境变量中可用吗?”你是“
                #“忘记激活虚拟环境?”
            )
        raise
    execute_from_command_line(sys.argv)

