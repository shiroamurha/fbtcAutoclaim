import json



allowed_keys = ["domain", "name", "path", "value", "id"]
treated_cookie_dicts = []


cookies_dicts = json.load(open('cookies.json', 'r'))

for list_item in range(0, len(cookies_dicts)):

    new_dict = dict()
    for dict_item in cookies_dicts[list_item]:
        
        if dict_item in allowed_keys:

            new_dict[dict_item] = cookies_dicts[list_item][dict_item]
        
    treated_cookie_dicts.append(new_dict)
    new_dict = None

##  finally  ##
json.dump(treated_cookie_dicts, open('cookies.json', 'w'), indent=4)


#     {
#         "domain": ".freebitco.in",
#         "name": "_ga",
#         "path": "/",
#         "value": "GA1.2.1787846977.1634149775",
#         "id": 1
#     },