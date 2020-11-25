import os
import re
import subprocess

from fastapi_plus.utils.db import DbConfig


class SyncModel(object):
    """SyncModel，同步数据模型.

    将数据库中的表转换成model

    Attributes:
        model_header: model头部
        is_use_base_model: 是否使用基础model
        base_model_lines: 基础model行
        dao: 当前业务数据处理类
    """

    app_dir: str  # 应用目录名
    model_header = 'from fastapi_plus.model.base import *\n\n\n'
    is_use_base_model = False
    base_model_path = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'model' + os.sep + 'base.py'
    base_model_lines = []
    db_config: DbConfig = None

    def sqlacodegen(self, file_path):
        subprocess.call(['sqlacodegen', self.db_config.get_url(), '--outfile', file_path])

    def get_models_content(self, file_path):
        self.sqlacodegen(file_path)
        content = self._read_file_content(file_path)
        return content

    @staticmethod
    def _read_file_content(file_path: str) -> str:
        """
        读取文件
        :param file_path:
        :return:
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def _transform_name(src: str, first_upper: bool = True):
        """
        将下划线分隔的名字,转换为驼峰模式
        :param src:
        :param first_upper: 转换后的首字母是否指定大写(如
        :return:
        """
        arr = src.split('_')
        res = ''
        for i in arr:
            res = res + i[0].upper() + i[1:]

        if not first_upper:
            res = res[0].lower() + res[1:]
        return res

    @staticmethod
    def _get_table_name(content):
        table_name_list = re.findall(".*__tablename__ = '(.*)'.*", content)

        if table_name_list:
            return table_name_list[0]
        else:
            return None

    def sync(self, app_dir: str == 'app', db_config: DbConfig, is_use_base_model: bool = False,
             base_model_path: str = None,
             model_header: str = None):

        self.app_dir = app_dir
        self.db_config = db_config
        file_path = self.app_dir + os.sep + 'temporary' + os.sep + 'models.py'
        models_content = self.get_models_content(file_path)
        content_list = models_content.split('\n\nclass ')

        if base_model_path:
            self.base_model_path = base_model_path

        if model_header:
            self.model_header = model_header

        if is_use_base_model:
            self.is_use_base_model = is_use_base_model
            self._init_base_model()
        else:
            self.model_header = content_list[0]

        for content in content_list:
            self._save_model(content)

        os.remove(file_path)

    def _init_base_model(self):
        content = self._read_file_content(self.base_model_path)
        class_list = content.split('class Base(DeclarativeBase):')
        lines = class_list[1].split('\n')

        for line in lines:
            line = line.strip()

            if line:
                self.base_model_lines.append(line)

    def _use_base_model(self, model_content):
        model_lines = model_content.split('\n')
        del model_lines[0]
        lines = []

        for model_line in model_lines:
            for base_model_line in self.base_model_lines:
                if model_line.find(base_model_line) > -1:
                    model_line = None
                    break

            if model_line is not None:
                lines.append(model_line)

        return '\n'.join(lines)

    def _save_model(self, content):
        table_name = self._get_table_name(content)
        if not table_name:
            return

        if self.is_use_base_model:
            content = self._use_base_model(content)

        file_name = table_name[len(self.db_config.table_name_prefix):]
        class_name = self._transform_name(file_name)
        file_path = self.app_dir + os.sep + 'model' + os.sep + file_name + '.py'
        file_content = self.model_header + 'class ' + class_name + '(Base):\n' + content
        file_content = file_content.replace('Column(JSON,', 'Column(LONGTEXT,')

        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(file_content)
