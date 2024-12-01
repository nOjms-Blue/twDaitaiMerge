from typing import TypeAlias

# (selector, utility)
TailwindObject: TypeAlias = tuple[str, list[str]]

# m-2 -> mt-2, mb-2, ml-2, mr-2 のように分解
def parseTwObj(twobj: TailwindObject) -> list[TailwindObject]:
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

# mt-2, mb-2, ml-2, mr-2 -> m-2 のように結合
def mergeTwObj(twobj_list: list[TailwindObject]) -> list[TailwindObject]:
	def searchProp(prop: list[str], is_minus: bool, search_list: list[TailwindObject], starts_props: list[str]):
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
	
	search: list[TailwindObject] = []
	merged: list[TailwindObject] = []
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

# TailwindObjectに変換
def toTwObj(className: str):
	# className -> selector, utility
	bracket: bool = False
	start: int = 0
	for i in range(0, len(className), 1):
		c = className[i]
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
	separated: tuple[str, str] = ("", className)
	if start < len(className):
		separated = (className[:start], className[start:])
	selector, utility = separated
	
	# ハイフンで分割
	prop_split: list[str] = []
	bracket: bool = False
	start: int = 0
	for i in range(0, len(utility), 1):
		c = utility[i]
		if i == start:
			if c == "[":
				bracket = True
				continue
		if bracket:
			if c == "]":
				bracket = False
		else:
			if c == "-":
				prop_split.append(utility[start:i])
				start = i + 1
	if start < len(utility):
		prop_split.append(utility[start:])
	
	return parseTwObj((selector, prop_split))
