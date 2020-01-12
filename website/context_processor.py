from common.models import News, Category


def categories(request):
    # get root categories from database
    root_categories_query_set = News.objects.values('root_category').distinct()
    root_categories = [root_cat['root_category'] for root_cat in root_categories_query_set]

    footer_categories = []
    temp = []
    for i in range(len(root_categories)):
        if len(temp) == 4:
            footer_categories.append(temp)
            temp = []
        temp.append(root_categories[i])
    footer_categories.append(temp)

    choose_categories = []
    temp = []
    for i in range(len(root_categories)):
        if len(temp) == 6:
            choose_categories.append(temp)
            temp = []
        temp.append(root_categories[i])
    choose_categories.append(temp)
    return {'root_categories': root_categories, 'footer_categories': footer_categories, 'choose_categories': choose_categories}


def user_selected_categories(request):
    if request.user.is_authenticated:
        cats_query = Category.objects.filter(user=request.user)
        cats = set(cat.name for cat in cats_query)
        return {'selected_categories': cats}
    return {'selected_categories': []}