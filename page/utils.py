# -*- coding:utf-8 -*-
import yaml


class Utils:
    @classmethod
    def from_file(cls, path):
        with open(path, encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
            params = yaml_data["params"]
            keys = set()
            values = []
            if isinstance(params, list):
                for row in params:
                    if isinstance(row, dict):
                        for key in row:  # 当前yaml中row只有一个键值对，这里对row进行循环可以兼容row为存在多个键值对的字典
                            keys.add(key)
                            # row.values()返回的类型是dict_values，所以得强行改成list
                            values.append(list(row.values())[0])  # 这里有问题，取了list的第一个值就把兼容多键值对的效果搞没了
            var_names = ','.join(keys)
            return {'key': var_names, 'value': values}
