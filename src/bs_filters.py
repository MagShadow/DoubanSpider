# def is_user_name(ele):


def is_signature(ele):
    return ele.name == "div" and ele.has_attr('class') and ('signature_display' in ele['class'])
    # if ele.name == "div" and ele.has_attr('class'):
    #     print(ele['class'])
    #     return True
    # else:
    #     return False


def is_item(ele):
    return ele.name == 'li' and ele.has_attr('class') and ele['class'] == ['aob']
