import re

OPERATOR=r" ?(\+|-) ?"
INT_PART = r'\d+'
OPTIONAL_DECIMAL = r'(?:\.|\.\d+)?'
NUMBER = f'{INT_PART}{OPTIONAL_DECIMAL}'
PERIOD_LETTER = r'(?:cd|CD|bd|BD|[dDwWmMqQsShHyY])'
DATE_PERIOD = f"(?:({NUMBER})({PERIOD_LETTER}))"
REPEATING_DATE_PERIODS = f"(?:{DATE_PERIOD}{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?{DATE_PERIOD}?)"
PIPE = r'\|'
TWOLETTERCAL = r'[A-ZA-Z][A-ZA-Z]'
REPEATING_CALUNIONS = f" ?{PIPE} ?({TWOLETTERCAL})(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?(?:u({TWOLETTERCAL}))?"
PIPE_REPEAT_CAL_UNION = f"(?:{REPEATING_CALUNIONS})?"
ROLL = r' ?/ ?(MF|MP|F|P) ?'
PIPE_ROLL = f"(?:{ROLL})?"
RHS_PATTERN = f"{OPERATOR}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION}{PIPE_ROLL}"
MATCH_WITH_DTPERIOD = f"(.*)(?= ?){RHS_PATTERN}"
MATCH_WITHORWITHOUT_DTPERIOD = f"(?:{MATCH_WITH_DTPERIOD})|(.*)"
FULL_PATTERN=MATCH_WITHORWITHOUT_DTPERIOD
PIPE_2 = r'(\|)?'
TWOLETTERCAL_2 = r'[u]?[A-ZA-Z][A-ZA-Z]'
REPEATING_CALUNIONS_2 = f" ?(?:{PIPE_2}) ?({TWOLETTERCAL_2})({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?({TWOLETTERCAL_2})?"
ROLL_2 = r' ?(/)? ?(MF|MP|F|P) ?'
PIPE_ROLL_2 = f"(?:{ROLL_2})?"
PIPE_REPEAT_CAL_UNION_2 = f"(?:{REPEATING_CALUNIONS_2})?"
OPERATOR_2 = r" ?(\+|-)? ?"
RHS_PATTERN_2 = f"{OPERATOR_2}{REPEATING_DATE_PERIODS} ?{PIPE_REPEAT_CAL_UNION_2}{PIPE_ROLL_2}"
TEST_DATES_1 = ['04/20/22', '04/20/2022', '4/20/22', '4/20/2022', '04-20-22', '04-20-2022', '4-20-22', '4-20-2022', '20220420', '20 apr 22', '20-apr-22', '20apr22', '20 apr 2022', '20-apr-2022', '20apr2022']
TEST_DATES_2 = ['10/07/22', '10/07/2022', '10/7/22', '10/7/2022', '10-07-22', '10-07-2022', '10-7-22', '10-7-2022', '20221007', '07 Oct 22', '07-Oct-22', '07Oct22', '07 Oct 2022', '07-Oct-2022', '07Oct2022','1/1/15','1/22/15','1/11/15','10/1/15']
PTNW = r'\bt0\b|\bt\b|\bT\b|\btoday\b|\bToday\b|\bTODAY\b'
PTN = r'[0-9][0-9]?[0-9]?[0-9]?\/?\-?\.?\ ?[0-9]?[0-9]?[0-9]?[0-9]?[a-zA-Z]?[a-z]?[a-z]?\/?\-?\.?\ ?[0-9][0-9]?[0-9]?[0-9]?'  # \/?\-?\.?\ ?


def date_matcher(string):
	letter = None
	string2 = string.lower()
	if 'dec' in string2:  # when to parse dates, if month has d,s,m letter it does not work so replace the letter with n
		string2 = string2.replace('dec','nec')
		letter = 'Dec'
	elif 'sep' in string2:
		string2 = string2.replace('sep','nec')
		letter = 'Sep'
	elif 'may' in string2:
		string2 = string2.replace('may','nec')
		letter = 'May'
	elif 'mar' in string2:
		string2 = string2.replace('mar','nec')
		letter = 'Mar'
	if letter is None:
		string = '+'+string
		string = string.replace('++','+')
	else:
		string2 = '+'+string2
		string2 = string2.replace('++','+')
	l = list(re.findall(FULL_PATTERN,string)[0]) if letter is None else list(re.findall(FULL_PATTERN,string2)[0])
	if l[0]=='' and l[-1]!='':
		l = list(reversed(l))
	l[0] = l[0][1:]
	if letter is not None:
		l[0] = l[0].replace('nec',letter)
	
	return l
def match_st_ed(string):
	string = string.replace(' ','')
	ptn = r'\d{4}|\d{2}|\d{1}|[a-zA-Z]+'
	rs = re.findall(ptn,string)
	return rs

def test_match_1():
	for i in range(len(TEST_DATES_1)):
		x = '+'.join([TEST_DATES_1[i] , TEST_DATES_2[i]])
		rs =  match_st_ed(x)
		print(rs)
def test_dt_formats():
	fs = ['1','11','01','2022','22']
	ch = [('/','/'),('.','.'),('',''),('-','-'),(' ',' ')]
	ms = ['Oct','2','10','02']
	# ch2 = ['/','.','','-',' ']
	ls = ['1','11','01','2022','22']
	dts_raw = []
	dts_conv = []
	ptn_l = []
	for f in fs:
		for c in ch:
			for m in ms:
				for l in ls:
					if (len(f)==1 or f=='01') and (len(l)==1 or l=='01'):
						continue
					if len(f)==4 and len(l)==4:
						continue
					st_ = ''.join([f,c[0],m,c[1],l])
					if c[0]=='' and c[1]=='':
						rs = 'd8'
						if not rs in ptn_l:
							ptn_l.append("d{8}")
					else:
						mid_ = f'd{len(m)}' if len(m)!=3 else  f'w{len(m)}'
						rs = f'd{len(f)}{c[0]}{mid_}{c[1]}d{len(l)}'
						if not rs in ptn_l:
							ptn_l.append(rs)
					dts_raw.append(st_)

if __name__=='__main__':
	string = '20200228 + 1 BD|CA/MF'
	string = string.replace(' ','')
	for i in range(len(TEST_DATES_2)):
		x = match_st_ed(TEST_DATES_2[i])
	y2 = '20150113-2014-1-25'
	y3 = '2015-01-1-2014-1-25'
	y4 = '2015-1-1-3bd'
	y5 = '-3bd'
	y6 = '3bd'
	y7 = '20150113'
	y8 = '20150113-3d|NY/MF'
	y9 = '1/3/22 - 2-1-19'
	y10 ='20150113-20140125'
	y11 ='20150113-1-25-2014'
	print(re.findall(PTN,y2))
	print(re.findall(PTN,y3))
	print(re.findall(PTN,y4))
	print(re.findall(PTN,y5))
	print(re.findall(PTN,y6))
	print(re.findall(PTN,y7))
	print(re.findall(PTN,y8))
	print(re.findall(PTN,y9))
	print(re.findall(PTN,y10))
	print(re.findall(PTN,y11))

	
