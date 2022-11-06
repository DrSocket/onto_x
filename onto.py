import csv
import sys

label_not_found = 1
id_not_found = 2
error_args = 3

def error(code):
	if code == id_not_found:
		print("The id you entered was not found.")
	if code == label_not_found:
		print("The label you entered was not found.")
	if code == error_args:
		print ("The program takes 2 arguments, `ID` or `LABEL` and the search parameter.")
	sys.exit(1)

class Data:

	labelToId = dict()

	idToLabel = dict()

	idToParents = dict()

	parentToIds = dict()

	def addParents(self, classId, parents):
		if len(parents) == 0:
			self.idToParents[classId] = None
			return 0
		arr = parents.split('|')
		self.idToParents[classId] = arr
		return arr

	def addId(self, parent, classId):
		if parent not in self.parentToIds:
			self.parentToIds[parent] = [classId]
		else:
			self.parentToIds[parent] += [classId]

	def mapIdAndLabel(self, classId, label):
		if label not in self.labelToId:
			self.labelToId[label] = classId
		if classId not in self.idToLabel:
			self.idToLabel[classId] = label

	def mapIdsAndParents(self, classId, parents):
		if classId not in self.idToParents:
			par = self.addParents(classId, parents)
			if par != 0:
				self.mapParentToIds(par, classId)

	def mapParentToIds(self, parents, classId):
		for parent in parents:
			self.addId(parent, classId)



def relateId(classId, level):
	seen.append(classId)
	if classId not in data.idToLabel:
		return
	parents = data.idToParents[classId]
	level += 1
	if parents != None:
		for parent in parents:
			if parent in seen:
				continue
			else:
				relateId(parent, level)
	if level == 0 and parents != None:
		for parent in parents:
			for sibling in data.parentToIds[parent]:
				if (sibling != classId) and data.idToLabel[sibling] not in result:
					result[data.idToLabel[sibling]] = 0 
	else:
		result[data.idToLabel[classId]] = level

def fill_data():
	with open("./onto_x.csv", 'r') as file:
		csvreader = csv.reader(file)
		header = next(csvreader)
		for row in csvreader:
			data.mapIdAndLabel(row[0], row[1])
			data.mapIdsAndParents(row[0], row[2])

if __name__ == "__main__":
	data = Data()
	result = dict()
	seen = list()

	fill_data()
	av = sys.argv
	if len(av) != 3:
		error(error_args)
	if av[1] == 'ID':
		if av[2] not in data.idToLabel:
			error(id_not_found)
		relateId(av[2], -1)
	elif av[1] == 'LABEL':
		if av[2] not in data.labelToId:
			error(label_not_found)
		relateId(data.labelToId[av[2]], -1)

	sorted_dict = dict()
	sorted_keys = sorted(result, key=result.get, reverse=True)
	for x in sorted_keys:
		sorted_dict[x] = result[x]

	print (sorted_dict)