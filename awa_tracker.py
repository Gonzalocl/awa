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

