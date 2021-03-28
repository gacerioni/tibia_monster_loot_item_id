import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from html_table_parser import HTMLTableParser


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


def get_tibia_id_dict():
    url = 'https://tibia.fandom.com/wiki/Item_IDs'
    xhtml = url_get_contents(url).decode('utf-8')

    p = HTMLTableParser()
    p.feed(xhtml)
    # pprint(p.tables)
    # print(p.tables[0][1:])
    # print(type(p.tables[0][1:]))

    item_dict_final = {}
    for item in p.tables[0][1:]:
        item_dict_final[item[0]] = item[1]

    return (item_dict_final)


def get_tibiawiki_opensearch_api(monster_name):
    pre_formatted_url = "https://www.tibiawiki.com.br/api.php?action=opensearch&search="
    parsed_monster_name = monster_name.replace(" ", "%20")
    request_url = pre_formatted_url + parsed_monster_name

    response = requests.get(request_url)

    return response.text


def get_tibiawiki_monster_page_content(monster_name):
    pre_formatted_url = "https://www.tibiawiki.com.br/api.php?action=query&prop=revisions&rvprop=content&titles="
    parsed_monster_name = monster_name.replace(" ", "%20")
    request_url = pre_formatted_url + parsed_monster_name

    response = requests.get(request_url)

    return response.text


def get_tibiawiki_monster_loot_single_list(monster_page_raw):
    # Im going for readability and logic progress, not performance! Dont be a jerk.

    loot_kind_as_on_html = ["lootcomum", "lootincomum", "lootsemiraro", "lootraro", "lootmuitoraro", "lootRaid"]
    parsed_list_response = []

    query = re.compile("\<pre class=.+\>\{.+\"\*\"\:\s\"(\{\{.+\}\}).*\}\<", flags=re.DOTALL)
    result = query.search(monster_page_raw)

    for kind in loot_kind_as_on_html:
        try:
            print("Getting Monster's {0}".format(kind))
            expression = "{0}\s+\=\s(.*?)\|".format(kind)
            loot_str = re.compile(expression).search(result.group(1)).group(1).replace("\\n", "")
            loot_final = [x.replace("[", "").replace("]", "") for x in re.findall("\[\[.+?\]\]", loot_str)]
            # print(loot_final)
        except:
            print("FAILED, but I'll ignore. Maybe this monster doesn't have this kind of loot.")
        else:
            print("OK, adding this loot list to the response.")
            parsed_list_response = parsed_list_response + loot_final

    return parsed_list_response


def get_tibiawiki_monster_loot_by_probability(monster_page_raw):
    # Im going for readability and logic progress, not performance! Dont be a jerk.

    query = re.compile("\<pre class=.+\>\{.+\"\*\"\:\s\"(\{\{.+\}\}).*\}\<", flags=re.DOTALL)
    result = query.search(monster_page_raw)

    loot_common_str = re.compile("lootcomum\s+\=\s(.*?)\|").search(result.group(1)).group(1).replace("\\n", "")
    loot_common_final = [x.replace("[", "").replace("]", "") for x in re.findall("\[\[.+?\]\]", loot_common_str)]

    loot_uncommon_str = re.compile("lootincomum\s+\=\s(.*?)\|").search(result.group(1)).group(1).replace("\\n", "")
    loot_uncommon_final = [x.replace("[", "").replace("]", "") for x in re.findall("\[\[.+?\]\]", loot_uncommon_str)]

    loot_semirare_str = re.compile("lootsemiraro\s+\=\s(.*?)\|").search(result.group(1)).group(1).replace("\\n", "")
    loot_semirare_final = [x.replace("[", "").replace("]", "") for x in re.findall("\[\[.+?\]\]", loot_semirare_str)]

    loot_rare_str = re.compile("lootraro\s+\=\s(.*?)\|").search(result.group(1)).group(1).replace("\\n", "")
    loot_rare_final = [x.replace("[", "").replace("]", "") for x in re.findall("\[\[.+?\]\]", loot_rare_str)]

    parsed_dict_response = {"common": loot_common_final, "uncommon": loot_uncommon_final,
                            "semi-rare": loot_semirare_final, "rare": loot_rare_final}

    return parsed_dict_response


def get_loot_list_item_id(loot_list):
    item_id_dict = get_tibia_id_dict()
    monster_item_id_dict = {}

    for item in loot_list:
        monster_item_id_dict[item] = item_id_dict[item]

    return monster_item_id_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # 1-) Then, I'll load the the monster
    print("Please enter the monster name: ")
    monster_name = input()

    # 2-) Now, I'll retrieve the monster loot id dict
    monster_loot = get_tibiawiki_monster_loot_single_list(get_tibiawiki_monster_page_content(monster_name))

    # 3-) Now, I'll search for each loot item, to get the respective ID
    final_monster_item_id_dict = get_loot_list_item_id(monster_loot)

    # 4-) Just a pretty print.
    print("################ {0}'s Loot Item ID REPORT ################".format(monster_name))
    for item in final_monster_item_id_dict:
        print("ITEM NAME: {0} --- ID: {1}".format(item, final_monster_item_id_dict[item]))
    print("###########################################################".format(monster_name))
    print()
    print("Done!")
