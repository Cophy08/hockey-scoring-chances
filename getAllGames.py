import requests, sqlite3, re
from bs4 import BeautifulSoup

myDB = sqlite3.connect('hsc.db')

# need to redo 2012030161
# need to deal with more players on ice

def pbpinsert(gameid):
	# redo game id, split and calculate
	gid = gameid
	year = str(gameid)[:4]+str(int(str(gameid)[:4])+1)
	gameid = str(gameid)[5:]

	cur = myDB.execute('SELECT id FROM pbp WHERE gid=?', [gid])
	fetchd = cur.fetchone()
	if fetchd is not None:
		return gameid
		# need something here to ID those who have something already

	url = "http://www.nhl.com/scores/htmlreports/"+year+"/PL0"+gameid+".HTM"

	r = requests.get(url)
	the_page = r.text
	soup = BeautifulSoup(the_page, 'html.parser') 

	rows = soup.findAll("tr", "evenColor")

	events = []

	for r in rows:
		cells = r.findAll("td")
		gnumber = int(cells[0].text)

		time = cells[3].text
		time = time[:time.find(":")+3]
		nums = time.split(":")
		timeup = (int(nums[0])*60 + int(nums[1]))
		timedown = 1200 - timeup

		period = int(cells[1].text)
		event = cells[4].text
		description = cells[5].text

		awayOnIce = cells[6].findAll('font')
		awayOnIce = [x.text for x in awayOnIce]
		awayOnIce = ' '.join(awayOnIce)
		awayOnIce = awayOnIce.split()

		homeOnIce = cells[6].findNextSiblings('td')[0].text
		homeOnIce = ' '.join(homeOnIce.split())
		homeOnIce = re.sub("[^0-9 ]", "", homeOnIce)
		homeOnIce = homeOnIce.split()

		# check len of
		if len(homeOnIce) < 6:
			homeOnIce += [-1]*(6-len(homeOnIce))
		if len(awayOnIce) < 6:
			awayOnIce += [-1]*(6-len(awayOnIce))

		newPBPdata = [gid, gnumber, period, timeup, timedown, event, description] + awayOnIce + homeOnIce	
		newPBPdata = tuple(newPBPdata)

		sql = "INSERT INTO pbp (gid, gnumber, period, timeup, timedown, event, description, v1, v2, v3, v4, v5, v6, h1, h2, h3, h4, h5, h6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

		# insert into db	
		try:			
			# save each item
			myDB.execute(sql, newPBPdata)
			myDB.commit()
		except Exception, err:
			print "FAILED TO INSERT: ",
			print str(err)
			print newPBPdata
			pass

	return -1

def pbp():
	gamesIDs = [2009020877, 2009020878, 2009020879, 2009020880, 2009020881, 2009020882, 2009020883, 2009020884, 2009020885, 2009020886, 2009020887, 2009020888, 2009020889, 2009020890, 2009020891, 2009020892, 2009020893, 2009020894, 2009020895, 2009020896, 2009020897, 2009020899, 2009020898, 2009020900, 2009020901, 2009020902, 2009020903, 2009020904, 2009020905, 2009020906, 2009020907, 2009020908, 2009020909, 2009020910, 2009020911, 2009020912, 2009020913, 2009020914, 2009020915, 2009020916, 2009020917, 2009020918, 2009020919, 2009020920, 2009020921, 2009090001, 2009090002, 2009090003, 2009090004, 2009090005, 2009090006, 2009090007, 2009090008, 2009090009, 2009090010, 2009090011, 2009090012, 2009090013, 2009090014, 2009090015, 2009090016, 2009090017, 2009090018, 2009090019, 2009090020, 2009090021, 2009090022, 2009090023, 2009090024, 2009090025, 2009090026, 2009090027, 2009090028, 2009090029, 2009090030, 2009020922, 2009020923, 2009020924, 2009020925, 2009020926, 2009020927, 2009020928, 2009020929, 2009020930, 2009020931, 2009020932, 2009020933, 2009020934, 2009020935, 2009020936, 2009020937, 2009020938, 2009020939, 2009020940, 2009020941, 2009020942, 2009020943, 2009020944, 2009020945, 2009020946, 2009020947, 2009020948, 2009020949, 2009020950, 2009020951, 2009020952, 2009020953, 2009020954, 2009020955, 2009020956, 2009020957, 2009020958, 2009020959, 2009020960, 2009020961, 2009020962, 2009020963, 2009020964, 2009020971, 2009020965, 2009020966, 2009020967, 2009020968, 2009020969, 2009020970, 2009020972, 2009020973, 2009020974, 2009020975, 2009020976, 2009020978, 2009020980, 2009020977, 2009020979, 2009020981, 2009020982, 2009020983, 2009020984, 2009020985, 2009020986, 2009020987, 2009020988, 2009020989, 2009020990, 2009020991, 2009020992, 2009020993, 2009020994, 2009020995, 2009020996, 2009020997, 2009020998, 2009020999, 2009021000, 2009021001, 2009021002, 2009021003, 2009021004, 2009021005, 2009021006, 2009021014, 2009021007, 2009021008, 2009021009, 2009021010, 2009021011, 2009021012, 2009021013, 2009021022, 2009021015, 2009021016, 2009021017, 2009021018, 2009021019, 2009021020, 2009021021, 2009021023, 2009021024, 2009021025, 2009021026, 2009021027, 2009021029, 2009021030, 2009021028, 2009021031, 2009021032, 2009021033, 2009021034, 2009021035, 2009021036, 2009021037, 2009021038, 2009021039, 2009021040, 2009021041, 2009021042, 2009021043, 2009021044, 2009021045, 2009021046, 2009021047, 2009021048, 2009021049, 2009021050, 2009021051, 2009021052, 2009021053, 2009021054, 2009021055, 2009021056, 2009021057, 2009021058, 2009021059, 2009021060, 2009021061, 2009021062, 2009021063, 2009021064, 2009021065, 2009021066, 2009021067, 2009021068, 2009021069, 2009021070, 2009021071, 2009021072, 2009021073, 2009021074, 2009021075, 2009021076, 2009021077, 2009021078, 2009021079, 2009021080, 2009021081, 2009021082, 2009021083, 2009021084, 2009021085, 2009021086, 2009021087, 2009021088, 2009021089, 2009021090, 2009021091, 2009021092, 2009021093, 2009021094, 2009021095, 2009021096, 2009021097, 2009021098, 2009021099, 2009021100, 2009021101, 2009021102, 2009021103, 2009021104, 2009021105, 2009021106, 2009021107, 2009021108, 2009021109, 2009021110, 2009021111, 2009021112, 2009021113, 2009021114, 2009021115, 2009021116, 2009021117, 2009021118, 2009021119, 2009021120, 2009021121, 2009021122, 2009021123, 2009021124, 2009021125, 2009021126, 2009021127, 2009021128, 2009021129, 2009021130, 2009021131, 2009021132, 2009021133, 2009021134, 2009021135, 2009021136, 2009021137, 2009021138, 2009021139, 2009021140, 2009021141, 2009021142, 2009021143, 2009021144, 2009021145, 2009021146, 2009021147, 2009021148, 2009021149, 2009021150, 2009021151, 2009021152, 2009021153, 2009021154, 2009021155, 2009021156, 2009021157, 2009021158, 2009021159, 2009021160, 2009021161, 2009021162, 2009021163, 2009021164, 2009021165, 2009021166, 2009021167, 2009021168, 2009021169, 2009021170, 2009021171, 2009021172, 2009021173, 2009021174, 2009021175, 2009021176, 2009021177, 2009021178, 2009021179, 2009021180, 2009021181, 2009021182, 2009021183, 2009021184, 2009021185, 2009021188, 2009021186, 2009021187, 2009021189, 2009021190, 2009021191, 2009021192, 2009021193, 2009021194, 2009021195, 2009021196, 2009021197, 2009021198, 2009021199, 2009021200, 2009021201, 2009021202, 2009021203, 2009021204, 2009021205, 2009021206, 2009021207, 2009021208, 2009021209, 2009021210, 2009021211, 2009021212, 2009021213, 2009021214, 2009021215, 2009021216, 2009021217, 2009021218, 2009021219, 2009021220, 2009021221, 2009021222, 2009021224, 2009021223, 2009021225, 2009021226, 2009021227, 2009021228, 2009021229, 2009021230, 2008030121, 2008030141, 2008030131, 2008030171, 2008030111, 2008030161, 2008030181, 2008030151, 2008030142, 2008030132, 2008030172, 2008030122, 2008030162, 2008030112, 2008030182, 2008030143, 2008030173, 2008030133, 2008030152, 2008030113, 2008030123, 2008030183, 2008030144, 2008030163, 2008030134, 2008030174, 2008030153, 2008030114, 2008030124, 2008030184, 2008030145, 2008030164, 2008030135, 2008030154, 2008030125, 2008030146, 2008030185, 2008030155, 2008030126, 2008030136, 2008030186, 2008030156, 2008030127, 2008030137, 2008030241, 2008030231, 2008030211, 2008030221, 2008030242, 2008030232, 2008030212, 2008030222, 2008030243, 2008030233, 2008030223, 2008030213, 2008030244, 2008030234, 2008030224, 2008030214, 2008030225, 2008030245, 2008030235, 2008030215, 2008030226, 2008030246, 2008030216, 2008030236, 2008030227, 2008030237, 2008030217, 2008030321, 2008030311, 2008030322, 2008030312, 2008030323, 2008030313, 2008030324, 2008030314, 2008030325, 2008030411, 2008030412, 2008030413, 2008030414, 2008030415, 2008030416, 2008030417, 2008020001, 2008020002, 2008020003, 2008020004, 2008020005, 2008020006, 2008020007, 2008020008, 2008020009, 2008020010, 2008020011, 2008020012, 2008020013, 2008020014, 2008020015, 2008020016, 2008020017, 2008020018, 2008020019, 2008020020, 2008020021, 2008020022, 2008020023, 2008020024, 2008020025, 2008020026, 2008020027, 2008020028, 2008020029, 2008020030, 2008020031, 2008020032, 2008020033, 2008020034, 2008020035, 2008020036, 2008020037, 2008020038, 2008020040, 2008020039, 2008020041, 2008020042, 2008020043, 2008020044, 2008020045, 2008020046, 2008020047, 2008020048, 2008020049, 2008020050, 2008020051, 2008020052, 2008020053, 2008020054, 2008020055, 2008020056, 2008020057, 2008020058, 2008020059, 2008020060, 2008020061, 2008020062, 2008020063, 2008020064, 2008020065, 2008020066, 2008020067, 2008020068, 2008020069, 2008020070, 2008020071, 2008020072, 2008020073, 2008020074, 2008020075, 2008020076, 2008020077, 2008020078, 2008020079, 2008020080, 2008020081, 2008020082, 2008020083, 2008020084, 2008020085, 2008020086, 2008020087, 2008020088, 2008020089, 2008020090, 2008020091, 2008020092, 2008020093, 2008020094, 2008020095, 2008020096, 2008020097, 2008020098, 2008020099, 2008020100, 2008020101, 2008020102, 2008020103, 2008020104, 2008020110, 2008020105, 2008020106, 2008020107, 2008020108, 2008020109, 2008020111, 2008020112, 2008020113, 2008020114, 2008020115, 2008020116, 2008020117, 2008020118, 2008020119, 2008020120, 2008020121, 2008020122, 2008020123, 2008020124, 2008020125, 2008020126, 2008020127, 2008020128, 2008020129, 2008020130, 2008020131, 2008020132, 2008020133, 2008020134, 2008020135, 2008020136, 2008020137, 2008020138, 2008020139, 2008020140, 2008020141, 2008020142, 2008020143, 2008020144, 2008020145, 2008020146, 2008020147, 2008020148, 2008020149, 2008020150, 2008020151, 2008020152, 2008020153, 2008020154, 2008020155, 2008020156, 2008020157, 2008020158, 2008020159, 2008020160, 2008020161, 2008020162, 2008020163, 2008020164, 2008020165, 2008020166, 2008020167, 2008020168, 2008020169, 2008020170, 2008020171, 2008020172, 2008020173, 2008020174, 2008020175, 2008020176, 2008020177, 2008020178, 2008020179, 2008020180, 2008020181, 2008020182, 2008020183, 2008020184, 2008020186, 2008020185, 2008020187, 2008020188, 2008020189, 2008020190, 2008020191, 2008020192, 2008020193, 2008020194, 2008020195, 2008020196, 2008020197, 2008020198, 2008020199, 2008020200, 2008020201, 2008020202, 2008020203, 2008020204, 2008020205, 2008020206, 2008020207, 2008020208, 2008020210, 2008020209, 2008020211, 2008020212, 2008020213, 2008020214, 2008020215, 2008020216, 2008020217, 2008020218, 2008020219, 2008020220, 2008020221, 2008020222, 2008020223, 2008020224, 2008020225, 2008020226, 2008020227, 2008020228, 2008020229, 2008020230, 2008020231, 2008020232, 2008020233, 2008020234, 2008020235, 2008020236, 2008020237, 2008020238, 2008020239, 2008020240, 2008020241, 2008020242, 2008020243, 2008020244, 2008020245, 2008020246, 2008020247, 2008020248, 2008020249, 2008020250, 2008020251, 2008020252, 2008020253, 2008020254, 2008020255, 2008020256, 2008020257, 2008020258, 2008020259, 2008020260, 2008020261, 2008020262, 2008020263, 2008020264, 2008020265, 2008020266, 2008020267, 2008020268, 2008020269, 2008020270, 2008020271, 2008020272, 2008020273, 2008020274, 2008020275, 2008020276, 2008020277, 2008020278, 2008020279, 2008020280, 2008020281, 2008020282, 2008020283, 2008020284, 2008020285, 2008020286, 2008020287, 2008020288, 2008020290, 2008020291, 2008020289, 2008020292, 2008020293, 2008020294, 2008020295, 2008020296, 2008020297, 2008020298, 2008020299, 2008020300, 2008020301, 2008020302, 2008020303, 2008020304, 2008020305, 2008020306, 2008020307, 2008020308, 2008020309, 2008020310, 2008020311, 2008020312, 2008020313, 2008020314, 2008020315, 2008020316, 2008020317, 2008020318, 2008020319, 2008020320, 2008020321, 2008020322, 2008020323, 2008020324, 2008020325, 2008020326, 2008020327, 2008020328, 2008020329, 2008020330, 2008020331, 2008020332, 2008020333, 2008020334, 2008020335, 2008020336, 2008020337, 2008020338, 2008020339, 2008020340, 2008020341, 2008020342, 2008020343, 2008020344, 2008020345, 2008020346, 2008020347, 2008020348, 2008020349, 2008020350, 2008020351, 2008020352, 2008020353, 2008020354, 2008020355, 2008020356, 2008020357, 2008020358, 2008020359, 2008020360, 2008020361, 2008020362, 2008020363, 2008020364, 2008020365, 2008020366, 2008020367, 2008020368, 2008020369, 2008020370, 2008020371, 2008020372, 2008020373, 2008020374, 2008020375, 2008020376, 2008020377, 2008020378, 2008020379, 2008020382, 2008020380, 2008020381, 2008020383, 2008020384, 2008020385, 2008020386, 2008020387, 2008020388, 2008020389, 2008020390, 2008020391, 2008020392, 2008020394, 2008020393, 2008020395, 2008020396, 2008020397, 2008020398, 2008020399, 2008020400, 2008020401, 2008020402, 2008020403, 2008020404, 2008020412, 2008020405, 2008020406, 2008020407, 2008020408, 2008020409, 2008020410, 2008020411, 2008020413, 2008020414, 2008020415, 2008020416, 2008020417, 2008020418, 2008020419, 2008020420, 2008020421, 2008020422, 2008020423, 2008020424, 2008020425, 2008020426, 2008020427, 2008020428, 2008020429, 2008020430, 2008020431, 2008020432, 2008020433, 2008020434, 2008020435, 2008020436, 2008020437, 2008020438, 2008020439, 2008020440, 2008020441, 2008020442, 2008020443, 2008020444, 2008020445, 2008020446, 2008020447, 2008020448, 2008020449, 2008020450, 2008020451, 2008020452, 2008020453, 2008020454, 2008020455, 2008020456, 2008020457, 2008020458, 2008020459, 2008020460, 2008020461, 2008020462, 2008020463, 2008020464, 2008020465, 2008020466, 2008020467, 2008020468, 2008020469, 2008020470, 2008020471, 2008020472, 2008020473, 2008020474, 2008020475, 2008020476, 2008020477, 2008020478, 2008020479, 2008020480, 2008020481, 2008020482, 2008020483, 2008020484, 2008020485, 2008020489, 2008020486, 2008020487, 2008020488, 2008020490, 2008020491, 2008020492, 2008020493, 2008020494, 2008020495, 2008020496, 2008020497, 2008020498, 2008020499, 2008020500, 2008020501, 2008020502, 2008020503, 2008020504, 2008020505, 2008020506, 2008020507, 2008020508, 2008020509, 2008020510, 2008020511, 2008020512, 2008020513, 2008020514, 2008020515, 2008020516, 2008020517, 2008020518, 2008020519, 2008020520, 2008020521, 2008020522, 2008020523, 2008020524, 2008020525, 2008020526, 2008020527, 2008020528, 2008020529, 2008020530, 2008020531, 2008020532, 2008020533, 2008020534, 2008020535, 2008020537, 2008020536, 2008020538, 2008020539, 2008020540, 2008020541, 2008020542, 2008020543, 2008020544, 2008020545, 2008020546, 2008020547, 2008020548, 2008020549, 2008020550, 2008020551, 2008020552, 2008020553, 2008020554, 2008020555, 2008020556, 2008020557, 2008020558, 2008020559, 2008020560, 2008020561, 2008020562, 2008020563, 2008020564, 2008020565, 2008020566, 2008020567, 2008020568, 2008020569, 2008020570, 2008020571, 2008020572, 2008020573, 2008020574, 2008020575, 2008020576, 2008020577, 2008020578, 2008020579, 2008020580, 2008020581, 2008020582, 2008020583, 2008020584, 2008020585, 2008020586, 2008020587, 2008020588, 2008020589, 2008020590, 2008020591, 2008020592, 2008020594, 2008020593, 2008020595, 2008020596, 2008020597, 2008020598, 2008020599, 2008020600, 2008020601, 2008020602, 2008020603, 2008020604, 2008020605, 2008020606, 2008020607, 2008020608, 2008020609, 2008020610, 2008020611, 2008020612, 2008020613, 2008020614, 2008020619, 2008020615, 2008020616, 2008020617, 2008020618, 2008020620, 2008020621, 2008020622, 2008020623, 2008020624, 2008020625, 2008020626, 2008020627, 2008020628, 2008020629, 2008020630, 2008020631, 2008020632, 2008020633, 2008020634, 2008020635, 2008020636, 2008020637, 2008020638, 2008020639, 2008020640, 2008020641, 2008020642, 2008020643, 2008020644, 2008020645, 2008020646, 2008020647, 2008020648, 2008020649, 2008020650, 2008020651, 2008020652, 2008020653, 2008020654, 2008020655, 2008020656, 2008020657, 2008020658, 2008020659, 2008020660, 2008020661, 2008020662, 2008020663, 2008020664, 2008020665, 2008020666, 2008020667, 2008020668, 2008020669, 2008020670, 2008020671, 2008020672, 2008020673, 2008020674, 2008020676, 2008020675, 2008020677, 2008020678, 2008020679, 2008020680, 2008020681, 2008020682, 2008020683, 2008020684, 2008020685, 2008020686, 2008020687, 2008020688, 2008020689, 2008020690, 2008020691, 2008020692, 2008020693, 2008020694, 2008020695, 2008020696, 2008020697, 2008020698, 2008020699, 2008020700, 2008040057, 2008020701, 2008020702, 2008020703, 2008020704, 2008020705, 2008020706, 2008020707, 2008020708, 2008020709, 2008020710, 2008020711, 2008020712, 2008020713, 2008020714, 2008020715, 2008020716, 2008020717, 2008020718, 2008020719, 2008020720, 2008020721, 2008020722, 2008020723, 2008020724, 2008020725, 2008020726, 2008020727, 2008020728, 2008020729, 2008020730, 2008020731, 2008020732, 2008020733, 2008020734, 2008020735, 2008020736, 2008020737, 2008020738, 2008020739, 2008020740, 2008020741, 2008020742, 2008020743, 2008020744, 2008020745, 2008020746, 2008020747, 2008020748, 2008020749, 2008020751, 2008020752, 2008020753, 2008020754, 2008020750, 2008020755, 2008020756, 2008020757, 2008020758, 2008020759, 2008020760, 2008020761, 2008020762, 2008020763, 2008020764, 2008020765, 2008020766, 2008020767, 2008020768, 2008020769, 2008020770, 2008020771, 2008020772, 2008020773, 2008020774, 2008020775, 2008020776, 2008020777, 2008020778, 2008020779, 2008020780, 2008020781, 2008020782, 2008020783, 2008020784, 2008020785, 2008020786, 2008020787, 2008020788, 2008020789, 2008020790, 2008020791, 2008020792, 2008020793, 2008020794, 2008020795, 2008020796, 2008020797, 2008020798, 2008020799, 2008020800, 2008020801, 2008020802, 2008020803, 2008020804, 2008020805, 2008020806, 2008020807, 2008020808, 2008020809, 2008020810, 2008020811, 2008020812, 2008020813, 2008020814, 2008020815, 2008020816, 2008020817, 2008020818, 2008020819, 2008020820, 2008020821, 2008020822, 2008020823, 2008020824, 2008020825, 2008020826, 2008020827, 2008020828, 2008020829, 2008020830, 2008020831, 2008020832, 2008020833, 2008020835, 2008020834, 2008020836, 2008020837, 2008020838, 2008020839, 2008020840, 2008020841, 2008020842, 2008020843, 2008020844, 2008020845, 2008020846, 2008020847, 2008020848, 2008020849, 2008020850, 2008020851, 2008020852, 2008020853, 2008020854, 2008020855, 2008020856, 2008020857, 2008020858, 2008020859, 2008020860, 2008020861, 2008020862, 2008020863, 2008020864, 2008020865, 2008020866, 2008020867, 2008020868, 2008020869, 2008020870, 2008020871, 2008020872, 2008020873, 2008020874, 2008020876, 2008020875, 2008020877, 2008020878, 2008020879, 2008020880, 2008020881, 2008020882, 2008020883, 2008020884, 2008020885, 2008020886, 2008020887, 2008020888, 2008020889, 2008020891, 2008020890, 2008020892, 2008020893, 2008020894, 2008020895, 2008020896, 2008020897, 2008020898, 2008020899, 2008020900, 2008020901, 2008020902, 2008020903, 2008020904, 2008020905, 2008020906, 2008020907, 2008020908, 2008020909, 2008020910, 2008020911, 2008020912, 2008020913, 2008020914, 2008020915, 2008020916, 2008020917, 2008020918, 2008020919, 2008020920, 2008020921, 2008020922, 2008020923, 2008020924, 2008020925, 2008020926, 2008020927, 2008020928, 2008020929, 2008020930, 2008020931, 2008020932, 2008020933, 2008020934, 2008020935, 2008020936, 2008020937, 2008020938, 2008020939, 2008020940, 2008020941, 2008020942, 2008020943, 2008020944, 2008020945, 2008020946, 2008020947, 2008020948, 2008020949, 2008020950, 2008020951, 2008020952, 2008020953, 2008020954, 2008020955, 2008020956, 2008020957, 2008020958, 2008020959, 2008020960, 2008020961, 2008020962, 2008020963, 2008020964, 2008020965, 2008020966, 2008020967, 2008020968, 2008020969, 2008020970, 2008020971, 2008020972, 2008020973, 2008020974, 2008020975, 2008020976, 2008020977, 2008020978, 2008020980, 2008020979, 2008020981, 2008020982, 2008020983, 2008020984, 2008020985, 2008020986, 2008020987, 2008020988, 2008020989, 2008020990, 2008020991, 2008020992, 2008020993, 2008020994, 2008020995, 2008020996, 2008020997, 2008020998, 2008020999, 2008021000, 2008021001, 2008021002, 2008021003, 2008021004, 2008021005, 2008021006, 2008021007, 2008021010, 2008021008, 2008021009, 2008021011, 2008021012, 2008021013, 2008021014, 2008021015, 2008021016, 2008021017, 2008021018, 2008021019, 2008021020, 2008021021, 2008021022, 2008021023, 2008021024, 2008021025, 2008021026, 2008021027, 2008021028, 2008021029, 2008021030, 2008021031, 2008021032, 2008021033, 2008021034, 2008021035, 2008021036, 2008021037, 2008021038, 2008021039, 2008021040, 2008021041, 2008021042, 2008021043, 2008021044, 2008021045, 2008021046, 2008021047, 2008021048, 2008021049, 2008021050, 2008021051, 2008021052, 2008021053, 2008021054, 2008021055, 2008021056, 2008021057, 2008021058, 2008021059, 2008021060, 2008021061, 2008021062, 2008021063, 2008021064, 2008021065, 2008021066, 2008021067, 2008021068, 2008021069, 2008021070, 2008021071, 2008021072, 2008021073, 2008021074, 2008021075, 2008021076, 2008021077, 2008021079, 2008021078, 2008021080, 2008021081, 2008021082, 2008021083, 2008021084, 2008021085, 2008021086, 2008021087, 2008021088, 2008021089, 2008021090, 2008021091, 2008021092, 2008021093, 2008021094, 2008021095, 2008021096, 2008021097, 2008021098, 2008021099, 2008021100, 2008021101, 2008021102, 2008021103, 2008021104, 2008021105, 2008021106, 2008021107, 2008021108, 2008021109, 2008021110, 2008021111, 2008021112, 2008021113, 2008021114, 2008021115, 2008021116, 2008021122, 2008021117, 2008021118, 2008021119, 2008021120, 2008021121, 2008021123, 2008021124, 2008021125, 2008021126, 2008021127, 2008021128, 2008021129, 2008021130, 2008021131, 2008021132, 2008021133, 2008021134, 2008021135, 2008021136, 2008021137, 2008021138, 2008021139, 2008021140, 2008021141, 2008021142, 2008021143, 2008021144, 2008021145, 2008021146, 2008021147, 2008021148, 2008021149, 2008021150, 2008021151, 2008021152, 2008021153, 2008021154, 2008021155, 2008021156, 2008021157, 2008021158, 2008021159, 2008021160, 2008021161, 2008021162, 2008021163, 2008021164, 2008021165, 2008021166, 2008021167, 2008021168, 2008021169, 2008021170, 2008021171, 2008021172, 2008021173, 2008021174, 2008021177, 2008021175, 2008021176, 2008021178, 2008021179, 2008021180, 2008021181, 2008021182, 2008021183, 2008021184, 2008021185, 2008021186, 2008021187, 2008021188, 2008021189, 2008021190, 2008021191, 2008021192, 2008021193, 2008021194, 2008021195, 2008021196, 2008021197, 2008021198, 2008021199, 2008021200, 2008021201, 2008021202, 2008021203, 2008021204, 2008021205, 2008021206, 2008021207, 2008021208, 2008021209, 2008021210, 2008021211, 2008021212, 2008021213, 2008021214, 2008021215, 2008021216, 2008021217, 2008021218, 2008021219, 2008021220, 2008021221, 2008021222, 2008021223, 2008021224, 2008021225, 2008021226, 2008021230, 2008021227, 2008021228, 2008021229, 2007030121, 2007030141, 2007030171, 2007030161, 2007030111, 2007030151, 2007030162, 2007030181, 2007030122, 2007030131, 2007030142, 2007030172, 2007030152, 2007030112, 2007030182, 2007030132, 2007030113, 2007030143, 2007030163, 2007030123, 2007030153, 2007030173, 2007030114, 2007030133, 2007030183, 2007030164, 2007030174, 2007030124, 2007030144, 2007030154, 2007030115, 2007030134, 2007030184, 2007030175, 2007030165, 2007030145, 2007030155, 2007030185, 2007030135, 2007030116, 2007030176, 2007030156, 2007030166, 2007030186, 2007030117, 2007030136, 2007030137, 2007030167, 2007030211, 2007030231, 2007030221, 2007030241, 2007030232, 2007030212, 2007030222, 2007030242, 2007030213, 2007030223, 2007030243, 2007030233, 2007030214, 2007030244, 2007030224, 2007030234, 2007030245, 2007030215, 2007030225, 2007030246, 2007030321, 2007030311, 2007030322, 2007030312, 2007030323, 2007030313, 2007030324, 2007030314, 2007030325, 2007030315, 2007030326, 2007030411, 2007030412, 2007030413, 2007030414, 2007030415, 2007030416, 2007020001, 2007020002, 2007020003, 2007020004, 2007020005, 2007020006, 2007020007, 2007020008, 2007020009, 2007020010, 2007020011, 2007020013, 2007020012, 2007020014, 2007020015, 2007020016, 2007020017, 2007020018, 2007020019, 2007020020, 2007020022, 2007020023, 2007020024, 2007020025, 2007020026, 2007020027, 2007020028, 2007020021, 2007020029, 2007020030, 2007020031, 2007020032, 2007020033, 2007020034, 2007020035, 2007020036, 2007020037, 2007020038, 2007020039, 2007020040, 2007020041, 2007020042, 2007020043, 2007020044, 2007020045, 2007020046, 2007020047, 2007020048, 2007020049, 2007020051, 2007020050, 2007020052, 2007020053, 2007020054, 2007020055, 2007020056, 2007020057, 2007020058, 2007020059, 2007020060, 2007020061, 2007020062, 2007020063, 2007020064, 2007020065, 2007020066, 2007020067, 2007020068, 2007020069, 2007020070, 2007020071, 2007020072, 2007020073, 2007020074, 2007020075, 2007020076, 2007020077, 2007020078, 2007020079, 2007020080, 2007020081, 2007020082, 2007020083, 2007020084, 2007020085, 2007020086, 2007020087, 2007020088, 2007020089, 2007020090, 2007020091, 2007020092, 2007020093, 2007020094, 2007020095, 2007020096, 2007020097, 2007020098, 2007020099, 2007020100, 2007020101, 2007020102, 2007020103, 2007020104, 2007020105, 2007020106, 2007020107, 2007020108, 2007020109, 2007020110, 2007020111, 2007020112, 2007020113, 2007020114, 2007020115, 2007020116, 2007020117, 2007020118, 2007020119, 2007020120, 2007020121, 2007020122, 2007020123, 2007020124, 2007020125, 2007020126, 2007020127, 2007020128, 2007020129, 2007020130, 2007020131, 2007020132, 2007020133, 2007020134, 2007020135, 2007020136, 2007020137, 2007020138, 2007020139, 2007020140, 2007020141, 2007020142, 2007020143, 2007020144, 2007020146, 2007020145, 2007020147, 2007020148, 2007020149, 2007020150, 2007020151, 2007020152, 2007020153, 2007020154, 2007020155, 2007020156, 2007020157, 2007020158, 2007020159, 2007020160, 2007020161, 2007020162, 2007020163, 2007020164, 2007020165, 2007020166, 2007020167, 2007020168, 2007020169, 2007020170, 2007020171, 2007020172, 2007020173, 2007020174, 2007020175, 2007020176, 2007020177, 2007020179, 2007020178, 2007020181, 2007020180, 2007020182, 2007020183, 2007020184, 2007020185, 2007020186, 2007020187, 2007020188, 2007020189, 2007020190, 2007020191, 2007020192, 2007020193, 2007020194, 2007020195, 2007020196, 2007020197, 2007020198, 2007020199, 2007020200, 2007020201, 2007020202, 2007020203, 2007020204, 2007020205, 2007020206, 2007020207, 2007020208, 2007020209, 2007020210, 2007020211, 2007020212, 2007020213, 2007020214, 2007020215, 2007020216, 2007020217, 2007020218, 2007020219, 2007020220, 2007020222, 2007020223, 2007020224, 2007020221, 2007020225, 2007020226, 2007020227, 2007020228, 2007020229, 2007020230, 2007020231, 2007020232, 2007020233, 2007020234, 2007020235, 2007020236, 2007020237, 2007020238, 2007020239, 2007020240, 2007020241, 2007020242, 2007020243, 2007020244, 2007020245, 2007020246, 2007020247, 2007020248, 2007020249, 2007020250, 2007020251, 2007020252, 2007020253, 2007020254, 2007020255, 2007020256, 2007020257, 2007020258, 2007020259, 2007020260, 2007020261, 2007020262, 2007020263, 2007020264, 2007020265, 2007020266, 2007020267, 2007020268, 2007020269, 2007020270, 2007020271, 2007020272, 2007020273, 2007020274, 2007020275, 2007020276, 2007020277, 2007020278, 2007020279, 2007020280, 2007020281, 2007020282, 2007020283, 2007020284, 2007020285, 2007020286, 2007020287, 2007020288, 2007020289, 2007020290, 2007020291, 2007020292, 2007020293, 2007020294, 2007020295, 2007020296, 2007020297, 2007020299, 2007020298, 2007020301, 2007020302, 2007020303, 2007020304, 2007020300, 2007020305, 2007020306, 2007020307, 2007020308, 2007020309, 2007020310, 2007020311, 2007020312, 2007020313, 2007020314, 2007020315, 2007020316, 2007020317, 2007020318, 2007020319, 2007020320, 2007020321, 2007020322, 2007020323, 2007020324, 2007020325, 2007020326, 2007020327, 2007020328, 2007020329, 2007020330, 2007020334, 2007020331, 2007020332, 2007020333, 2007020335, 2007020336, 2007020337, 2007020338, 2007020339, 2007020340, 2007020341, 2007020342, 2007020343, 2007020344, 2007020345, 2007020346, 2007020347, 2007020348, 2007020349, 2007020350, 2007020351, 2007020352, 2007020353, 2007020354, 2007020355, 2007020356, 2007020357, 2007020358, 2007020359, 2007020360, 2007020361, 2007020362, 2007020363, 2007020364, 2007020365, 2007020366, 2007020367, 2007020368, 2007020369, 2007020370, 2007020371, 2007020372, 2007020373, 2007020374, 2007020375, 2007020376, 2007020377, 2007020378, 2007020379, 2007020380, 2007020381, 2007020382, 2007020383, 2007020384, 2007020385, 2007020386, 2007020387, 2007020388, 2007020389, 2007020390, 2007020391, 2007020392, 2007020393, 2007020394, 2007020395, 2007020396, 2007020397, 2007020398, 2007020399, 2007020400, 2007020401, 2007020402, 2007020403, 2007020404, 2007020405, 2007020406, 2007020407, 2007020408, 2007020409, 2007020410, 2007020411, 2007020412, 2007020413, 2007020414, 2007020415, 2007020416, 2007020417, 2007020418, 2007020419, 2007020420, 2007020421, 2007020422, 2007020423, 2007020424, 2007020425, 2007020426, 2007020427, 2007020428, 2007020429, 2007020430, 2007020431, 2007020432, 2007020433, 2007020434, 2007020435, 2007020436, 2007020437, 2007020438, 2007020439, 2007020440, 2007020441, 2007020442, 2007020443, 2007020444, 2007020445, 2007020446, 2007020447, 2007020449, 2007020450, 2007020448, 2007020451, 2007020452, 2007020453, 2007020454, 2007020455, 2007020456, 2007020457, 2007020458, 2007020459, 2007020460, 2007020461, 2007020462, 2007020463, 2007020464, 2007020465, 2007020466, 2007020467, 2007020479, 2007020468, 2007020469, 2007020470, 2007020471, 2007020472, 2007020473, 2007020474, 2007020475, 2007020476, 2007020477, 2007020478, 2007020480, 2007020481, 2007020482, 2007020483, 2007020484, 2007020485, 2007020486, 2007020487, 2007020488, 2007020489, 2007020490, 2007020491, 2007020492, 2007020493, 2007020494, 2007020495, 2007020496, 2007020497, 2007020498, 2007020499, 2007020500, 2007020501, 2007020502, 2007020503, 2007020504, 2007020505, 2007020506, 2007020507, 2007020508, 2007020509, 2007020510, 2007020511, 2007020512, 2007020513, 2007020514, 2007020516, 2007020515, 2007020517, 2007020518, 2007020519, 2007020520, 2007020521, 2007020522, 2007020523, 2007020524, 2007020525, 2007020526, 2007020527, 2007020528, 2007020529, 2007020530, 2007020531, 2007020532, 2007020533, 2007020534, 2007020535, 2007020536, 2007020538, 2007020539, 2007020540, 2007020537, 2007020541, 2007020542, 2007020543, 2007020544, 2007020545, 2007020546, 2007020549, 2007020547, 2007020548, 2007020550, 2007020551, 2007020552, 2007020553, 2007020554, 2007020555, 2007020556, 2007020557, 2007020558, 2007020559, 2007020560, 2007020561, 2007020562, 2007020563, 2007020564, 2007020565, 2007020566, 2007020567, 2007020568, 2007020569, 2007020570, 2007020571, 2007020572, 2007020573, 2007020574, 2007020575, 2007020576, 2007020577, 2007020578, 2007020579, 2007020580, 2007020581, 2007020582, 2007020583, 2007020584, 2007020585, 2007020586, 2007020587, 2007020588, 2007020589, 2007020590, 2007020591, 2007020592, 2007020593, 2007020594, 2007020595, 2007020596, 2007020597, 2007020598, 2007020599, 2007020600, 2007020601, 2007020602, 2007020603, 2007020604, 2007020605, 2007020606, 2007020607, 2007020608, 2007020609, 2007020610, 2007020614, 2007020611, 2007020612, 2007020613, 2007020615, 2007020616, 2007020617, 2007020618, 2007020619, 2007020620, 2007020621, 2007020622, 2007020623, 2007020624, 2007020625, 2007020626, 2007020627, 2007020628, 2007020629, 2007020630, 2007020631, 2007020632, 2007020633, 2007020634, 2007020635, 2007020636, 2007020637, 2007020638, 2007020639, 2007020640, 2007020642, 2007020643, 2007020644, 2007020641, 2007020645, 2007020646, 2007020647, 2007020648, 2007020649, 2007020650, 2007020651, 2007020652, 2007020653, 2007020654, 2007020655, 2007020656, 2007020657, 2007020658, 2007020659, 2007020660, 2007020661, 2007020662, 2007020663, 2007020664, 2007020665, 2007020666, 2007020667, 2007020668, 2007020669, 2007020670, 2007020671, 2007020672, 2007020673, 2007020674, 2007020675, 2007020676, 2007020677, 2007020678, 2007020679, 2007020680, 2007020681, 2007020682, 2007020683, 2007020684, 2007020685, 2007020686, 2007020687, 2007020688, 2007020689, 2007020690, 2007020691, 2007020692, 2007020693, 2007020694, 2007020695, 2007020696, 2007020697, 2007020698, 2007020699, 2007020700, 2007020701, 2007020702, 2007020703, 2007020704, 2007020705, 2007020706, 2007020712, 2007020707, 2007020708, 2007020709, 2007020710, 2007020711, 2007020713, 2007020714, 2007020715, 2007020716, 2007020718, 2007020717, 2007020719, 2007020720, 2007020721, 2007020722, 2007020723, 2007020724, 2007020725, 2007020726, 2007020727, 2007020728, 2007020729, 2007020730, 2007020731, 2007020732, 2007020733, 2007020734, 2007020735, 2007020736, 2007020737, 2007020738, 2007020739, 2007020740, 2007020741, 2007020742, 2007020744, 2007020745, 2007020746, 2007020747, 2007020743, 2007020748, 2007020749, 2007020750, 2007020751, 2007020752, 2007020753, 2007040056, 2007020754, 2007020755, 2007020756, 2007020757, 2007020758, 2007020759, 2007020762, 2007020760, 2007020761, 2007020763, 2007020764, 2007020765, 2007020768, 2007020766, 2007020767, 2007020769, 2007020770, 2007020771, 2007020772, 2007020773, 2007020774, 2007020775, 2007020776, 2007020777, 2007020778, 2007020779, 2007020780, 2007020781, 2007020782, 2007020783, 2007020784, 2007020796, 2007020785, 2007020786, 2007020787, 2007020788, 2007020789, 2007020790, 2007020791, 2007020792, 2007020793, 2007020794, 2007020795, 2007020797, 2007020798, 2007020799, 2007020800, 2007020801, 2007020802, 2007020803, 2007020804, 2007020805, 2007020806, 2007020807, 2007020808, 2007020809, 2007020810, 2007020811, 2007020812, 2007020813, 2007020814, 2007020815, 2007020816, 2007020817, 2007020818, 2007020819, 2007020820, 2007020821, 2007020822, 2007020823, 2007020824, 2007020825, 2007020826, 2007020827, 2007020828, 2007020829, 2007020830, 2007020831, 2007020832, 2007020833, 2007020834, 2007020835, 2007020836, 2007020837, 2007020838, 2007020839, 2007020840, 2007020841, 2007020842, 2007020843, 2007020844, 2007020845, 2007020846, 2007020847, 2007020848, 2007020849, 2007020850, 2007020851, 2007020852, 2007020853, 2007020855, 2007020854, 2007020856, 2007020857, 2007020859, 2007020858, 2007020860, 2007020862, 2007020863, 2007020864, 2007020861, 2007020865, 2007020866, 2007020867, 2007020868, 2007020869, 2007020870, 2007020871, 2007020872, 2007020873, 2007020874, 2007020875, 2007020876, 2007020877, 2007020878, 2007020879, 2007020880, 2007020881, 2007020882, 2007020883, 2007020884, 2007020885, 2007020886, 2007020887, 2007020888, 2007020889, 2007020891, 2007020892, 2007020893, 2007020890, 2007020894, 2007020895, 2007020896, 2007020897, 2007020898, 2007020899, 2007020900, 2007020901, 2007020902, 2007020903, 2007020904, 2007020905, 2007020906, 2007020907, 2007020908, 2007020909, 2007020910, 2007020911, 2007020912, 2007020913, 2007020914, 2007020915, 2007020916, 2007020917, 2007020918, 2007020919, 2007020920, 2007020921, 2007020922, 2007020923, 2007020924, 2007020925, 2007020926, 2007020927, 2007020928, 2007020929, 2007020930, 2007020931, 2007020932, 2007020933, 2007020934, 2007020935, 2007020937, 2007020936, 2007020938, 2007020939, 2007020940, 2007020941, 2007020942, 2007020943, 2007020944, 2007020945, 2007020946, 2007020947, 2007020948, 2007020949, 2007020951, 2007020952, 2007020953, 2007020950, 2007020954, 2007020955, 2007020956, 2007020957, 2007020958, 2007020959, 2007020960, 2007020961, 2007020962, 2007020963, 2007020964, 2007020965, 2007020966, 2007020967, 2007020968, 2007020969, 2007020970, 2007020971, 2007020972, 2007020973, 2007020974, 2007020975, 2007020976, 2007020977, 2007020978, 2007020979, 2007020980, 2007020981, 2007020982, 2007020983, 2007020984, 2007020986, 2007020985, 2007020987, 2007020990, 2007020991, 2007020992, 2007020989, 2007020988, 2007020993, 2007020994, 2007020995, 2007020996, 2007020997, 2007020998, 2007020999, 2007021000, 2007021001, 2007021002, 2007021003, 2007021004, 2007021006, 2007021007, 2007021005, 2007021009, 2007021008, 2007021010, 2007021011, 2007021012, 2007021013, 2007021014, 2007021015, 2007021016, 2007021017, 2007021018, 2007021019, 2007021020, 2007021021, 2007021022, 2007021023, 2007021024, 2007021025, 2007021026, 2007021027, 2007021028, 2007021034, 2007021029, 2007021030, 2007021031, 2007021032, 2007021033, 2007021035, 2007021036, 2007021038, 2007021037, 2007021039, 2007021040, 2007021041, 2007021042, 2007021043, 2007021044, 2007021045, 2007021046, 2007021047, 2007021048, 2007021049, 2007021050, 2007021051, 2007021052, 2007021053, 2007021054, 2007021055, 2007021056, 2007021057, 2007021058, 2007021059, 2007021060, 2007021061, 2007021062, 2007021063, 2007021064, 2007021065, 2007021066, 2007021067, 2007021068, 2007021069, 2007021070, 2007021071, 2007021072, 2007021073, 2007021074, 2007021075, 2007021076, 2007021077, 2007021078, 2007021079, 2007021080, 2007021083, 2007021081, 2007021082, 2007021084, 2007021085, 2007021086, 2007021087, 2007021088, 2007021089, 2007021090, 2007021091, 2007021092, 2007021093, 2007021094, 2007021095, 2007021096, 2007021097, 2007021098, 2007021099, 2007021100, 2007021101, 2007021102, 2007021103, 2007021104, 2007021105, 2007021106, 2007021107, 2007021108, 2007021109, 2007021110, 2007021111, 2007021112, 2007021113, 2007021114, 2007021115, 2007021116, 2007021117, 2007021118, 2007021119, 2007021120, 2007021121, 2007021122, 2007021123, 2007021124, 2007021125, 2007021126, 2007021127, 2007021128, 2007021129, 2007021130, 2007021131, 2007021132, 2007021133, 2007021134, 2007021135, 2007021136, 2007021137, 2007021138, 2007021139, 2007021140, 2007021141, 2007021143, 2007021142, 2007021144, 2007021145, 2007021146, 2007021147, 2007021148, 2007021149, 2007021150, 2007021151, 2007021152, 2007021153, 2007021154, 2007021155, 2007021156, 2007021157, 2007021158, 2007021159, 2007021161, 2007021160, 2007021162, 2007021163, 2007021164, 2007021165, 2007021166, 2007021167, 2007021168, 2007021169, 2007021170, 2007021171, 2007021172, 2007021173, 2007021174, 2007021175, 2007021176, 2007021177, 2007021179, 2007021180, 2007021178, 2007021181, 2007021182, 2007021183, 2007021184, 2007021185, 2007021186, 2007021187, 2007021188, 2007021189, 2007021190, 2007021191, 2007021192, 2007021193, 2007021194, 2007021195, 2007021196, 2007021197, 2007021198, 2007021199, 2007021200, 2007021201, 2007021202, 2007021203, 2007021204, 2007021205, 2007021206, 2007021207, 2007021209, 2007021208, 2007021210, 2007021211, 2007021212, 2007021213, 2007021214, 2007021215, 2007021216, 2007021218, 2007021217, 2007021219, 2007021220, 2007021221, 2007021222, 2007021223, 2007021226, 2007021224, 2007021225, 2007021227, 2007021228, 2007021229, 2007021230]
	fails = []
	for gid in gamesIDs:
		print gid
		value = pbpinsert(gid)
		if value > -1:
			fails.append(value) 
			print "%s FAILED" % (value)