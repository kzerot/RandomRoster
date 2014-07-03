
def in_div(value, cls=None, id=None):
    result = '<div'
    if id:
        result += ' id="%s"' % id
    if cls:
        result += ' class="%s"' % cls
    result += '>'
    result += value
    result += '</div>'
    return result


def in_p(value, cls=None, id=None):
    result = '<p'
    if id:
        result += ' id="%s"' % id
    if cls:
        result += ' class="%s"' % cls
    result += '>'
    result += value
    result += '</p>'
    return result


def in_a(href, value, cls=None, id=None):
    result = '<a href="%s"' % href
    if id:
        result += ' id="%s"' % id
    if cls:
        result += ' class="%s"' % cls
    result += '>'
    result += value
    result += '</a>'
    return result


def select(items, name, id=None):
    if not id:
        id = name
    result = '<select name="%s" id="%s">' % (name, id)
    for item in items:
        result += '<option value="%s">%s</option>' % (item, items[item])
    result += '</select>'
    return result
