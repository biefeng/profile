import datetime

_admin_menus = [
    {
        "type": "subMenu",
        "title": "博客",
        "icon_class": "el-icon-location",
        "items": [
            {
                "type": "item",
                "title": '发表博客'
            },
            {
                "type": "item",
                "title": '管理博客'
            }, {
                "type": "item",
                "title": '博客分类'
            },
            {
                "type": "item",
                "title": '博客抓取'
            }
        ]
    },
    {
        "type": "subMenu",
        "title": "评论",
        "icon_class": "el-icon-location",
        "items": [
            {
                "type": "item",
                "title": '管理评论'
            }
        ]
    },
    {
        "type": "subMenu",
        "title": "插件",
        "icon_class": "el-icon-location",
        "items": [
            {
                "type": "item",
                "title": '插件管理'
            }, {
                "type": "item",
                "title": '插件管理'
            }
        ]
    }
]

_index_menus = [
    {
        "type": "subMenu",
        "title": "1",
        "icon_class": "el-icon-location",
        "items": [
            {
                "type": "group",
                "title": "1",
                "items": [
                    {
                        "type": "item",
                        "title": '1-1'
                    }, {
                        "type": "item",
                        "title": '1-2'
                    }
                ]
            },
            {
                "type": "group",
                "title": "2",
                "items": [
                    {
                        "type": "item",
                        "title": '1-1'
                    }, {
                        "type": "item",
                        "title": '1-2'
                    }
                ]
            }
        ]
    },
    {
        "type": "item",
        "title": '3-1'
    }
]

_INDEX_MENU_CONFIG = {
    "default_active": '0-0',
    "default_openeds": ['0-1'],
    "cls": 'el-menu-demo',
    "mode": 'vertical',
    "bg_color": '#545c64',
    "text_color": '#fff',
    "active_text_color": '#ffd04b'
}
_ADMIN_MENU_CONFIG = {
    "default_active": '1',
    "default_openeds": ['0-0-0'],
    "cls": 'el-menu-demo',
    "mode": 'vertical',
    "bg_color": '#545c64',
    "text_color": '#fff',
    "active_text_color": '#ffd04b'
}


def _resolve_menu(menu_json, config):
    if menu_json is None or isinstance(menu_json, tuple):
        return ''
    html = '<el-menu default-active="{default_active}" class="{cls}" mode="{mode}"  background-color="{bg_color}" text-color="{text_color}" active-text-color="{active_text_color}">'.format(**config)
    for index, item in enumerate(menu_json):
        html += _resolve_menu_item(item, str(index))
    return html + '</el-menu>'


def _resolve_menu_item(item, index):
    title = item['title']
    item_type = item['type']
    if item_type == 'group':
        gt = '<el-menu-item-group title="{title}">'.format(title=title)
        items = item['items']
        if items is not None and isinstance(items, list):
            for ti, si in enumerate(items):
                gt += _resolve_menu_item(si, index + "-" + str(ti))
        gt += '</el-menu-item-group>'
        return gt
    elif item_type == 'subMenu':
        gs = '<el-submenu index="{index}"> <template slot="title"><i class="{icon_class}"></i><span>{title}</span></template>'.format(index=index, icon_class="", title=title)
        items = item['items']
        if items is not None and isinstance(items, list):
            for ti, si in enumerate(items):
                gs += _resolve_menu_item(si, index + "-" + str(ti))
        gs += '</el-submenu>'
        return gs
    elif item_type == 'item':
        gi = '<el-menu-item index="{index}">{title}</el-menu-item>'.format(title=title, index=index)
        return gi


def get_menu(**kwargs):
    tmp = _INDEX_MENU_CONFIG.copy()
    tmp.update(kwargs)
    return _resolve_menu(_index_menus, tmp)


if __name__ == '__main__':
    print(get_menu(mode='horizontal'))
    sql = 'INSERT INTO articles (title, content, content_md, articleType_id, source_id) VALUES (%(title)s, %(content)s, %(content_md)s, %(source_id)s)'

    parameters = {'summary': None, 'update_time': datetime.datetime(2020, 7, 4, 7, 27, 25, 131312), 'content': '&lt;h3&gt;&lt;a id=&quot;Emoji_smiley_1&quot;&gt;&lt;/a&gt;Emoji表情 😃&lt;/h3&gt;\n&lt;blockquote&gt;\n&lt;p&gt;Blockquotes ⭐️&lt;/p&gt;\n&lt;/blockquote&gt;\n', 'content_md': '\n### Emoji表情 :smiley:\n\n> Blockquotes :star:\n', 'title': '27222', 'num_of_view': 0, 'articleType_id': 1, 'create_time': datetime.datetime(2020, 7, 4, 7, 27, 25, 131312), 'ref_url': None, 'source_id': 1}
    test = "%(sty)s".format_map({'sty':1})
    print(test)

    print('INSERT INTO articles (title, ref_url, content, content_md, summary, create_time, update_time, num_of_view, `articleType_id`, source_id) VALUES (%(title)s, %(ref_url)s, %(content)s, %(content_md)s, %(summary)s, %(create_time)s, %(update_time)s, %(num_of_view)s, %(articleType_id)s, %(source_id)s)' % {'summary': None, 'update_time': datetime.datetime(2020, 7, 4, 7, 27, 25, 131312), 'content': '&lt;h3&gt;&lt;a id=&quot;Emoji_smiley_1&quot;&gt;&lt;/a&gt;Emoji表情 😃&lt;/h3&gt;\n&lt;blockquote&gt;\n&lt;p&gt;Blockquotes ⭐️&lt;/p&gt;\n&lt;/blockquote&gt;\n', 'content_md': '\n### Emoji表情 :smiley:\n\n> Blockquotes :star:\n', 'title': '27222', 'num_of_view': 0, 'articleType_id': 1, 'create_time': datetime.datetime(2020, 7, 4, 7, 27, 25, 131312), 'ref_url': None, 'source_id': 1})
