import json, csv, re, string, sys

def read_json(json_fp):
	'''Reads a json and returns the enclosed data.'''
	with open(json_fp, 'r') as json_file:
		data = json.load(json_file)
		return data

def split_into_paragraphs(data):
	'''Splits text into paragraphs'''
	paragraphs = data.split('\n')
	return paragraphs

def add_paragraph(dictionary, key, date, value):
	if key in dictionary:
		if date in dictionary[key]:
			dictionary[key][date].append(value)
		else:
			dictionary[key][date] = [value]
	else:
		dictionary[key] = {date:[value]}

def get_info(dictionary, entry):
	dictionary[entry['Name']] = [entry['id'],entry['leadership_title'],entry['party'],entry['bioguideid'],entry['birthday'],entry['gender'],entry['osid'],entry['pvsid'],entry['role_type'],entry['senator_class'],entry['senator_rank'],entry['startdate'],entry['state'],entry['district']]

def search(data, term_list):
	'''Creates a dictionary with senders as keys and lists of paragraphs as values'''
	paragraphs_dict = {}
	info_dict = {}
	for term in term_list:
		for entry in data:
			if entry['Name'] not in info_dict:
				get_info(info_dict, entry)
			paragraphs = split_into_paragraphs(entry['Body'])
			for paragraph in paragraphs:
				if term.lower() in paragraph.lower():
					add_paragraph(paragraphs_dict, entry['Name'], entry['Date'], paragraph.replace('\r',''))
	return (paragraphs_dict, info_dict)

def form_lists(dictionary, info_dict):
	'''Forms the lists that will be written as a csv'''
	return_list = [['Name','ID','Leadership Title','Party','Bioguide ID','Birthday','Gender','OSID','PVSID','Role Type','Senator Class','Senator Rank','Start Date','State','District','Date','Reference(s)']]
	for key in dictionary:
		for date in dictionary[key]:
			append_list = []
			append_list.append(key)
			for entry in info_dict[key]:
				append_list.append(entry)
			append_list.append(date)
			for paragraph in dictionary[key][date]:
				append_list.append(paragraph)
			return_list.append(append_list)
	return return_list

def write_csv(data, csv_fp):
	'''Writes a list of lists to a csv file with each list as a row.'''
	with open(csv_fp, 'w') as out:
		csv_out = csv.writer(out, lineterminator = '\n')
		for row in data:
			csv_out.writerow(row)


json_data = read_json('term_references_dataset.json')
num_terms = int(raw_input('Please enter the number of terms to search for: '))
term_list = []
output_title = ''
for i in range(0,num_terms):
	term = raw_input('Please enter a search term: ')
	output_title += term.lower() + '_'
	term_list.append(term)
paragraph_dict,info_dict = search(json_data,term_list)
lists = form_lists(paragraph_dict,info_dict)
output_title += 'references.csv'
write_csv(lists, output_title)
