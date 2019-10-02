# def is_user_name(ele):


def is_signature(ele):
    if ele.name != "div" or not ele.has_attr('class'):
        return False
    return ('signature_display' in ele['class']) or ('a_edit_signature' in ele['class'])
    # if ele.name == "div" and ele.has_attr('class'):
    #     print(ele['class'])
    #     return True
    # else:
    #     return False


def is_item(ele):
    return ele.name == 'li' and ele.has_attr('class') and ele['class'] == ['aob']
