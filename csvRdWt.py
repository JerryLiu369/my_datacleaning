def readcsv(filename: str):
	with open(filename, "r", encoding="UTF-8-sig") as f:
		ret = f.read().strip(" ").strip("\n").split("\n")
		retdic = {}
		for i, v in enumerate(ret):
			ret[i] = v.split(",")
		for i, v in enumerate(ret[0]):
			retdic[v] = i
		return ret, retdic


def writecsv(ls: list[list], filename: str = "done"):
	with open(filename + ".csv", "w", encoding="UTF-8-sig") as f:
		for row in ls:
			tempstr = ""
			for val in row:
				tempstr += str(val) + ","
			f.write(tempstr[:-1:] + "\n")