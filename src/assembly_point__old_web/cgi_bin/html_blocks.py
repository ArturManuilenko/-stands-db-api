from typing import Optional, Dict, Any


class Block:
    def __init__(self, tag, param=''):
        self.tag = tag
        self.param = ' ' + param
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __str__(self):
        return '<{}{}>\n'.format(self.tag, self.param) +\
            '\n'.join(['\t' + str(item) for item in self.items]) +\
            '\n</{}>'.format(self.tag)


class Table:
    def __init__(self, caption=None, css_class='basetable'):
        self.caption = caption
        self.rows = []
        self.caption = caption
        self.header = None
        self.css_class = css_class

    def __str__(self):
        res = ['<table class="{}">'.format(self.css_class)]
        if self.caption:
            res.append(' <caption>{}</caption>'.format(self.caption))

        if self.header:
            res.append(' <tr>')
            for innerHtml, attributes in self.header:
                param_str = ' ' + attributes if attributes else ''
                res.append('  <th{}>{}</th>'.format(param_str, innerHtml))
            res.append(' </tr>')

        for row in self.rows:
            res.append(' <tr>')
            for innerHtml, attributes in row[0]:
                param_str = ' ' + attributes if attributes else ''
                res.append('  <td{}>{}</td>'.format(param_str, innerHtml))
            res.append(' </tr>')

        res.append('</table>')
        return ''.join(res)

    def add_row(self, *args, attributes=None):
        row = []
        for cell in args:
            if type(cell) is str:
                row.append((cell, None))
            else:
                row.append((cell[0], cell[1]))
        self.rows.append((row, attributes))

    def add_cell(self, innerHtml, attributes=None):
        self.rows[-1].append((innerHtml, attributes))

    def set_header(self, *args):
        row = []
        for cell in args:
            if type(cell) is str:
                row.append((cell, None))
            else:
                row.append( (cell[0], cell[1]) )
        self.header = row

    def print(self):
        print(str(self))


class ItemNavigation:
    def __init__(self, page, id, caption=''):
        self.page = page
        self.id = id
        self.caption = caption

    def __str__(self):
        return '''    <div class="item-navigation">
        <div class="navigation-left">
            <a href="{page}?nav=first" title="Перейти к первой записи">
                <div class="navigation-btn"><img src="/icons/record_begin.png" height=32></div>
            </a>
            <a href="{page}?id={id}&nav=prev" title="Перейти к предыдущей записи">
                <div class="navigation-btn"><img src="/icons/record_prev.png" height=32><span style="line-height:32px">предыдущий</span></div>
            </a>
        </div>
        <div class = navigation-center>{caption}</div>
        <div class="navigation-right">
            <a href="{page}?id={id}&nav=next" title="Перейти к следующей записи">
                <div class="navigation-btn">следующий<img src="/icons/record_next.png" height=32></div>
            </a>
            <a href="{page}?nav=last" title="Перейти к последней записи">
                <div class="navigation-btn"><img src="/icons/record_end.png" height=32></div>
            </a>
        </div>
    </div>
        '''.format(page=self.page, id=self.id, caption=self.caption)


class PageNavigation:
    def __init__(self, link, page, count):
        self.link = link
        self.page = page
        self.count = count

    def __str__(self):
        first = '<a href="{}" title="Первая страница"><img src="/icons/record_begin.png"></a>'.format(self.link)
        prev = '<a href="{}&page={}" title="Предыдущая страница"><img src="/icons/record_prev.png"></a>'.format(
            self.link, self.page - 1) if self.page != 1 else ''
        next = '<a href="{}&page={}" title="Следующая страница"><img src="/icons/record_next.png"></a>'.format(
            self.link, self.page + 1) if self.page != self.count else ''
        last = '<a href="{}&page={}" title="Последняя страница"><img src="/icons/record_end.png"></a>'.format(
            self.link, self.count)

        nums = []
        if self.page <= 6:
            for i in range(1, self.page):
                nums.append('<a href="{}&page={}">{}</a>'.format(self.link, i, i))
        else:
            for i in range(1, 4):
                nums.append('<a href="{}&page={}">{}</a>'.format(self.link, i, i))
            nums.append('..')
            for i in range(self.page - 2, self.page):
                nums.append('<a href="{}&page={}">{}</a>'.format(self.link, i, i))

        nums.append('<div>{}</div>'.format(self.page))

        if self.page >= self.count - 5:
            for i in range(self.page + 1, self.count + 1):
                nums.append('<a href="{}&page={}">{}</a>'.format(self.link, i, i))
        else:
            for i in range(self.page + 1, self.page + 3):
                nums.append('<a href="{}&page={}">{}</a>'.format(self.link, i, i))
            nums.append('..')
            for i in range(self.count - 2, self.count + 1):
                nums.append('<a href="{}&page={}">{}</a>'.format(self.link, i, i))


        return '''
<div class="page">
    <div class="page-left">{first}{prev}</div>
    <div class="page-middle">Страницы: {nums}</div>
    <div class="page-right">{next}{last}</div>
</div>
        '''.format(first = first, prev = prev, next=next, last=last, nums = ' '.join(nums))


class EditForm(Block):
    class Row:
        def __init__(self, caption, row_id, command, parent, new=False):
            self.caption = caption
            self.row_id = row_id
            self.command = command
            self.value = []
            self.parent = parent
            self.new = new

        def set_value(self, value):
            self.value = [value]

        def add_text(self, text):
            self.value.append('''<span>{}</span>'''.format(text))
            return self

        def add_button(self, text, command, script = None):
            if script:
                self.value.append('''<button onclick="{}">{}</button> '''.format(script, text))
            else:
                self.value.append('''<button onclick="edit_change(this); edit_action(this, {});">{}</button> '''.format(command, text))
            return self

        def add_text_edit(self, name, value):
            actions = '' if self.parent.group_apply else ''' value="{value}" oninput="edit_change(this);" onkeypress="edit_change(this);" onchange="edit_change(this);"'''
            self.value.append('''<input type="text" name="{name}" value="{value}"{actions}>'''.format(name=name, value=value, actions=actions))
            return self

        def add_check_box(self, name, text, value: str = '', checked: bool = False):
            checked = ' checked' if checked else ''
            actions = '' if self.parent.group_apply else ''' value="{value}" oninput="edit_change(this);" onkeypress="edit_change(this);" onchange="edit_change(this);"'''
            self.value.append('''<label><input type="checkbox" name="{name}" value="{value}"{checked} {actions}>{text}</label>'''.format(
                name=name, value=value, checked=checked, actions=actions, text=text))
            return self

        def add_combo_box(self, name, values, selected=None):
            opts = ['<option value="{}"{}>{}</option>'.format(value_id, ' selected' if value_id == selected else '', descr) for value_id, descr in values]
            actions = '' if self.parent.group_apply else ''' value="{value}" oninput="edit_change(this);" onkeypress="edit_change(this);" onchange="edit_change(this);"'''
            self.value.append('''<select name="{name}" {actions}>{value}</select>'''.format(
                name=name, value=''.join(opts), actions=actions))
            return self

        def __str__(self):
            str_id = ' id="{}"'.format(self.row_id) if self.row_id else ''
            new = ''
            if self.new:
                str_id += ' style="display:none;"'
                new = '<div class="edit-show"><button onclick="edit_show(this);"><img src="/icons/add_plus.png" height="24"></button></div>'
            if self.command:
                self.value.append('''
    <button class="edit-confirm" onclick="edit_action(this, {cmd});"><img src="/icons/apply.png" height="24"></button>
    <button class="edit-confirm" onclick="edit_action(this);"><img src="/icons/cancel.png" height="24"></button>
    <div class="edit-inprogress"><img src="/icons/inprogress.gif" height="32"></div>
'''.format(cmd=self.command))
            text = '''
<div class="edit-row" >
	<div class="edit-info"> {caption} </div>
	<div class="edit-cell"><div class="edit-edit"{str_id}>
        {value}
    </div>{new}</div>
</div>
'''.format(caption=self.caption, value='\n'.join(self.value), str_id=str_id, new=new)
            return text

    def __init__(self, group_apply: bool = False, command: Optional[str] = None) -> None:
        super().__init__('div', 'class="edit-form"')
        self.group_apply = group_apply
        self.command = command

    def add_row(self, caption, row_id: Optional = None, command: Optional[str] = None):
        row = self.Row(caption, row_id, command, self)
        self.add(row)
        return row

    def add_new_row(self, caption, row_id: Optional = None, command: Optional = None):
        row = self.Row(caption, row_id, command, self, True)
        self.add(row)
        return row

    def add_info(self, caption: str, value: str) -> None:
        row = self.add_row(caption, None, None)
        row.set_value(str(value))

    def add_text_edit(self, caption: str, value: str, text_id: str, command: str):
        self.add('''
    <div class="edit-row" >
	    <div class="edit-info"> {hdr} </div>
	    <div class="edit-cell"><div class="edit-edit" id="{id}">
		    <input type="text" name="{text_id}" value="{val}" oninput="edit_change(this);" onkeypress="edit_change(this);" onchange="edit_change(this);">
		    <button class="edit-confirm" onclick="edit_action(this, {cmd});"><img src="/icons/apply.png" height="24"></button>
		    <button class="edit-confirm" onclick="edit_action(this);"><img src="/icons/cancel.png" height="24"></button>
		    <div class="edit-inprogress"><img src="/icons/inprogress.gif" height="32"></div>
	    </div></div>
    </div>
'''.format(hdr=caption, val=str(value), text_id=text_id, cmd=command))

    def add_group_buttons(self, cmd: str, caption: Optional[str] = '', btn_apply: Optional[str] = '') -> None:
        if self.group_apply:
            val = '''
    <label></label>
    <button onclick="edit_change(this); edit_action(this, edit_add_value({cmd},document));"><img src="/icons/apply.png" height="24">{btn_apply}</button>
    <button onclick="edit_change(this); edit_action(this);"><img src="/icons/cancel.png" height="24"></button>
    <div class="edit-inprogress"><img src="/icons/inprogress.gif" height="32"></div>'''.format(btn_apply=btn_apply, cmd=cmd)

            self.add_row(caption).set_value(val)


class PeriodPicker(Block):

    def __init__(self, dt_from, dt_to, params: Dict[str, Any]) -> None:
        self.dt = (dt_from, dt_to)
        self.params = params

    def __str__(self):
        params = '\n    '.join(['<input type="hidden" name="{}" value="{}">'.format(key, self.params[key])
                            for key in self.params.keys()])
        return '''
<form>
    {}
    С <input name="from" id="datetimepicker_from" type="text" > до
    <input name="to" id="datetimepicker_to" type="text" >
    <input type="submit" value="Получить">
</form>
<script>setStendTime("{}","{}")</script>
        '''.format(params, *self.dt)
