import re

domain_file = "domain.txt"
links_file = "links.txt"

with open(domain_file) as f:
  domain_name = f.read()

with open(links_file) as f:
  links = f.read()

print(domain_name)
print(links)
