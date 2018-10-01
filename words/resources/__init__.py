from __future__ import print_function, unicode_literals, absolute_import
import os
import glob
import dandan

resources = []


def get_item(filename):
    data = dandan.value.get_json(filename)
    if not data:
        return None
    if not isinstance(data, list):
        return None
    name = os.path.splitext(os.path.basename(filename))[0]
    item = dandan.value.AttrDict()
    item.type = 'list'
    item.name = name
    item.list = data
    return item


def get_menu(dirname):
    menu = dandan.value.AttrDict()
    menu.type = 'menu'
    menu.name = os.path.basename(dirname)
    menu.list = []
    files = glob.glob(os.path.join(dirname, "*"))
    for filename in files:
        if os.path.isfile(filename) and filename.endswith(".json"):
            item = get_item(filename)
            if not item:
                continue
            menu.list.append(item)
            continue
        if os.path.isdir(filename):
            submenu = get_menu(filename)
            if not submenu:
                continue
            menu.list.append(submenu)
    if not menu.list:
        return []
    menu.list = sorted(menu.list, key=lambda e: e.name)
    return menu


def get_resources():
    global resources
    if resources:
        return resources

    dirname = os.path.dirname(os.path.abspath(__file__))
    resources = get_menu(dirname).list
    return resources
