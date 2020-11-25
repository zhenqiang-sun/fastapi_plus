import os


class GenerateModel(object):
    """
    基于Demo代码生成新的模块，省去复制粘贴
    """

    lib_path: str  # fastapi_plus库路径
    app_path: str  # app应用路径
    model_name: str  # model名称，小写+下划线式，snake
    model_name_pascal: str  # model名称，大驼峰，pascal

    def __init__(self, app_path: str, model_name: str):
        # 接收、处理入参
        self.app_path = app_path
        self.model_name = model_name
        self.model_name_pascal = self._transform_name(model_name)
        self.lib_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 生成文件
        self._generate_file('controller')
        self._generate_file('dao')
        self._generate_file('model')
        self._generate_file('schema')
        self._generate_file('service')

    @staticmethod
    def _transform_name(src: str, first_upper: bool = True) -> str:
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
    def _read_file_content(file_path: str) -> str:
        """
        读取文件
        :param file_path:
        :return:
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def _save_file_content(file_path: str, file_content: str):
        """
        保存文件
        :param file_path:
        :param file_content:
        :return:
        """

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)

    def _generate_file(self, dir_name: str):
        """
        生成文件
        :param dir_name:
        :return:
        """

        src_file_path = self.lib_path + os.sep + dir_name + os.sep + 'demo.py'
        new_file_path = self.app_path + os.sep + dir_name + os.sep + self.model_name + '.py'

        file_content = self._read_file_content(src_file_path)

        file_content = file_content.replace('demo', self.model_name)
        file_content = file_content.replace('Demo', self.model_name_pascal)

        self._save_file_content(new_file_path, file_content)
