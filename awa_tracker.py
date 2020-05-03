import re
from selenium import webdriver

domain_file = "domain.txt"
links_file = "links.txt"
output_file = "out.txt"
chromedriver_file = "chromedriver_location.txt"

with open(domain_file) as f:
  domain_name = f.read()

with open(links_file) as f:
  links_str = f.read()

with open(chromedriver_file) as f:
  chromedriver_location = f.read()

item_pattern = re.escape('<div class="col-12 col-md-4">')
extract_link_pattern = "{}.*?{}(.*?){}.*?{}".format(re.escape('<div class="col-12 col-md-4">'), re.escape('<a href="'), re.escape('">'), re.escape('</a>'))

num_items = len(re.findall(item_pattern, links_str, re.DOTALL))
links = re.findall(extract_link_pattern, links_str, re.DOTALL)

if len(links) != num_items:
  print("Could not find all links.")
  exit()

output_f = open(output_file, "w")
print("link,state", file=output_f)

driver = webdriver.Chrome(chromedriver_location)
for l in links:
  link = "{}{}".format(domain_name, l)
  driver.get(link)

  state = "error"

  try:
    if not driver.find_element_by_id("get-key-actions").get_attribute("style"):
      state = "available"
      print("\"{}\",\"{}\"".format(link, state))
    elif not driver.find_element_by_id("no-keys-left-until-level").get_attribute("style"):
      state = "available_with_level"
      print("\"{}\",\"{}\"".format(link, state))
    elif not driver.find_element_by_id("no-keys-left").get_attribute("style"):
      state = "unavailable"
      print("\"{}\",\"{}\"".format(link, state))
    else:
      print("Error: {}".format(link))
  except:
    print("Error: {}".format(link))

  print("\"{}\",\"{}\"".format(link, state), file=output_f)

output_f.close()

