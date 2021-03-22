
import pandas as pd

def main(input_txt):
	answer = []
	question = []
	df = pd.DataFrame(columns=['Question','Answer'])

	split_txt = input_txt.split('\n')
	
	# filter question that end with '?'
	for ques in split_txt:
	    if ques.endswith('?'):
	        question.append(ques)

	# split text on basis of 'Answer'
	ans_txt = input_txt.split('Answer:')[1:]

	# filter answer
	for no, ans in enumerate(ans_txt):
	    answer.append(ans.split(str(no+2)+'.')[0])

	# create a dataframe
	for no,i in enumerate(zip(question,answer)):
	    df.loc[no, ['Question','Answer']] = [i[0], 'Answer: '+i[1]]

	# save the dataframe
	df.to_csv('./Output.csv', index=False)


if __name__ == '__main__':
	input_txt = open('./Input.txt', 'r', encoding="utf8").read()
	main(input_txt)