import re
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open('tests/20130120173004-0.eml') as f:
	data = f.readlines()
	data = "".join(data)

	pat = re.compile(r"^(---\n.*?)\n\n", re.S|re.M)
	result = pat.findall(data)

	if len(result) > 0:
		xarf = load(result[0], Loader=Loader)
		print xarf