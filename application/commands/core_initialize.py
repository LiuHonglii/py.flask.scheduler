# -*- coding: utf-8 -*-
import json
from pathlib import Path
from sqlalchemy import text
from application.common import CustomError
from application.models import db

BASE_DIR = Path(__file__).parent


class CoreInitialize():
    """
    使用方法：继承此类，重写 run方法，在 run 中调用 save 进行数据初始化
    """

    def __init__(self, create_by=None, modifier=None):
        """
        create_by: 创建人id
        modifier: 修改者
        """
        self.create_by = create_by or 1
        self.modifier = modifier or '超级管理员'

    def init_save(self, *, ModelClass, ModelClassNested=None, unique_columns=None, fk=None, is_truncate=False, is_create_by=True):
        """
        初始化数据
        :param ModelClass: 主模型
        :param ModelClassNested: 嵌套模型
        :param unique_columns: 唯一列
        :param fk: 外键字段
        :param is_truncate: 是否截断表
        :param is_create_by: 是否添加创建者ID
        :return:
        """
        print(f"正在初始化===>[{ModelClass.__doc__}]")
        if is_truncate:
            try:
                db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
                db.session.execute("TRUNCATE TABLE {};".format(ModelClass.__tablename__))
                if ModelClassNested:
                    db.session.execute("TRUNCATE TABLE {};".format(ModelClassNested.__tablename__))
                db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
                db.session.commit()
            except Exception as e:
                raise e

        file_path = BASE_DIR / f'json_file/init_{ModelClass.__tablename__}.json'

        if not file_path.exists():
            raise CustomError(f'路径【{file_path}】不存在')
        # 读取文件
        f = file_path.read_text(encoding='utf-8')
        for ele in json.loads(f):
            filter_data = {}
            nested_list = []
            nested_key = None
            if unique_columns and not fk:
                for column in unique_columns:
                    if column in ele:
                        filter_data[column] = ele[column]
            else:
                for key, value in ele.items():
                    if isinstance(value, list):
                        nested_list.extend(value)
                        nested_key = key
                        continue
                    elif value == None or value == '':
                        continue
                    else:
                        filter_data[key] = value

            instance = ModelClass.query.filter_by(**filter_data).first()
            with db.auto_commit():
                if instance:
                    for k, v in ele.items():
                        if hasattr(instance, k):
                            setattr(instance, k, v)
                else:
                    ele.pop(nested_key, None)
                    if is_create_by:
                        instance = ModelClass(modifier=self.modifier,
                                              create_by=self.create_by, update_by=self.create_by, **ele)
                    else:
                        instance = ModelClass(**ele)
                    db.session.add(instance)
                    db.session.flush()

                    if hasattr(instance, 'password_hash'):
                        instance.password = '12345678'

                fk_dict = {}
                if fk:
                    fk_dict |= {fk: instance.id}

                # 嵌套数据处理
                for nested in nested_list:
                    filter_nested = {}
                    for k, v in nested.items():
                        if v == None or v == '':
                            continue
                        filter_nested[k] = v

                    nested_instance = ModelClassNested.query.filter_by(**fk_dict, **filter_nested).first()
                    if nested_instance:
                        for k, v in ele.items():
                            if hasattr(nested_instance, k):
                                setattr(nested_instance, k, v)
                    else:
                        if is_create_by:
                            nested_instance = ModelClassNested(modifier=self.modifier,
                                                               create_by=self.create_by, update_by=self.create_by,
                                                               **fk_dict, **nested)
                        else:
                            nested_instance = ModelClassNested(**fk_dict, **nested)
                        db.session.add(nested_instance)

        print(f"初始化完成===>[{ModelClass.__doc__}]")

    def destroy(self, table_name):
        """删除表"""
        try:
            db.session.execute(text(f"DROP TABLE IF EXISTS public.{table_name};"))
            db.session.commit()
        except Exception as e:
            raise CustomError(f'删除数据表失败 {e}')

        print(f"删除表完成===>[{table_name}]")

    def run(self):
        raise NotImplementedError('.run() must be overridden')
