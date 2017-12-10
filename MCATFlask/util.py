def listify(dictionary):
    ret_list = []

    for key in dictionary:
        for i in dictionary[key]:
            ret_list.append((key, i))

    return ret_list
