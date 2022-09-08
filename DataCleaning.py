helptxt = """
DataCleaning form ljw
include 1 function and 1 class

Function:
    VarSplit

Class:
    StructData:
        Attrs:
            self. brief={Terms:ls[str],
                        Times:ls[int],
                        Vars:ls[int]}
            self. data
    
        Methods:
            self.WriteLong()
            self.WriteWide()

Example:
    a = StructData("filename.csv", "wide", timename="year", code="UTF-8-sig")
    a.WriteLong("done.csv")
"""


def Help():
	print(helptxt)


def VarSplit(VarName: str) -> (str, int):
	nums = '0123456789'
	if VarName == "":
		var = ""
		year = None
	else:
		if VarName[-1] not in nums:
			var = VarName
			year = None
		else:
			i = -1
			for i in range(len(VarName) - 1, -1, -1):
				if VarName[i] not in nums:
					i += 1
					break
			var = VarName[:i]
			year = eval(VarName[i:].removeprefix("0"))
	return var, year


class StructData:
	"""
	Attrs:
		self. brief={Terms:list[str],
					Times:list[int],
					Vars:list[str]}
		self. data:a dictionary val=data[term:str][time:int][var:str]

	Methods:
		self.WriteLong()
		self.WriteWide()
	"""
	
	@staticmethod
	def __FmtCheck(ls: list):
		lens = set()
		for i in ls:
			lens.add(len(i))
		if len(lens) > 1:
			raise Exception("表格宽度不一致!")
	
	def __init__(self, filename: str, LongORWide: str, TermsIndex=0, TimesIndex=1, timename="time", code="UTF-8-sig"):
		with open(filename, "r", encoding=code) as f:
			ls = f.read().strip(" ").strip(",").strip("\n").split("\n")
		for i, iv in enumerate(ls):
			ls[i] = iv.split(",")
		StructData.__FmtCheck(ls)
		TermName = ""
		TermsLS = []
		TimeName = ""
		TimesLS = []
		VarsLS = []
		if LongORWide.lower() in ["long", "l"]:
			for i, iv in enumerate(ls):
				if i == 0:
					for j, jv in enumerate(iv):
						if j == TermsIndex:
							TermName = jv
						elif j == TimesIndex:
							TimeName = jv
						else:
							if jv not in VarsLS:
								VarsLS.append(jv)
				else:
					tempTerm = iv[TermsIndex]
					tempTime = iv[TimesIndex]
					if tempTerm not in TermsLS:
						TermsLS.append(tempTerm)
					if tempTime not in TimesLS:
						TimesLS.append(tempTime)
		elif LongORWide.lower() in ["wide", "w"]:
			TimeName = timename
			for i, iv in enumerate(ls):
				if i == 0:
					for j, jv in enumerate(iv):
						if j == TermsIndex:
							TermName = jv
						else:
							tempVar, tempTime = VarSplit(jv)
							if tempVar not in VarsLS:
								VarsLS.append(tempVar)
							if tempTime is not None:
								if tempTime not in TimesLS:
									TimesLS.append(tempTime)
				else:
					tempTerm = iv[TermsIndex]
					if tempTerm not in TermsLS:
						TermsLS.append(tempTerm)
		else:
			raise Exception("格式输入错误")
		TimesLS.sort()
		self.brief = [[TermName, TermsLS], [TimeName, TimesLS], ["Vars", VarsLS]]
		self.data = {}
		for i in TermsLS:
			self.data[i] = {}
			for j in TimesLS:
				self.data[i][j] = {}
				for k in VarsLS:
					self.data[i][j][k] = ""
		print("数据初始化开始，请等待...")
		if LongORWide.lower() in ["long", "l"]:
			for i, iv in enumerate(ls):
				if i != 0:
					for j, jv in enumerate(iv):
						if j != TermsIndex and j != TimesIndex:
							self.data[iv[TermsIndex]][iv[TimesIndex]][ls[0][j]] = jv
		elif LongORWide.lower() in ["wide", "w"]:
			n = len(ls)
			for i, iv in enumerate(ls):
				if i != 0:
					for j, jv in enumerate(iv):
						if j != TermsIndex:
							tempVar, tempTime = VarSplit(ls[0][j])
							if tempTime is None:
								for k in TimesLS:
									self.data[iv[TermsIndex]][k][tempVar] = jv
							else:
								self.data[iv[TermsIndex]][tempTime][tempVar] = jv
				print("已完成{:.2f}%\r".format((i + 1) / n * 100))
		print("数据初始化完成")
		print(self)
	
	def __str__(self):
		OutStr = "attr:" + "\n"
		brief = self.brief
		for i in [0, 1, 2]:
			for j in [0, 1]:
				OutStr += str(brief[i][j]) + "\n"
		return OutStr
	
	def WriteWide(self, filename: str = "done.csv"):
		print("写入开始...")
		RAW = self.data
		Brief = self.brief
		with open(filename, "w", encoding="UTF-8-sig") as f:
			TempStr = Brief[0][0]
			for i in Brief[2][1]:
				for j in Brief[1][1]:
					TempStr += "," + i + str(j)
			f.write(TempStr + "\n")
			for term in Brief[0][1]:
				TempStr = term
				for var in Brief[2][1]:
					for time in Brief[1][1]:
						TempStr += "," + RAW[term][time][var]
				f.write(TempStr + "\n")
		print("写入已完成")
	
	def WriteLong(self, filename: str = "done.csv"):
		print("写入开始...")
		RAW = self.data
		Brief = self.brief
		with open(filename, "w", encoding="UTF-8-sig") as f:
			TempStr = Brief[0][0] + "," + Brief[1][0]
			for i in Brief[2][1]:
				TempStr += "," + i
			f.write(TempStr + "\n")
			for i in Brief[0][1]:
				for j in Brief[1][1]:
					TempStr = i + ","
					TempStr += str(j)
					for k in Brief[2][1]:
						TempStr += "," + RAW[i][j][k]
					f.write(TempStr + "\n")
		print("写入已完成")