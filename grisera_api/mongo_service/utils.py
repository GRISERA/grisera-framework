def mongo_deep_iteration(func):
    """
    Decorator for performing a function on each primitive value in mongo output/input
    dict. Mongo document field values are either primitives, dicts or arrays.
    """

    def deep_iteration(dict_to_iterate):
        if type(dict_to_iterate) is not dict:
            return
        for field, value in dict_to_iterate.items():
            if type(value) is dict:
                deep_iteration(value)
            elif type(value) is list:
                for list_elem in value:
                    deep_iteration(list_elem)
            else:
                dict_to_iterate[field] = func(dict_to_iterate[field])

    return deep_iteration
