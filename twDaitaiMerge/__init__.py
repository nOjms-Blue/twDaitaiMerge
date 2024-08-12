# encoding : utf-8

def twMerge(*className):
	def parseTwObj(twobj) -> list:
		selector, props = twobj

		is_minus = False
		if len(props) > 0:
			if props[0] == "":
				props = props[1:]
				is_minus = True

		minus = ([""] if is_minus else [])

		if len(props) > 0:
			if props[0] == "inset" and len(props) >= 2:
				if props[1] == "x":
					return [
						(selector, minus + ["left", *props[2:]]),
						(selector, minus + ["right", *props[2:]]),
					]
				elif props[1] == "y":
					return [
						(selector, minus + ["top", *props[2:]]),
						(selector, minus + ["bottom", *props[2:]]),
					]
				else:
					return [
						(selector, minus + ["left", *props[1:]]),
						(selector, minus + ["right", *props[1:]]),
						(selector, minus + ["top", *props[1:]]),
						(selector, minus + ["bottom", *props[1:]]),
					]
			elif props[0] == "p" and len(props) >= 2:
				return [
					(selector, minus + ["pt", *props[1:]]),
					(selector, minus + ["pr", *props[1:]]),
					(selector, minus + ["pb", *props[1:]]),
					(selector, minus + ["pl", *props[1:]]),
				]
			elif props[0] == "px" and len(props) >= 2:
				return [
					(selector, minus + ["pr", *props[1:]]),
					(selector, minus + ["pl", *props[1:]]),
				]
			elif props[0] == "py" and len(props) >= 2:
				return [
					(selector, minus + ["pt", *props[1:]]),
					(selector, minus + ["pb", *props[1:]]),
				]
			elif props[0] == "m" and len(props) >= 2:
				return [
					(selector, minus + ["mt", *props[1:]]),
					(selector, minus + ["mr", *props[1:]]),
					(selector, minus + ["mb", *props[1:]]),
					(selector, minus + ["ml", *props[1:]]),
				]
			elif props[0] == "mx" and len(props) >= 2:
				return [
					(selector, minus + ["mr", *props[1:]]),
					(selector, minus + ["ml", *props[1:]]),
				]
			elif props[0] == "my" and len(props) >= 2:
				return [
					(selector, minus + ["mt", *props[1:]]),
					(selector, minus + ["mb", *props[1:]]),
				]
			elif props[0] == "size" and len(props) >= 2:
				return [
					(selector, minus + ["w", *props[1:]]),
					(selector, minus + ["h", *props[1:]]),
				]
			elif props[0] == "rounded":
				size = []
				pos = []
				if len(props) >= 3:
					if props[1] in ["s", "ss", "se", "e", "ee", "es", "t", "b", "l", "r", "tl", "tr", "bl", "br"]:
						if props[1] == "s":
							pos = ["ss", "se"]
						elif props[1] == "e":
							pos = ["ee", "es"]
						elif props[1] == "t":
							pos = ["tl", "tr"]
						elif props[1] == "b":
							pos = ["bl", "br"]
						elif props[1] == "l":
							pos = ["tl", "bl"]
						elif props[1] == "r":
							pos = ["tr", "br"]
						else:
							pos = [props[1]]
						size = props[2:]
				else:
					pos = ["tl", "tr", "bl", "br"]
					size = props[1:]
				ls = []
				for p in pos:
					ls.append((selector, minus + ["rounded", p] + size))
				return ls
			elif props[0] == "border":
				if props == ["border"] or props[:2] == ["border", "x"] or props[:2] == ["border", "y"] or props[:2] == ["border", "s"] or props[:2] == ["border", "e"] or props[:2] == ["border", "t"] or props[:2] == ["border", "r"] or props[:2] == ["border", "b"] or props[:2] == ["border", "l"]:
					values = []
					pos = []
					if len(props) >= 3:
						if props[1] in ["x", "y", "s", "e", "t", "b", "l", "r"]:
							if props[1] == "x":
								pos = ["l", "r"]
							elif props[1] == "y":
								pos = ["t", "b"]
							else:
								pos = [props[1]]
							values = props[2:]
					else:
						pos = ["t", "b", "l", "r"]
						values = props[1:]
					ls = []
					for p in pos:
						ls.append((selector, minus + ["border", p] + values))
					return ls
				elif props[:2] == ["border", "spacing"]:
					if len(props) >= 3:
						if props[2] != "x" and props[2] != "y":
							return [
								(selector, minus + ["border", "spacing", "x", *props[2:]]),
								(selector, minus + ["border", "spacing", "y", *props[2:]]),
							]
			elif props[0] == "scroll":
				if len(props) >= 2:
					if props[1] in ["m", "mx", "my", "ms", "me", "mt", "mr", "mb", "ml"]:
						if props[1] == "m":
							return [
								(selector, minus + ["scroll", "mt", *props[2:]]),
								(selector, minus + ["scroll", "mr", *props[2:]]),
								(selector, minus + ["scroll", "mb", *props[2:]]),
								(selector, minus + ["scroll", "ml", *props[2:]]),
							]
						elif props[1] == "mx":
							return [
								(selector, minus + ["scroll", "mr", *props[2:]]),
								(selector, minus + ["scroll", "ml", *props[2:]]),
							]
						elif props[1] == "my":
							return [
								(selector, minus + ["scroll", "mt", *props[2:]]),
								(selector, minus + ["scroll", "mb", *props[2:]]),
							]
					elif props[1] in ["p", "px", "py", "ps", "pe", "pt", "pr", "pb", "pl"]:
						if props[1] == "p":
							return [
								(selector, minus + ["scroll", "pt", *props[2:]]),
								(selector, minus + ["scroll", "pr", *props[2:]]),
								(selector, minus + ["scroll", "pb", *props[2:]]),
								(selector, minus + ["scroll", "pl", *props[2:]]),
							]
						elif props[1] == "px":
							return [
								(selector, minus + ["scroll", "pr", *props[2:]]),
								(selector, minus + ["scroll", "pl", *props[2:]]),
							]
						elif props[1] == "py":
							return [
								(selector, minus + ["scroll", "pt", *props[2:]]),
								(selector, minus + ["scroll", "pb", *props[2:]]),
							]

		return [twobj]
	
	def mergeTwObj(twobj_list: list[tuple]) -> list:
		def searchProp(prop, is_minus, search_list, starts_props):
			def startProp(target, start_prop):
				if len(target) < len(start_prop):
					return False

				for i in range(0, len(start_prop), 1):
					if target[i] != start_prop[i]:
						return False
				
				return True
			
			def searchOne(prop, search_props, start_prop):
				if not startProp(search_props, start_prop):
					return False
				
				return bool(prop[len(start_prop):] == search_props[len(start_prop):])
			
			same_value_props_index = []
			is_exist = {}
			for one_props in starts_props:
				is_exist[one_props] = False
				one_prop = one_props.split("-")
				if len(prop) >= len(one_prop):
					matched = True
					for i in range(0, len(one_prop), 1):
						if prop[i] != one_prop[i]:
							matched = False
							break
					
					if matched:
						is_exist[one_props] = True
			
			for i in range(0, len(search_list), 1):
				s_prop = search_list[i][1]
				if len(s_prop) >= 1:
					if is_minus != bool(s_prop[0] == ""):
						continue
					if s_prop[0] == "":
						s_prop = s_prop[1:]
				
				for start_props in starts_props:
					start_prop = start_props.split("-")
					if searchOne(prop, s_prop, start_prop):
						same_value_props_index.append(i)
						is_exist[start_props] = True
			
			return same_value_props_index, is_exist
		
		search = []
		merged = []
		for twobj in twobj_list:
			search.append(twobj)
		
		while(len(search) > 0):
			twobj = search.pop()
			selector, props = twobj

			is_minus = False
			if len(props) >= 1:
				if props[0] == "":
					is_minus = True
					props = props[1:]

			if len(props) >= 1:
				if props[0] in ["left", "right", "top", "bottom"]:
					same_value_props_index, is_exist = searchProp(props, is_minus, search, ["left", "right", "top", "bottom"])
					
					# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
					if is_exist["bottom"] and is_exist["left"] and is_exist["right"] and is_exist["top"]:
						for i in reversed(same_value_props_index):
							del search[i]
						merged.append((selector, ["inset", *props[1:]]))
						continue
					elif props[0] in ["left", "right"]:
						if is_exist["left"] or is_exist["right"]:
							for i in reversed(same_value_props_index):
								if search[i][1][0] in ["left", "right"]:
									del search[i]
							merged.append((selector, ["inset", "x", *props[1:]]))
							continue
					elif props[0] in ["top", "bottom"]:
						if is_exist["top"] or is_exist["bottom"]:
							for i in reversed(same_value_props_index):
								if search[i][1][0] in ["top", "bottom"]:
									del search[i]
							merged.append((selector, ["inset", "y", *props[1:]]))
							continue
				elif props[0] in ["pt", "pr", "pb", "pl"]:
					same_value_props_index, is_exist = searchProp(props, is_minus, search, ["pt", "pr", "pb", "pl"])
					
					# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
					if is_exist["pt"] and is_exist["pr"] and is_exist["pb"] and is_exist["pl"]:
						for i in reversed(same_value_props_index):
							del search[i]
						merged.append((selector, ["p", *props[1:]]))
						continue
					elif props[0] in ["pl", "pr"]:
						if is_exist["pl"] and is_exist["pr"]:
							for i in reversed(same_value_props_index):
								if search[i][1][0] in ["pl", "pr"]:
									del search[i]
							merged.append((selector, ["px", *props[1:]]))
							continue
					elif props[0] in ["pt", "pb"]:
						if is_exist["pt"] and is_exist["pb"]:
							for i in reversed(same_value_props_index):
								if search[i][1][0] in ["pt", "pb"]:
									del search[i]
							merged.append((selector, ["py", *props[1:]]))
							continue
				elif props[0] in ["mt", "mr", "mb", "ml"]:
					same_value_props_index, is_exist = searchProp(props, is_minus, search, ["mt", "mr", "mb", "ml"])

					# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
					if is_exist["mt"] and is_exist["mr"] and is_exist["mb"] and is_exist["ml"]:
						for i in reversed(same_value_props_index):
							del search[i]
						merged.append((selector, ["m", *props[1:]]))
						continue
					elif props[0] in ["ml", "mr"]:
						if is_exist["ml"] and is_exist["mr"]:
							for i in reversed(same_value_props_index):
								if search[i][1][0] in ["ml", "mr"]:
									del search[i]
							merged.append((selector, ["mx", *props[1:]]))
							continue
					elif props[0] in ["mt", "mb"]:
						if is_exist["mt"] and is_exist["mb"]:
							for i in reversed(same_value_props_index):
								if search[i][1][0] in ["mt", "mb"]:
									del search[i]
							merged.append((selector, ["my", *props[1:]]))
							continue
				elif props[0] in ["w", "h"]:
					same_value_props_index, is_exist = searchProp(props, is_minus, search, ["w", "h"])
					
					# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
					if is_exist["w"] and is_exist["h"]:
						for i in reversed(same_value_props_index):
							del search[i]
						merged.append((selector, ["size", *props[1:]]))
						continue
				elif props[0] == "rounded":
					if len(props) >= 2:
						if props[1] in ["ss", "se"]:
							same_value_props_index, is_exist = searchProp(props, is_minus, search, ["rounded-ss", "rounded-se"])
							
							# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
							if is_exist["rounded-ss"] and is_exist["rounded-se"]:
								for i in reversed(same_value_props_index):
									del search[i]
								merged.append((selector, ["rounded", "s", *props[2:]]))
								continue
						elif props[1] in ["es", "ee"]:
							same_value_props_index, is_exist = searchProp(props, is_minus, search, ["rounded-es", "rounded-ee"])
							
							# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
							if is_exist["rounded-es"] and is_exist["rounded-ee"]:
								for i in reversed(same_value_props_index):
									del search[i]
								merged.append((selector, ["rounded", "e", *props[2:]]))
								continue
						elif props[1] in ["tl", "tr", "bl", "br"]:
							same_value_props_index, is_exist = searchProp(props, is_minus, search, ["rounded-tl", "rounded-tr", "rounded-bl", "rounded-br"])
							
							# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
							if is_exist["rounded-tl"] and is_exist["rounded-tr"] and is_exist["rounded-bl"] and is_exist["rounded-br"]:
								for i in reversed(same_value_props_index):
									del search[i]
								merged.append((selector, ["rounded", *props[2:]]))
								continue
							elif props[1] in ["tl", "tr"] and is_exist["rounded-tl"] and is_exist["rounded-tr"]:
								for i in reversed(same_value_props_index):
									if search[i][1][1] in ["tl", "tr"]:
										del search[i]
								merged.append((selector, ["rounded", "t", *props[2:]]))
								continue
							elif props[1] in ["tr", "br"] and is_exist["rounded-tr"] and is_exist["rounded-br"]:
								for i in reversed(same_value_props_index):
									if search[i][1][1] in ["tr", "br"]:
										del search[i]
								merged.append((selector, ["rounded", "r", *props[2:]]))
								continue
							elif props[1] in ["bl", "br"] and is_exist["rounded-bl"] and is_exist["rounded-br"]:
								for i in reversed(same_value_props_index):
									if search[i][1][1] in ["bl", "br"]:
										del search[i]
								merged.append((selector, ["rounded", "b", *props[2:]]))
								continue
							elif props[1] in ["tl", "bl"] and is_exist["rounded-tl"] and is_exist["rounded-bl"]:
								for i in reversed(same_value_props_index):
									if search[i][1][1] in ["tl", "bl"]:
										del search[i]
								merged.append((selector, ["rounded", "l", *props[2:]]))
								continue
				elif props[0] == "border":
					if len(props) >= 2:
						if props[1] in ["t", "r", "b", "l"]:
							same_value_props_index, is_exist = searchProp(props, is_minus, search, ["border-t", "border-r", "border-b", "border-l"])
							
							# 結合可能であれば対象は削除し、結合結果を追加して次の値へ
							if is_exist["border-t"] and is_exist["border-r"] and is_exist["border-b"] and is_exist["border-l"]:
								for i in reversed(same_value_props_index):
									del search[i]
								merged.append((selector, ["border", *props[2:]]))
								continue
							elif props[1] in ["t", "b"]:
								if is_exist["border-t"] and is_exist["border-b"]:
									for i in reversed(same_value_props_index):
										if search[i][1][1] in ["t", "b"]:
											del search[i]
									merged.append((selector, ["border", "y", *props[2:]]))
									continue
							elif props[1] in ["r", "l"]:
								if is_exist["border-r"] and is_exist["border-l"]:
									for i in reversed(same_value_props_index):
										if search[i][1][1] in ["r", "l"]:
											del search[i]
									merged.append((selector, ["border", "x", *props[2:]]))
									continue

			merged.append(twobj)
		return merged

	def toTwObj(className):
		split = className
		bracket = False
		start = 0
		for i in range(0, len(split), 1):
			c = split[i]
			if i == start:
				if c == "[":
					bracket = True
			if bracket:
				if c == "]":
					bracket = False
			else:
				if c == ":":
					start = i + 1
				elif c == "-":
					break
		separated = ("", split)
		if start < len(split):
			separated = (split[:start], split[start:])
		
		prop_split = []
		bracket = False
		start = 0
		for i in range(0, len(separated[1]), 1):
			c = separated[1][i]
			if i == start:
				if c == "[":
					bracket = True
					continue
			if bracket:
				if c == "]":
					bracket = False
			else:
				if c == "-":
					prop_split.append(separated[1][start:i])
					start = i + 1
		if start < len(separated[1]):
			prop_split.append(separated[1][start:])
		
		return parseTwObj((separated[0], prop_split))

	# ユーティリティ部が特定の値から始まっているか
	def startUtility(target, start):
		if len(target) >= len(start):
			for i in range(0, len(start), 1):
				if target[i] != start[i]:
					return False
			return True

		return False

	# ユーティリティ部が一致しているか
	def matchUtility(target, comparison):
		if len(target) == len(comparison):
			for i in range(0, len(target), 1):
				if target[i] != comparison[i]:
					return False
			return True
		return False

	# ユーティリティ部がいずれかと一致しているか
	def matchUtilitiesOr(target, *comparison_utils):
		for comparison in comparison_utils:
			if matchUtility(target, comparison):
				return True
		return False

	# ユーティリティ部が特定の値+サイズから始まるか
	def startSizeUtility(target, start):
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
	def startColorUtility(target, start):
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
	def startNumberUtility(target, start):
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
	def startPositionUtility(target, start):
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
	def startPercentUtility(target, start):
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
	def dblChk(target1, target2, function, *args):
		return function(target1, *args) and function(target2, *args)

	# いずれかのユーティリティの比較関数の結果がTrueになるか
	def orChk(target1, target2, function, *args):
		return function(target1, *args) or function(target2, *args)

	merged_twobj = {}
	for class_name in className:
		splited = str(class_name).split(" ")
		class_names = []
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
	
	twmerged = []
	for selector in sorted(merged_twobj):
		twobj_ls = mergeTwObj(merged_twobj[selector])
		for m in twobj_ls:
			twmerged.append(m[0] + "-".join(m[1]))

	return " ".join(twmerged)
