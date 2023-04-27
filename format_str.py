from collections import Iterable

def FormatStr(obj, obj_name, space_num):
    l_character = "{"
    r_character = "}"
    need_key = False
    space = " " * space_num
    equal_character = '=' if space_num == 0 else ':'
    #print obj, ' is ', type(obj), isinstance(obj, Iterable)
    if not isinstance(obj, Iterable) or isinstance(obj, str):
        obj_str = "'{}'".format(obj) if isinstance(obj, str) else obj
        if obj_name:
            return "{}{} {} {}".format(space, obj_name, equal_character, obj_str)
        else:
            return "{}{}".format(space, obj_str)
    if isinstance(obj, list):
        l_character = "["
        r_character = "]"
    elif isinstance(obj, (tuple, set)):
        l_character = "("
        r_character = ")"
    elif isinstance(obj, dict):
        need_key = True
    res_inner = ""
    if obj_name:
        res_inner += "{}{} {} {}\n".format(
            space, obj_name, equal_character, l_character
        )
    else:
        res_inner += "{}{}\n".format(space, l_character)
    if need_key:
        for _key, _val in obj.iteritems():
            if isinstance(_key, int):
                _item_key = "{}".format(_key)
            else:
                _item_key = "'{}'".format(_key)
            res_inner += FormatStr(_val, _item_key, space_num + 4)
            res_inner += ",\n"
    else:
        for _val in obj:
            res_inner += FormatStr(_val, "", space_num + 4)
            res_inner += ",\n"
    res_inner += "{}{}".format(space, r_character)
    return res_inner


def WriteProto(proto_name, data, root_key="DataList", out_put=False):
    s = FormatStr(data, root_key, 0)
    f = open(proto_name, "wt")
    f.write("# -*- coding: utf-8 -*-\n\n")
    f.write(s)
    f.close()


def WriteJson(proto_name, data):
    import json
    s = json.dumps(data)
    f = open(proto_name, "wt")
    f.write(s)
    f.close()


def unicode_convert(input):
    if isinstance(input, dict):
        return {
            unicode_convert(key): unicode_convert(value)
            for key, value in input.iteritems()
        }
    elif isinstance(input, list):
        return [unicode_convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
    
def GetRes(name, mode='rt'):
    data_str = ''
    try:
        f = open(name, mode)
        data_str = f.read()
        f.close()
    except:
        pass
    return data_str

def ReadPyFromRes(name):
    data_str = GetRes(name)
    data = eval(data_str)
    return unicode_convert(data)

def ReadJsonFromRes(name):
    import json
    data_str = GetRes(name)
    if not data_str:
        return None
    data = json.loads(data_str)
    return unicode_convert(data)


def ConvertDictToGameData(infos):
    data_list = []
    for k, v in infos.iteritems():
        v['id'] = k
        data_list.append(v)
    return data_list


def ConvertGameDataToDict(infos):
    if not isinstance(infos, dict):
        return infos
    new_dict = {}
    for it_data in infos.itervalues():
        it_data.pop('id', None)
        new_data = ConvertGameDataToDict(it_data)
        new_dict[it_data['id']] = new_data
    return new_dict


def EmptyDict(infos):
    if not isinstance(infos, dict):
        return
    del_list = []
    for k in infos.iterkeys():
        EmptyDict(infos[k])
        if isinstance(infos[k], dict) and not infos[k]:
            del_list.append(k)
    for k in del_list:
        infos.pop(k, None)
    if len(infos) == 1 and 'id' in infos:
        infos.clear()