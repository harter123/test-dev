import requests
import traceback


class InterfaceUtils:

    @classmethod
    def parse_parameter(cls, parameter):
        """
        form形式的参数转成字典，例如 [{'key': 'a', 'value': 'a', 'type': 'string'}, {'key': 'b', 'value': '1', 'type': 'int'}]
        会转成字典：{"a": "a", "b": 1}
        :param parameter:
        :return:
        """
        ret = {}
        if not parameter:
            return ret

        for p in parameter:
            try:
                p_type = p.get('type', None)
                if p_type is None:
                    continue
                key = p.get('key', None)
                if key is None:
                    continue
                value = p.get('value', None)
                if value is None:
                    continue
                if "string" == p_type:
                    ret[key] = str(value)
                elif "int" == p_type:
                    ret[key] = int(value)
                elif "float" == p_type:
                    ret[key] = float(value)
                elif "bool" == p_type:
                    ret[key] = bool(value)
                else:
                    continue
            except Exception:
                continue
        return ret

    @classmethod
    def send_request(cls, url, method, header, parameter, parameter_type):
        ret = ''
        if "form" == parameter_type:  # 第一步， 把form形式转成字典，如果是json，则不需要
            parameter = cls.parse_parameter(parameter)

        try:
            if "GET" == method:
                ret = cls.__get_request(url, header, parameter)
            elif "POST" == method:
                ret = cls.__post_request(url, header, parameter, parameter_type)
            elif "DELETE" == method:
                ret = cls.__delete_request(url, header, parameter, parameter_type)
            elif "PUT" == method:
                ret = cls.__put_request(url, header, parameter, parameter_type)
            return ret
        except Exception:
            return traceback.format_exc()

    @classmethod
    def __set_header(cls, header, parameter_type):
        if "json" == parameter_type:  # json形式
            header["content-type"] = "application/json"
        else:  # form形式
            header["content-type"] = "application/x-www-form-urlencoded"
        return header

    @classmethod
    def __get_request(cls, url, header, parameter):
        """
        get请求，数据都在url，超时30s
        :param url: 字符串
        :param header: 字典
        :param parameter: 字典
        :return:
        """
        ret = requests.get(url, params=parameter, headers=header, timeout=30)
        return ret.text

    @classmethod
    def __post_request(cls, url, header, parameter, parameter_type):
        """
        post 请求
        :param url:
        :param header: 字典
        :param parameter: 字典
        :param parameter_type:
        :return:
        """
        header = cls.__set_header(header, parameter_type)
        if "json" == parameter_type:
            ret = requests.post(url, json=parameter, headers=header, timeout=30)
        else:
            ret = requests.post(url, data=parameter, headers=header, timeout=30)
        return ret.text

    @classmethod
    def __delete_request(cls, url, header, parameter, parameter_type):
        """
        delete请求
        :param url:
        :param header:
        :param parameter:
        :param parameter_type:
        :return:
        """
        header = cls.__set_header(header, parameter_type)
        if "json" == parameter_type:
            ret = requests.delete(url, json=parameter, headers=header, timeout=30)
        else:
            ret = requests.delete(url, data=parameter, headers=header, timeout=30)
        return ret.text

    @classmethod
    def __put_request(cls, url, header, parameter, parameter_type):
        """
        put请求
        :param url:
        :param header:
        :param parameter:
        :param parameter_type:
        :return:
        """
        header = cls.__set_header(header, parameter_type)
        if "json" == parameter_type:
            ret = requests.put(url, json=parameter, headers=header, timeout=30)
        else:
            ret = requests.put(url, data=parameter, headers=header, timeout=30)
        return ret.text
