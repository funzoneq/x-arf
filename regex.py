import os
import re
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

for files in os.listdir("tests/"):
	with open('tests/%s' % files) as f:
		data = f.readlines()
		data = "".join(data)

		pat = re.compile(r"^(---\n.*?)\n\n", re.S|re.M)
		result = pat.findall(data)

		if len(result) > 0:
			xarf = load(result[0], Loader=Loader)
			print xarf