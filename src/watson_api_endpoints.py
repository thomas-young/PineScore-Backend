import json
import os
from ibm_watson import ToneAnalyzerV3
from gensim.summarization.summarizer import summarize

WORD_COUNT = 75

json_filename = os.path.join( os.getcwd(), 'data.json' )

tone_analyzer = ToneAnalyzerV3(
    version='2019-05-27',
    iam_apikey='0w77Ioz4bZbFy0i9ydKC-5PYhTyIKRU9pulzn2wYcJKT',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

def get_json(professor_name, json):
	text = str(' '.join(json))
	result_dict = {}
	name_split = professor_name.split(',')

	result_dict['id'] = name_split[1] + " " + name_split[0] 
	result_dict['summary'] = summarize(text, word_count=WORD_COUNT)

	tone_analysis = tone_analyzer.tone(
	    {'text': text},
	    content_type='application/json',
	).get_result()	

	tone_dict = dict()
	for a in tone_analysis['sentences_tone']:
			for t in a['tones']:
				if t['tone_id'] in tone_dict:
					tone_dict[t['tone_id']].append(t['score'])
				else:
					tone_dict[t['tone_id']] = [t['score']]
	
	for k, v in tone_dict.items():
		n = len(v)
		avg = sum(v) / n
		tone_dict[k] = [int(avg * 100), n]
	
	result_dict['pinescore'] = tone_dict['joy']
	controversy_score = 0
	controversy_n = 0
	tone_count = 0

	for tone in ['sadness', 'anger', 'fear']:
		if tone in tone_dict:
			controversy_score += tone_dict[tone][0]
			controversy_n += tone_dict[tone][1]
			tone_count += 1
	if tone_count > 0:		
		result_dict['controversy_score'] = int(controversy_score / tone_count)
	else:
		result_dict['controversy_score'] = 0
	result_dict['controversy_n'] = controversy_n

	return result_dict

with open(json_filename) as f:
	d = json.load(f)
print(d)
total = {}

for prof in d.keys():
	print(prof)
	if d[prof]:	
		try:
			myjson = get_json(prof, d[prof])
			name_split = prof.split(',')

			realname = name_split[1] + " " + name_split[0] 			
			total[realname] = myjson
		except:
			print(f"error with: {prof}")

# booker = get_json('Booker,Vaughn', d)
# phillips = get_json('Phillips,Anne', d)

# total = {'Vaughn Booker': booker, 'Anne Phillips': phillips}
# print(json.dumps(total, indent=4))

with open('output.json', 'w') as outfile:
    json.dump(total, outfile)
