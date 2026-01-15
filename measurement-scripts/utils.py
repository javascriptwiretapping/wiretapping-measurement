import os
import requests
from adblockparser import AdblockRules
import json
import pandas as pd
from os.path import basename
import re
from urllib.parse import urlparse
import tldextract
import ast

with open("entities.json", "r") as f:
    entities = json.load(f)
    entities = entities["entities"]

disconnect_entity_map = {}


def get_exfiltration_types(script_domain):
    # 1) Filter down to only the rows you care about
    df_filtered = df_requests[
        (df_requests.calling_script_domain.str.contains(script_domain, na=False))
        & (df_requests.data_leak == True)
    ].copy()

    # 2) If data_leak_type is coming in as a string like "['mail','tel']",
    #    turn it into an actual Python list:
    df_filtered["data_leak_type"] = df_filtered["data_leak_type"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    # 3) Now explode out the list to one row per single leak-type
    df_exploded = df_filtered.explode("data_leak_type")

    # 4) Drop any null entries (in case some rows had empty lists or None)
    df_exploded = df_exploded[df_exploded.data_leak_type.notnull()]

    # 5) If you want the *number of distinct sites* per leak-type:
    result = (
        df_exploded.drop_duplicates(["site_domain", "data_leak_type"])
        .groupby("data_leak_type")["site_domain"]
        .nunique()
        .reset_index(name="site_count")
    )

    return result


def read_file_newline_stripped(fname):

    with open(fname) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    return lines


def create_filterlist_rules(filterlist_dir):

    filterlist_rules = {}
    filterlists = os.listdir(filterlist_dir)
    for fname in filterlists:
        rule_dict = {}
        rules = read_file_newline_stripped(os.path.join(filterlist_dir, fname))
        rule_dict["script"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["script", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["script_third"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["third-party", "script", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["image"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["image", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["image_third"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["third-party", "image", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["css"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["stylesheet", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["css_third"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["third-party", "stylesheet", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["xmlhttp"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["xmlhttprequest", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["xmlhttp_third"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=[
                "third-party",
                "xmlhttprequest",
                "domain",
                "subdocument",
            ],
            skip_unsupported_rules=False,
        )
        rule_dict["third"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["third-party", "domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        rule_dict["domain"] = AdblockRules(
            rules,
            use_re2=False,
            max_mem=1024 * 1024 * 1024,
            supported_options=["domain", "subdocument"],
            skip_unsupported_rules=False,
        )
        filterlist_rules[fname] = rule_dict

    return filterlists, filterlist_rules


def build_disconnect_entity_map():
    for key in entities.keys():
        properties = entities[key]["properties"]
        resources = entities[key]["resources"]
        for p in properties:
            if p not in disconnect_entity_map:
                disconnect_entity_map[p] = key
        for r in resources:
            if r not in disconnect_entity_map:
                disconnect_entity_map[r] = key


# This will run one time to build a map for faster searching
with open("tracker-radar/build-data/generated/entity_map.json") as f:
    tracker_radar = json.load(f)

duck_entity_map = {}


def get_disconnect_entity(url):
    if url in disconnect_entity_map:
        return disconnect_entity_map[url]
    else:
        return url


def build_duck_entity_map():
    for key in tracker_radar.keys():
        props = tracker_radar[key]["properties"]
        for p in props:
            if p not in duck_entity_map:
                duck_entity_map[p] = key


def get_duck_duck_go_entity(url):
    if url in duck_entity_map:
        return duck_entity_map[url]
    else:
        return url


build_disconnect_entity_map()
build_duck_entity_map()

# download_lists("filterlists")
filterlists, filterlist_rules = create_filterlist_rules("filterlists")


def label_request_url(row, filterlists, filterlist_rules):
    try:
        top_domain = row.site_domain
        request_url = row.url
        request_domain = row.request_domain
        resource_type = "xmlhttprequest"

        label = False

        # print(f"Processing {request_url} from {top_domain}")

        for fl in filterlists:
            if top_domain and request_domain:
                list_label = match_url(
                    top_domain,
                    request_domain,
                    request_url,
                    resource_type,
                    filterlist_rules[fl],
                )

                label = label | list_label
            else:
                return pd.NA
        return label
    except:
        return pd.NA


def get_entity(url):
    entity = get_duck_duck_go_entity(url)
    entity = get_disconnect_entity(entity)
    return entity


# get etld+1 domain
def get_domain(url):
    if pd.isnull(url):
        return None
    ext = tldextract.extract(url)
    return ext.domain + "." + ext.suffix


def find_script_in_callstack_json(callstack_json):
    try:
        callstack_json = json.loads(callstack_json)

        if callstack_json["type"] == "script":
            try:
                callFrames = callstack_json["stack"]["callFrames"]
                for callFrame in callFrames:
                    if callFrame["url"] != "":
                        return callFrame["url"]
            except:
                return pd.NA
            return pd.NA
    except:
        return pd.NA

    return pd.NA


def get_javascript_filename(url):
    if url is None or pd.isna(url):
        return pd.NA

    # Parse the URL and get the base filename
    parsed_path = urlparse(url).path
    filename = basename(parsed_path)

    # Remove any trailing line/column information with or without a closing parenthesis
    cleaned_filename = re.sub(r":\d+(:\d+)?\)?$", "", filename)

    return cleaned_filename


def find_first_url_in_callstack(callstack):
    for line in callstack.split("\n"):
        if line.startswith("    at "):
            line = line.strip()
            if line.endswith(")"):
                line = line.split("(")[1]
            if line.startswith("http"):
                return line
    return None


def get_resource_type(attr):

    try:
        attr = json.loads(attr)
        return attr["content_policy_type"]
    except Exception as e:
        # print("error in type", e)
        return None
    return None


def download_lists(FILTERLIST_DIR):
    """
    Function to download the lists used in AdGraph.
    Args:
            FILTERLIST_DIR: Path of the output directory to which filter lists should be written.
    Returns:
            Nothing, writes the lists to a directory.
    This functions does the following:
    1. Sends HTTP requests for the lists used in AdGraph.
    2. Writes to an output directory.
    """

    raw_lists = {
        "easylist": "https://easylist.to/easylist/easylist.txt",
        "easyprivacy": "https://easylist.to/easylist/easyprivacy.txt",
        # "antiadblock": "https://raw.github.com/reek/anti-adblock-killer/master/anti-adblock-killer-filters.txt",
        # "blockzilla": "https://raw.githubusercontent.com/annon79/Blockzilla/master/Blockzilla.txt",
        # "fanboyannoyance": "https://easylist.to/easylist/fanboy-annoyance.txt",
        # "fanboysocial": "https://easylist.to/easylist/fanboy-social.txt",
        # "peterlowe": "http://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&mimetype=plaintext",
        # "squid": "http://www.squidblacklist.org/downloads/sbl-adblock.acl",
        # "warning": "https://easylist-downloads.adblockplus.org/antiadblockfilters.txt",
    }

    for listname, url in raw_lists.items():
        with open(os.path.join(FILTERLIST_DIR, "%s.txt" % listname), "wb") as f:
            f.write(requests.get(url).content)


def match_url(domain_top_level, current_domain, current_url, resource_type, rules_dict):

    try:
        if domain_top_level == current_domain:
            third_party_check = False
        else:
            third_party_check = True

        if resource_type == "sub_frame":
            subdocument_check = True
        else:
            subdocument_check = False

        if resource_type == "script":
            if third_party_check:
                rules = rules_dict["script_third"]
                options = {
                    "third-party": True,
                    "script": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }
            else:
                rules = rules_dict["script"]
                options = {
                    "script": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }

        elif resource_type == "image" or resource_type == "imageset":
            if third_party_check:
                rules = rules_dict["image_third"]
                options = {
                    "third-party": True,
                    "image": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }
            else:
                rules = rules_dict["image"]
                options = {
                    "image": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }

        elif resource_type == "stylesheet":
            if third_party_check:
                rules = rules_dict["css_third"]
                options = {
                    "third-party": True,
                    "stylesheet": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }
            else:
                rules = rules_dict["css"]
                options = {
                    "stylesheet": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }

        elif resource_type == "xmlhttprequest":
            if third_party_check:
                rules = rules_dict["xmlhttp_third"]
                options = {
                    "third-party": True,
                    "xmlhttprequest": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }
            else:
                rules = rules_dict["xmlhttp"]
                options = {
                    "xmlhttprequest": True,
                    "domain": domain_top_level,
                    "subdocument": subdocument_check,
                }

        elif third_party_check:
            rules = rules_dict["third"]
            options = {
                "third-party": True,
                "domain": domain_top_level,
                "subdocument": subdocument_check,
            }

        else:
            rules = rules_dict["domain"]
            options = {"domain": domain_top_level, "subdocument": subdocument_check}

        return rules.should_block(current_url, options)

    except Exception as e:
        print("Exception encountered", e)
        print("top url", domain_top_level)
        print("current url", current_domain)
        return False


def label_setter_data(row, filterlists, filterlist_rules):

    try:
        top_domain = row["top_level_domain"]
        setter_url = row["setter"]
        setter_domain = row["setter_domain"]
        resource_type = row["resource_type"]
        data_label = False

        for fl in filterlists:
            if top_domain and setter_domain:
                list_label = match_url(
                    top_domain,
                    setter_domain,
                    setter_url,
                    resource_type,
                    filterlist_rules[fl],
                )
                data_label = data_label | list_label
            else:
                data_label = "Error"
    except:
        data_label = "Error"

    return data_label
