from .object import TailwindObject, parseTwObj, mergeTwObj, toTwObj

def twMerge(*className: str) -> str:
	# ユーティリティ部が特定の値から始まっているか
	def startUtility(target: list[str], start: list[str]):
		if len(target) >= len(start):
			for i in range(0, len(start), 1):
				if target[i] != start[i]:
					return False
			return True
		
		return False
	
	# ユーティリティ部が一致しているか
	def matchUtility(target: list[str], comparison: list[str]):
		if len(target) == len(comparison):
			for i in range(0, len(target), 1):
				if target[i] != comparison[i]:
					return False
			return True
		return False
	
	# ユーティリティ部がいずれかと一致しているか
	def matchUtilitiesOr(target: list[str], *comparison_utils: list[str]):
		for comparison in comparison_utils:
			if matchUtility(target, comparison):
				return True
		return False

	# ユーティリティ部が特定の値+サイズから始まるか
	def startSizeUtility(target: list[str], start: list[str]):
		if not startUtility(target, start):
			return False
		
		if len(target) >= len(start) + 1:
			s = str(target[len(start)])

			ls = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl", "8xl", "9xl"]
			for v in ls:
				if s == v or s[:len(v) + 1] == v + "/":
					return True
			
			if s[:1] == "[":
				c = s[1:2]
				if c == "0" or c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9":
					return True
				elif s[:6] == "[calc(":
					return True

		return False
	
	# ユーティリティ部が特定の値+色から始まるか
	def startColorUtility(target: list[str], start: list[str]):
		if (not startUtility(target, start)) or len(target) < len(start) + 1:
			return False
		
		s = target[len(start)]
		ls = ["inherit", "current", "transparent", "black", "white"]
		for v in ls:
			if s == v or s[:len(v) + 1] == v + "/":
				return True
		
		if s in ["slate", "gray", "zinc", "neutral", "stone", "red", "orange", "amber", "yellow", "lime", "green", "emerald", "teal", "cyan", "sky", "blue", "indigo", "violet", "purple", "fuchsia", "pink", "rose"]:
			return True
		elif s[:len("[rgb(")] == "[rgb(" or s[:len("[#")] == "[#":
			return True

		return False
	
	# ユーティリティ部が特定の値+数値から始まるか
	def startNumberUtility(target: list[str], start: list[str]):
		if (not startUtility(target, start)) or len(target) < len(start) + 1:
			return False
		
		s = target[len(start)]
		if s[:1] == "[" and s[-1:] == "]":
			try:
				n = float(s[1:-1])
				return True
			except:
				return False
		
		return False
	
	# ユーティリティ部が特定の値+(top,bottom,left,right,center系)から始まるか
	def startPositionUtility(target: list[str], start: list[str]):
		if (not startUtility(target, start)) or len(target) < len(start) + 1:
			return False

		ls = ["bottom", "center", "left", "right", "top"]
		s = target[len(start)]
		if s in ls:
			return True
		elif s[:1] == "[":
			for v in ls:
				if target[:len(v) + 1] == ("[" + v):
					return True
		return False
	
	# ユーティリティ部が特定の値+割合から始まるか
	def startPercentUtility(target: list[str], start: list[str]):
		if (not startUtility(target, start)) or len(target) < len(start) + 1:
			return False
		
		s = target[len(start)]
		if s[-1:] == "%":
			try:
				n = int(s[:-1])
				return True
			except:
				pass
		elif s[:1] + s[-1:] == "[]":
			if s[-2:] == "%":
				try:
					n = int(s[1:-2])
					return True
				except:
					pass
			else:
				try:
					n = float(s[1:-1])
					return True
				except:
					pass
		return False
	
	# どちらのユーティリティも比較関数の結果がTrueになるか
	def dblChk(target1: list[str], target2: list[str], function, *args):
		return function(target1, *args) and function(target2, *args)
	
	# いずれかのユーティリティの比較関数の結果がTrueになるか
	def orChk(target1: list[str], target2: list[str], function, *args):
		return function(target1, *args) or function(target2, *args)
	
	merged_twobj: dict[str, list[TailwindObject]] = {}
	for class_name in className:
		splited = str(class_name).split(" ")
		class_names: list[TailwindObject] = []
		for split in splited:
			if split == "":
				continue
			else:
				twobj_ls = toTwObj(split)
				for twobj in twobj_ls:
					class_names.append(twobj)
		
		for c in class_names:
			c_selector, c_utility = c
			
			cu_minus = False
			if c_utility[:1] == [""]:
				cu_minus = True
				c_utility = c_utility[1:]
			
			if c_selector in merged_twobj:
				for i in reversed(range(0, len(merged_twobj[c_selector]), 1)):
					m_selector, m_utility = merged_twobj[c_selector][i]
					if len(c_utility) == len(m_utility):
						if startUtility(c_utility, m_utility):
							del merged_twobj[c_selector][i]
							continue
					
					mu_minus = False
					if m_utility[:1] == [""]:
						mu_minus = True
						m_utility = m_utility[1:]
					
					if orChk(c_utility, m_utility, startUtility, ["aspect"]):
						if dblChk(c_utility, m_utility, startUtility, ["aspect"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["columns"]):
						if dblChk(c_utility, m_utility, startUtility, ["columns"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["break", "after"]):
						if dblChk(c_utility, m_utility, startUtility, ["break", "after"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["break", "before"]):
						if dblChk(c_utility, m_utility, startUtility, ["break", "before"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["break", "inside"]):
						if dblChk(c_utility, m_utility, startUtility, ["break", "inside"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["box", "decoration"]):
						if dblChk(c_utility, m_utility, startUtility, ["box", "decoration"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["box", "border"], ["box", "content"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["box", "border"], ["box", "content"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["block"], ["inline", "block"], ["inline"], ["flex"], ["inline", "flex"], ["table"], ["inline", "table"], ["table", "caption"], ["table", "cell"], ["table", "column"], ["table", "column", "group"], ["table", "footer", "group"], ["table", "header", "group"], ["table", "row", "group"], ["table", "row"], ["flow", "root"], ["grid"], ["inline", "grid"], ["contents"], ["list", "item"], ["hidden"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["block"], ["inline", "block"], ["inline"], ["flex"], ["inline", "flex"], ["table"], ["inline", "table"], ["table", "caption"], ["table", "cell"], ["table", "column"], ["table", "column", "group"], ["table", "footer", "group"], ["table", "header", "group"], ["table", "row", "group"], ["table", "row"], ["flow", "root"], ["grid"], ["inline", "grid"], ["contents"], ["list", "item"], ["hidden"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["float"]):
						if dblChk(c_utility, m_utility, startUtility, ["float"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["clear"]):
						if dblChk(c_utility, m_utility, startUtility, ["clear"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["isolate"], ["isolate", "auto"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["isolate"], ["isolate", "auto"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["object", "contain"], ["object", "cover"], ["object", "fill"], ["object", "none"], ["object", "scale", "down"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["object", "contain"], ["object", "cover"], ["object", "fill"], ["object", "none"], ["object", "scale", "down"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startPositionUtility, ["object"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["object", "bottom"], ["object", "center"], ["object", "left"], ["object", "left", "bottom"], ["object", "left", "top"], ["object", "right"], ["object", "right", "bottom"], ["object", "right", "top"], ["object", "top"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["overflow"]):
						if dblChk(c_utility, m_utility, startUtility, ["overflow"]):
							if startUtility(c_utility, ["overflow", "x"]) or startUtility(m_utility, ["overflow", "x"]):
								if dblChk(c_utility, m_utility, startUtility, ["overflow", "x"]):
									del merged_twobj[c_selector][i]
							elif startUtility(c_utility, ["overflow", "y"]) or startUtility(m_utility, ["overflow", "y"]):
								if dblChk(c_utility, m_utility, startUtility, ["overflow", "y"]):
									del merged_twobj[c_selector][i]
							else:
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["overscroll"]):
						if dblChk(c_utility, m_utility, startUtility, ["overscroll"]):
							if startUtility(c_utility, ["overscroll", "x"]) or startUtility(m_utility, ["overscroll", "x"]):
								if dblChk(c_utility, m_utility, startUtility, ["overscroll", "x"]):
									del merged_twobj[c_selector][i]
							elif startUtility(c_utility, ["overscroll", "y"]) or startUtility(m_utility, ["overscroll", "y"]):
								if dblChk(c_utility, m_utility, startUtility, ["overscroll", "y"]):
									del merged_twobj[c_selector][i]
							else:
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["static"], ["fixed"], ["absolute"], ["relative"], ["sticky"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["static"], ["fixed"], ["absolute"], ["relative"], ["sticky"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["top"]):
						if dblChk(c_utility, m_utility, startUtility, ["top"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["right"]):
						if dblChk(c_utility, m_utility, startUtility, ["right"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["bottom"]):
						if dblChk(c_utility, m_utility, startUtility, ["bottom"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["left"]):
						if dblChk(c_utility, m_utility, startUtility, ["left"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["start"]):
						if dblChk(c_utility, m_utility, startUtility, ["start"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["end"]):
						if dblChk(c_utility, m_utility, startUtility, ["end"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["visible"], ["invisible"], ["collapse"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["visible"], ["invisible"], ["collapse"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["z"]):
						if dblChk(c_utility, m_utility, startUtility, ["z"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["basis"]):
						if dblChk(c_utility, m_utility, startUtility, ["basis"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["flex", "row"], ["flex", "row", "reverse"], ["flex", "col"], ["flex", "col", "reverse"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["flex", "row"], ["flex", "row", "reverse"], ["flex", "col"], ["flex", "col", "reverse"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["flex", "wrap"], ["flex", "wrap", "reverse"], ["flex", "nowrap"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["flex", "wrap"], ["flex", "wrap", "reverse"], ["flex", "nowrap"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["flex"]):
						if dblChk(c_utility, m_utility, startUtility, ["flex"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["grow"]):
						if dblChk(c_utility, m_utility, startUtility, ["grow"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["shrink"]):
						if dblChk(c_utility, m_utility, startUtility, ["shrink"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["order"]):
						if dblChk(c_utility, m_utility, startUtility, ["order"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["grid", "cols"]):
						if dblChk(c_utility, m_utility, startUtility, ["grid", "cols"]):
							del merged_twobj[c_selector][i]
					elif (startUtility(c_utility, ["col", "span"]) or matchUtility(c_utility, ["col", "auto"])) or (startUtility(m_utility, ["col", "span"]) or matchUtility(m_utility, ["col", "auto"])):
						if (startUtility(c_utility, ["col", "span"]) or matchUtility(c_utility, ["col", "auto"])) and (startUtility(m_utility, ["col", "span"]) or matchUtility(m_utility, ["col", "auto"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["col", "start"]):
						if dblChk(c_utility, m_utility, startUtility, ["col", "start"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["col", "end"]):
						if dblChk(c_utility, m_utility, startUtility, ["col", "end"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["grid", "rows"]):
						if dblChk(c_utility, m_utility, startUtility, ["grid", "rows"]):
							del merged_twobj[c_selector][i]
					elif (startUtility(c_utility, ["row", "span"]) or matchUtility(c_utility, ["row", "auto"])) or (startUtility(m_utility, ["row", "span"]) or matchUtility(m_utility, ["row", "auto"])):
						if (startUtility(c_utility, ["row", "span"]) or matchUtility(c_utility, ["row", "auto"])) and (startUtility(m_utility, ["row", "span"]) or matchUtility(m_utility, ["row", "auto"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["row", "start"]):
						if dblChk(c_utility, m_utility, startUtility, ["row", "start"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["row", "end"]):
						if dblChk(c_utility, m_utility, startUtility, ["row", "end"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["grid", "flow"]):
						if dblChk(c_utility, m_utility, startUtility, ["grid", "flow"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["auto", "cols"]):
						if dblChk(c_utility, m_utility, startUtility, ["auto", "cols"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["auto", "rows"]):
						if dblChk(c_utility, m_utility, startUtility, ["auto", "rows"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["gap"]):
						if dblChk(c_utility, m_utility, startUtility, ["gap"]):
							if startUtility(c_utility, ["gap", "x"]) or startUtility(m_utility, ["gap", "x"]):
								if dblChk(c_utility, m_utility, startUtility, ["gap", "x"]):
									del merged_twobj[c_selector][i]
							elif startUtility(c_utility, ["gap", "y"]) or startUtility(m_utility, ["gap", "y"]):
								if dblChk(c_utility, m_utility, startUtility, ["gap", "y"]):
									del merged_twobj[c_selector][i]
							else:
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["justify", "normal"], ["justify", "start"], ["justify", "end"], ["justify", "center"], ["justify", "between"], ["justify", "around"], ["justify", "evenly"], ["justify", "stretch"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["justify", "normal"], ["justify", "start"], ["justify", "end"], ["justify", "center"], ["justify", "between"], ["justify", "around"], ["justify", "evenly"], ["justify", "stretch"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["justify", "items"]):
						if dblChk(c_utility, m_utility, startUtility, ["justify", "items"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["justify", "self"]):
						if dblChk(c_utility, m_utility, startUtility, ["justify", "self"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["content", "normal"], ["content", "center"], ["content", "start"], ["content", "end"], ["content", "between"], ["content", "around"], ["content", "evenly"], ["content", "baseline"], ["content", "stretch"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["content", "normal"], ["content", "center"], ["content", "start"], ["content", "end"], ["content", "between"], ["content", "around"], ["content", "evenly"], ["content", "baseline"], ["content", "stretch"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["items"]):
						if dblChk(c_utility, m_utility, startUtility, ["items"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["self"]):
						if dblChk(c_utility, m_utility, startUtility, ["self"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["place", "content"]):
						if dblChk(c_utility, m_utility, startUtility, ["place", "content"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["place", "items"]):
						if dblChk(c_utility, m_utility, startUtility, ["place", "items"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["place", "self"]):
						if dblChk(c_utility, m_utility, startUtility, ["place", "self"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["ps"]):
						if dblChk(c_utility, m_utility, startUtility, ["ps"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["pe"]):
						if dblChk(c_utility, m_utility, startUtility, ["pe"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["pt"]):
						if dblChk(c_utility, m_utility, startUtility, ["pt"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["pr"]):
						if dblChk(c_utility, m_utility, startUtility, ["pr"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["pb"]):
						if dblChk(c_utility, m_utility, startUtility, ["pb"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["pl"]):
						if dblChk(c_utility, m_utility, startUtility, ["pl"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["ms"]):
						if dblChk(c_utility, m_utility, startUtility, ["ms"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["me"]):
						if dblChk(c_utility, m_utility, startUtility, ["me"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["mt"]):
						if dblChk(c_utility, m_utility, startUtility, ["mt"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["mr"]):
						if dblChk(c_utility, m_utility, startUtility, ["mr"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["mb"]):
						if dblChk(c_utility, m_utility, startUtility, ["mb"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["ml"]):
						if dblChk(c_utility, m_utility, startUtility, ["ml"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["space", "x"]):
						if dblChk(c_utility, m_utility, startUtility, ["space", "x"]):
							if not (matchUtility(c_utility, ["space", "x", "reverse"]) or matchUtility(m_utility, ["space", "x", "reverse"])):
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["space", "y"]):
						if dblChk(c_utility, m_utility, startUtility, ["space", "y"]):
							if not (matchUtility(c_utility, ["space", "y", "reverse"]) or matchUtility(m_utility, ["space", "y", "reverse"])):
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["w"]):
						if dblChk(c_utility, m_utility, startUtility, ["w"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["min", "w"]):
						if dblChk(c_utility, m_utility, startUtility, ["min", "w"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["max", "w"]):
						if dblChk(c_utility, m_utility, startUtility, ["max", "w"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["h"]):
						if dblChk(c_utility, m_utility, startUtility, ["h"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["min", "h"]):
						if dblChk(c_utility, m_utility, startUtility, ["min", "h"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["max", "h"]):
						if dblChk(c_utility, m_utility, startUtility, ["max", "h"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["font", "sans"], ["font", "serif"], ["font", "mono"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["font", "sans"], ["font", "serif"], ["font", "mono"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startSizeUtility, ["text"]):
						if dblChk(c_utility, m_utility, startSizeUtility, ["text"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["antialiased"], ["subpixel", "antialiased"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["antialiased"], ["subpixel", "antialiased"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["italic"], ["not", "italic"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["italic"], ["not", "italic"]):
							del merged_twobj[c_selector][i]
					elif (matchUtilitiesOr(c_utility, ["font", "thin"], ["font", "extralight"], ["font", "light"], ["font", "normal"], ["font", "medium"], ["font", "semibold"], ["font", "bold"], ["font", "extrabold"], ["font", "black"]) or startNumberUtility(c_utility, ["font"])) or (matchUtilitiesOr(m_utility, ["font", "thin"], ["font", "extralight"], ["font", "light"], ["font", "normal"], ["font", "medium"], ["font", "semibold"], ["font", "bold"], ["font", "extrabold"], ["font", "black"]) or startNumberUtility(m_utility, ["font"])):
						if (matchUtilitiesOr(c_utility, ["font", "thin"], ["font", "extralight"], ["font", "light"], ["font", "normal"], ["font", "medium"], ["font", "semibold"], ["font", "bold"], ["font", "extrabold"], ["font", "black"]) or startNumberUtility(c_utility, ["font"])) and (matchUtilitiesOr(m_utility, ["font", "thin"], ["font", "extralight"], ["font", "light"], ["font", "normal"], ["font", "medium"], ["font", "semibold"], ["font", "bold"], ["font", "extrabold"], ["font", "black"]) or startNumberUtility(m_utility, ["font"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["normal", "nums"], ["ordinal"], ["slashed", "zero"], ["lining", "nums"], ["oldstyle", "nums"], ["proportional", "nums"], ["tabular", "nums"], ["diagonal", "fractions"], ["stacked", "fractions"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["normal", "nums"], ["ordinal"], ["slashed", "zero"], ["lining", "nums"], ["oldstyle", "nums"], ["proportional", "nums"], ["tabular", "nums"], ["diagonal", "fractions"], ["stacked", "fractions"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["tracking"]):
						if dblChk(c_utility, m_utility, startUtility, ["tracking"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["line", "clamp"]):
						if dblChk(c_utility, m_utility, startUtility, ["line", "clamp"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["leading"]):
						if dblChk(c_utility, m_utility, startUtility, ["leading"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["list"]):
						if dblChk(c_utility, m_utility, startUtility, ["list"]):
							if startUtility(c_utility, ["list", "image"]) or startUtility(m_utility, ["list", "image"]):
								if dblChk(c_utility, m_utility, startUtility, ["list", "image"]):
									del merged_twobj[c_selector][i]
							elif startUtility(c_utility, ["list", "inside"]) or startUtility(c_utility, ["list", "outside"]) or startUtility(m_utility, ["list", "inside"]) or startUtility(m_utility, ["list", "outside"]):
								if dblChk(c_utility, m_utility, matchUtilitiesOr, ["list", "inside"], ["list", "outside"]):
									del merged_twobj[c_selector][i]
							else:
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["text", "left"], ["text", "center"], ["text", "right"], ["text", "justify"], ["text", "start"], ["text", "end"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["text", "left"], ["text", "center"], ["text", "right"], ["text", "justify"], ["text", "start"], ["text", "end"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["text"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["text"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["underline"], ["overline"], ["line", "through"], ["no", "underline"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["underline"], ["overline"], ["line", "through"], ["no", "underline"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["decoration"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["decoration"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["decoration", "solid"], ["decoration", "double"], ["decoration", "dotted"], ["decoration", "dashed"], ["decoration", "wavy"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["decoration", "solid"], ["decoration", "double"], ["decoration", "dotted"], ["decoration", "dashed"], ["decoration", "wavy"]):
							del merged_twobj[c_selector][i]
					elif (
						matchUtilitiesOr(c_utility, ["decoration", "auto"], ["decoration", "from", "font"], ["decoration", "0"], ["decoration", "1"], ["decoration", "2"], ["decoration", "4"], ["decoration", "8"]) or startSizeUtility(c_utility, ["decoration"])
					) or (
						matchUtilitiesOr(m_utility, ["decoration", "auto"], ["decoration", "from", "font"], ["decoration", "0"], ["decoration", "1"], ["decoration", "2"], ["decoration", "4"], ["decoration", "8"]) or startSizeUtility(m_utility, ["decoration"])
					):
						if (
							matchUtilitiesOr(c_utility, ["decoration", "auto"], ["decoration", "from", "font"], ["decoration", "0"], ["decoration", "1"], ["decoration", "2"], ["decoration", "4"], ["decoration", "8"]) or startSizeUtility(c_utility, ["decoration"])
						) and (
							matchUtilitiesOr(m_utility, ["decoration", "auto"], ["decoration", "from", "font"], ["decoration", "0"], ["decoration", "1"], ["decoration", "2"], ["decoration", "4"], ["decoration", "8"]) or startSizeUtility(m_utility, ["decoration"])
						):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["underline", "offset"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["underline", "offset"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["uppercase"], ["lowercase"], ["capitalize"], ["normal", "case"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["uppercase"], ["lowercase"], ["capitalize"], ["normal", "case"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["text", "ellipsis"], ["text", "clip"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["text", "ellipsis"], ["text", "clip"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["text", "wrap"], ["text", "nowrap"], ["text", "balance"], ["text", "pretty"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["text", "wrap"], ["text", "nowrap"], ["text", "balance"], ["text", "pretty"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["indent"]):
						if dblChk(c_utility, m_utility, startUtility, ["indent"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["align"]):
						if dblChk(c_utility, m_utility, startUtility, ["align"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["whitespace"]):
						if dblChk(c_utility, m_utility, startUtility, ["whitespace"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["break", "normal"], ["break", "words"], ["break", "all"], ["break", "keep"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["break", "normal"], ["break", "words"], ["break", "all"], ["break", "keep"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["hyphens"]):
						if dblChk(c_utility, m_utility, startUtility, ["hyphens"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["content"]):
						if dblChk(c_utility, m_utility, startUtility, ["content"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["bg", "fixed"], ["bg", "local"], ["bg", "scroll"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["bg", "fixed"], ["bg", "local"], ["bg", "scroll"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["bg", "clip"]):
						if dblChk(c_utility, m_utility, startUtility, ["bg", "clip"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["bg"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["bg"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["bg", "origin"]):
						if dblChk(c_utility, m_utility, startUtility, ["bg", "origin"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startPositionUtility, ["bg"]):
						if dblChk(c_utility, m_utility, startPositionUtility, ["bg"]):
							del merged_twobj[c_selector][i]
					elif (startUtility(c_utility, ["bg", "repeat"]) or matchUtility(c_utility, ["bg", "no", "repeat"])) or (startUtility(m_utility, ["bg", "repeat"]) or matchUtility(m_utility, ["bg", "no", "repeat"])):
						if (startUtility(c_utility, ["bg", "repeat"]) or matchUtility(c_utility, ["bg", "no", "repeat"])) and (startUtility(m_utility, ["bg", "repeat"]) or matchUtility(m_utility, ["bg", "no", "repeat"])):
							del merged_twobj[c_selector][i]
					elif (matchUtilitiesOr(c_utility, ["bg", "auto"], ["bg", "cover"], ["bg", "contain"]) or (c_utility[1][:8] == "[length:" if len(c_utility) >= 2 else False)) or (matchUtilitiesOr(m_utility, ["bg", "auto"], ["bg", "cover"], ["bg", "contain"]) or (m_utility[1][:8] == "[length:" if len(m_utility) >= 2 else False)):
						if (matchUtilitiesOr(c_utility, ["bg", "auto"], ["bg", "cover"], ["bg", "contain"]) or (c_utility[1][:8] == "[length:" if len(c_utility) >= 2 else False)) and (matchUtilitiesOr(m_utility, ["bg", "auto"], ["bg", "cover"], ["bg", "contain"]) and (m_utility[1][:8] == "[length:" if len(m_utility) >= 2 else False)):
							del merged_twobj[c_selector][i]
					elif (startUtility(c_utility, ["bg", "gradient"]) or matchUtility(c_utility, ["bg", "none"])) or (c_utility[1][:5] == "[url(" if len(c_utility) >= 2 else False) or (startUtility(m_utility, ["bg", "gradient"]) or matchUtility(m_utility, ["bg", "none"]) or (m_utility[1][:5] == "[url(" if len(m_utility) >= 2 else False)):
						if (startUtility(c_utility, ["bg", "gradient"]) or matchUtility(c_utility, ["bg", "none"])) or (c_utility[1][:5] == "[url(" if len(c_utility) >= 2 else False) and (startUtility(m_utility, ["bg", "gradient"]) or matchUtility(m_utility, ["bg", "none"]) or (m_utility[1][:5] == "[url(" if len(m_utility) >= 2 else False)):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["from"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["from"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startPercentUtility, ["from"]):
						if dblChk(c_utility, m_utility, startPercentUtility, ["from"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["via"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["via"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startPercentUtility, ["via"]):
						if dblChk(c_utility, m_utility, startPercentUtility, ["via"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["to"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["to"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startPercentUtility, ["to"]):
						if dblChk(c_utility, m_utility, startPercentUtility, ["to"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["rounded"]):
						if len(c_utility) >= 2 and len(m_utility) >= 2:
							ls_se = ["ss", "se", "ee", "es"]
							ls_trbl = ["tl", "tr", "bl", "br"]
							if (c_utility[1] in ls_se) != (m_utility[1] in ls_se) or (c_utility[1] in ls_trbl) != (m_utility[1] in ls_trbl):
								pass
							elif c_utility[1] == m_utility[1]:
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["border"]):
						if len(c_utility) >= 2 and len(m_utility) >= 2:
							if c_utility[1] == m_utility[1] and c_utility[1] in ["t", "b", "l", "r", "s", "e"]:
								if orChk(c_utility, m_utility, startColorUtility, c_utility[:2]):
									if dblChk(c_utility, m_utility, startColorUtility, c_utility[:2]):
										del merged_twobj[c_selector][i]
								else:
									del merged_twobj[c_selector][i]
							elif orChk(c_utility, m_utility, matchUtilitiesOr, ["border", "solid"], ["border", "dashed"], ["border", "dotted"], ["border", "double"], ["border", "hidden"], ["border", "none"]):
								if orChk(c_utility, m_utility, matchUtilitiesOr, ["border", "solid"], ["border", "dashed"], ["border", "dotted"], ["border", "double"], ["border", "hidden"], ["border", "none"]):
									del merged_twobj[c_selector][i]
							elif orChk(c_utility, m_utility, matchUtilitiesOr, ["border", "collapse"], ["border", "separate"]):
								if dblChk(c_utility, m_utility, matchUtilitiesOr, ["border", "collapse"], ["border", "separate"]):
									del merged_twobj[c_selector][i]
							elif orChk(c_utility, m_utility, startUtility, ["border", "spacing", "x"]):
								if dblChk(c_utility, m_utility, startUtility, ["border", "spacing", "x"]):
									del merged_twobj[c_selector][i]
							elif orChk(c_utility, m_utility, startUtility, ["border", "spacing", "y"]):
								if dblChk(c_utility, m_utility, startUtility, ["border", "spacing", "y"]):
									del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["divide", "x"]):
						if not orChk(c_utility, m_utility, startUtility, ["divide", "x", "reverse"]):
							if dblChk(c_utility, m_utility, startUtility, ["divide", "x"]):
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["divide", "y"]):
						if not orChk(c_utility, m_utility, startUtility, ["divide", "y", "reverse"]):
							if dblChk(c_utility, m_utility, startUtility, ["divide", "y"]):
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["divide"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["divide"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["divide", "solid"], ["divide", "dashed"], ["divide", "dotted"], ["divide", "double"], ["divide", "none"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["divide", "solid"], ["divide", "dashed"], ["divide", "dotted"], ["divide", "double"], ["divide", "none"]):
							del merged_twobj[c_selector][i]
					elif (matchUtilitiesOr(c_utility, ["outline", "0"], ["outline", "1"], ["outline", "2"], ["outline", "4"], ["outline", "8"]) or startSizeUtility(c_utility, ["outline"])) or (matchUtilitiesOr(m_utility, ["outline", "0"], ["outline", "1"], ["outline", "2"], ["outline", "4"], ["outline", "8"]) or startSizeUtility(m_utility, ["outline"])):
						if (matchUtilitiesOr(c_utility, ["outline", "0"], ["outline", "1"], ["outline", "2"], ["outline", "4"], ["outline", "8"]) or startSizeUtility(c_utility, ["outline"])) and (matchUtilitiesOr(m_utility, ["outline", "0"], ["outline", "1"], ["outline", "2"], ["outline", "4"], ["outline", "8"]) or startSizeUtility(m_utility, ["outline"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["outline"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["outline"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["outline", "none"], ["outline"], ["outline", "dashed"], ["outline", "dotted"], ["outline", "double"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["outline", "none"], ["outline"], ["outline", "dashed"], ["outline", "dotted"], ["outline", "double"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["outline", "offset"]):
						if dblChk(c_utility, m_utility, startUtility, ["outline", "offset"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["ring"]):
						if orChk(c_utility, m_utility, startUtility, ["ring", "offset"]):
							defined_width = [["ring", "offset", "0"], ["ring", "offset", "1"], ["ring", "offset", "2"], ["ring", "offset", "4"], ["ring", "offset", "8"]]
							if orChk(c_utility, m_utility, matchUtilitiesOr, *defined_width) or orChk(c_utility, m_utility, startSizeUtility, ["ring", "offset"]):
								if (matchUtilitiesOr(c_utility, *defined_width) or startSizeUtility(c_utility, ["ring", "offset"])) and (matchUtilitiesOr(m_utility, *defined_width) or startSizeUtility(m_utility, ["ring", "offset"])):
									del merged_twobj[c_selector][i]
							elif orChk(c_utility, m_utility, startColorUtility, ["ring", "offset"]):
								if dblChk(c_utility, m_utility, startColorUtility, ["ring", "offset"]):
									del merged_twobj[c_selector][i]
						elif orChk(c_utility, m_utility, matchUtilitiesOr, ["ring", "0"], ["ring", "1"], ["ring", "2"], ["ring"], ["ring", "4"], ["ring", "8"]) or orChk(c_utility, m_utility, startSizeUtility, ["ring"]):
							if (matchUtilitiesOr(c_utility, ["ring", "0"], ["ring", "1"], ["ring", "2"], ["ring"], ["ring", "4"], ["ring", "8"]) or startSizeUtility(c_utility, ["ring"])) and (matchUtilitiesOr(m_utility, ["ring", "0"], ["ring", "1"], ["ring", "2"], ["ring"], ["ring", "4"], ["ring", "8"]) or startSizeUtility(m_utility, ["ring"])):
								del merged_twobj[c_selector][i]
						elif orChk(c_utility, m_utility, startColorUtility, ["ring"]):
							if dblChk(c_utility, m_utility, startColorUtility, ["ring"]):
								del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startSizeUtility, ["shadow"]) or orChk(c_utility, m_utility, matchUtilitiesOr, ["shadow"], ["shadow", "inner"], ["shadow", "none"]):
						if (startSizeUtility(c_utility, ["shadow"]) or matchUtilitiesOr(c_utility, ["shadow"], ["shadow", "inner"], ["shadow", "none"])) and (startSizeUtility(m_utility, ["shadow"]) or matchUtilitiesOr(m_utility, ["shadow"], ["shadow", "inner"], ["shadow", "none"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["shadow"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["shadow"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["opacity"]):
						if dblChk(c_utility, m_utility, startUtility, ["opacity"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["mix", "blend"]):
						if dblChk(c_utility, m_utility, startUtility, ["mix", "blend"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["bg", "blend"]):
						if dblChk(c_utility, m_utility, startUtility, ["bg", "blend"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["blur"]):
						if dblChk(c_utility, m_utility, startUtility, ["blur"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["brightness"]):
						if dblChk(c_utility, m_utility, startUtility, ["brightness"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["contrast"]):
						if dblChk(c_utility, m_utility, startUtility, ["contrast"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["drop", "shadow"]):
						if dblChk(c_utility, m_utility, startUtility, ["drop", "shadow"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["grayscale"]):
						if dblChk(c_utility, m_utility, startUtility, ["grayscale"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["hue", "rotate"]):
						if dblChk(c_utility, m_utility, startUtility, ["hue", "rotate"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["invert"]):
						if dblChk(c_utility, m_utility, startUtility, ["invert"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["saturate"]):
						if dblChk(c_utility, m_utility, startUtility, ["saturate"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["sepia"]):
						if dblChk(c_utility, m_utility, startUtility, ["sepia"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "blur"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "blur"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "brightness"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "brightness"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "contrast"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "contrast"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "grayscale"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "grayscale"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "hue", "rotate"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "hue", "rotate"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "invert"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "invert"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "opacity"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "opacity"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "saturate"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "saturate"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["backdrop", "sepia"]):
						if dblChk(c_utility, m_utility, startUtility, ["backdrop", "sepia"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["table", "auto"], ["table", "fixed"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["table", "auto"], ["table", "fixed"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["caption", "top"], ["caption", "top"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["caption", "bottom"], ["caption", "bottom"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["transition"]):
						if dblChk(c_utility, m_utility, startUtility, ["transition"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["duration"]):
						if dblChk(c_utility, m_utility, startUtility, ["duration"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["ease"]):
						if dblChk(c_utility, m_utility, startUtility, ["ease"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["delay"]):
						if dblChk(c_utility, m_utility, startUtility, ["delay"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["animate"]):
						if dblChk(c_utility, m_utility, startUtility, ["animate"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scale"]):
						if dblChk(c_utility, m_utility, startUtility, ["scale"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["rotate"]):
						if dblChk(c_utility, m_utility, startUtility, ["rotate"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["translate", "x"]):
						if dblChk(c_utility, m_utility, startUtility, ["translate", "x"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["translate", "y"]):
						if dblChk(c_utility, m_utility, startUtility, ["translate", "y"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["skew", "x"]):
						if dblChk(c_utility, m_utility, startUtility, ["skew", "x"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["skew", "y"]):
						if dblChk(c_utility, m_utility, startUtility, ["skew", "y"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["origin"]):
						if dblChk(c_utility, m_utility, startUtility, ["origin"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["accent"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["accent"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["appearance"]):
						if dblChk(c_utility, m_utility, startUtility, ["appearance"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["cursor"]):
						if dblChk(c_utility, m_utility, startUtility, ["cursor"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startColorUtility, ["caret"]):
						if dblChk(c_utility, m_utility, startColorUtility, ["caret"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["pointer", "events"]):
						if dblChk(c_utility, m_utility, startUtility, ["pointer", "events"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["resize"]):
						if dblChk(c_utility, m_utility, startUtility, ["resize"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["scroll", "auto"], ["scroll", "smooth"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["scroll", "auto"], ["scroll", "smooth"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "ms"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "ms"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "me"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "me"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "mt"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "mt"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "mr"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "mr"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "mb"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "mb"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "ml"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "ml"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "ps"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "ps"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "pe"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "pe"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "pt"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "pt"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "pr"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "pr"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "pb"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "pb"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["scroll", "pl"]):
						if dblChk(c_utility, m_utility, startUtility, ["scroll", "pl"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "start"], ["snap", "end"], ["snap", "center"], ["snap", "align", "none"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "start"], ["snap", "end"], ["snap", "center"], ["snap", "align", "none"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "normal"], ["snap", "always"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "normal"], ["snap", "always"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "none"], ["snap", "x"], ["snap", "y"], ["snap", "both"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "none"], ["snap", "x"], ["snap", "y"], ["snap", "both"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "mandatory"], ["snap", "proximity"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["snap", "mandatory"], ["snap", "proximity"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["touch"]):
						if dblChk(c_utility, m_utility, startUtility, ["touch"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["select"]):
						if dblChk(c_utility, m_utility, startUtility, ["select"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["will", "change"]):
						if dblChk(c_utility, m_utility, startUtility, ["will", "change"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["fill"]):
						if dblChk(c_utility, m_utility, startUtility, ["fill"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtility, ["stroke", "none"]) or orChk(c_utility, m_utility, startColorUtility, ["stroke"]):
						if (matchUtility(c_utility, ["stroke", "none"]) or startColorUtility(c_utility, ["stroke"])) and (matchUtility(m_utility, ["stroke", "none"]) or startColorUtility(m_utility, ["stroke"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["stroke", "0"], ["stroke", "1"], ["stroke", "2"]) or orChk(c_utility, m_utility, startSizeUtility, ["stroke"]):
						if (matchUtilitiesOr(c_utility, ["stroke", "0"], ["stroke", "1"], ["stroke", "2"]) or startSizeUtility(c_utility, ["stroke"])) and (matchUtilitiesOr(m_utility, ["stroke", "0"], ["stroke", "1"], ["stroke", "2"]) or startSizeUtility(m_utility, ["stroke"])):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, matchUtilitiesOr, ["sr", "only"], ["not", "sr", "only"]):
						if dblChk(c_utility, m_utility, matchUtilitiesOr, ["sr", "only"], ["not", "sr", "only"]):
							del merged_twobj[c_selector][i]
					elif orChk(c_utility, m_utility, startUtility, ["forced", "color", "adjust"]):
						if dblChk(c_utility, m_utility, startUtility, ["forced", "color", "adjust"]):
							del merged_twobj[c_selector][i]

				merged_twobj[c_selector].append(c)
			else:
				merged_twobj[c_selector] = [c]
	
	twmerged: list[str] = []
	for selector in sorted(merged_twobj):
		twobj_ls = mergeTwObj(merged_twobj[selector])
		for m in twobj_ls:
			twmerged.append(m[0] + "-".join(m[1]))
	
	return " ".join(twmerged)
