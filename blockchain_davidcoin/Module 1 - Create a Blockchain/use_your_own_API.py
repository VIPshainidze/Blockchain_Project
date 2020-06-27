# Import libraries
from requests import get
from json import dumps

# Your own local host's url
URL = "http://127.0.0.1:5000/"

# Names of active pages
mine_block = "mine_block"
get_chain = "get_chain"
is_valid = "is_valid"


# Define function for to check if API works and use the API.
def check_request_and_get_result(url, target_page_name, checked=False, needed_json_dumps=True):
    target_url = url + target_page_name
    request = get(target_url)
    response = request.status_code
    if checked:
        return dumps(request.json(), sort_keys=True, indent=4) if needed_json_dumps else request.json()
    else:
        return "Congratulation, API works!" if response == 200 else "Something went wrong."


print(check_request_and_get_result(URL, get_chain, True))
