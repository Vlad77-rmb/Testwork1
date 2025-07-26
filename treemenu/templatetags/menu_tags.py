from django import template
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('treemenu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path_info

    # Получаем все пункты меню одним запросом
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    # Строим дерево меню
    menu_tree = []
    items_dict = {}

    for item in menu_items.order_by('order'):
        items_dict[item.id] = {
            'item': item,
            'children': [],
            'is_active': item.is_active(current_path),
            'is_parent_active': False
        }

    # Связываем родительские и дочерние элементы
    for item_id, item_data in items_dict.items():
        item = item_data['item']
        if item.parent_id:
            if item.parent_id in items_dict:
                items_dict[item.parent_id]['children'].append(item_data)
                # Помечаем родителя как активного, если активен ребенок
                if item_data['is_active']:
                    parent = items_dict[item.parent_id]
                    parent['is_parent_active'] = True
        else:
            menu_tree.append(item_data)

    return {
        'menu_tree': menu_tree,
        'menu_name': menu_name,
        'current_path': current_path,
    }