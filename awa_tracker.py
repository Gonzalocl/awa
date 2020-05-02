import re
import requests

domain_file = "domain.txt"
links_file = "links.txt"
output_file = "out.txt"

with open(domain_file) as f:
  domain_name = f.read()

with open(links_file) as f:
  links_str = f.read()

item_pattern = re.escape('<div class="col-12 col-md-4">')
extract_link_pattern = "{}.*?{}(.*?){}.*?{}".format(re.escape('<div class="col-12 col-md-4">'), re.escape('<a href="'), re.escape('">'), re.escape('</a>'))

num_items = len(re.findall(item_pattern, links_str, re.DOTALL))
links = re.findall(extract_link_pattern, links_str, re.DOTALL)

if len(links) != num_items:
  print("Could not find all links.")
  exit()

style_displayed = 'style=""'
style_no_displayed = 'style="display:none;"'

get_key_actions_pattern = "{}({}|{}){}".format(re.escape('<div id="get-key-actions" '),
                                               re.escape(style_displayed),
                                               re.escape(style_no_displayed),
                                               re.escape('>'))

no_keys_left_until_level_pattern = "{}({}|{}){}".format(re.escape('<span class="text-danger" id="no-keys-left-until-level" '),
                                                        re.escape(style_displayed),
                                                        re.escape(style_no_displayed),
                                                        re.escape('>'))

no_keys_left = "{}({}|{}){}".format(re.escape('<span class="text-danger" id="no-keys-left" '),
                                    re.escape(style_displayed),
                                    re.escape(style_no_displayed),
                                    re.escape('>'))

output_f = open(output_file, "w")
print("link,state", file=output_f)

for l in links:
  link = "{}{}".format(domain_name, l)
  req = str(requests.get(link).content)

  available = False
  available_level = False
  not_available = False

  match_item_available = re.search(get_key_actions_pattern, req, re.DOTALL)
  print(match_item_available.group(1))
  if match_item_available.group(1) == style_displayed:
    available = True
  elif match_item_available.group(1) == style_no_displayed:
    pass
  else:
    print("error match_item_available: {}".format(link))

  match_item_available_level = re.search(no_keys_left_until_level_pattern, req, re.DOTALL)
  print(match_item_available_level.group(1))
  if match_item_available_level.group(1) == style_displayed:
    available_level = True
  elif match_item_available_level.group(1) == style_no_displayed:
    pass
  else:
    print("error match_item_available_level: {}".format(link))

  match_item_not_available = re.search(no_keys_left, req, re.DOTALL)
  print(match_item_not_available.group(1))
  if match_item_not_available.group(1) == style_displayed:
    not_available = True
  elif match_item_not_available.group(1) == style_no_displayed:
    pass
  else:
    print("error match_item_not_available: {}".format(link))

  if available and not available_level and not not_available:
    print("{},{}".format(link, "available"), file=output_f)
  elif not available and available_level and not not_available:
    print("{},{}".format(link, "available_level"), file=output_f)
  elif not available and not available_level and not_available:
    print("{},{}".format(link, "not_available"), file=output_f)
  else:
    print("error multiple: {}".format(link))

  output_f.close()
  exit()

output_f.close()
