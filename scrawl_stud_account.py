import requests
from bs4 import BeautifulSoup as b

payload = {'mail_id':'404040523', 'mail_pwd':'gibe258deny700'}
rs = requests.session()
res = rs.post('http://stu.fju.edu.tw/stusql/SingleSignOn/StuScore/SSO_stu_login.asp', data = payload)
res2 = rs.get('http://stu.fju.edu.tw/stusql/SingleSignOn/StuScore/stu_scoreter.asp')
#print(res2.content)
soup = b(res2.content, "html.parser")
'''
all_td1 = soup.find_all('td', {'align': 'left', 'valign': None})
list1 = []
for obj in all_td1:
    list1.append(obj.contents[0])
    #print(obj)

for obj in list1:
    print(obj.string)

print("===============")
all_td2 = soup.find_all('td', {'align': 'center', 'valign': None})
list2 = []
for obj in all_td2:
    list2.append(obj.contents[0])
    #print(obj)

for obj in list2:
    print(obj.string)

print("===============")
all_td3 = soup.find_all('td', {'align': 'right', 'valign': None})
list3 = []
for obj in all_td3:
    list3.append(obj.contents[0])
    #print(obj)

for obj in list3:
    print(obj.string)
'''
######################################################################
all_td1 = soup.find_all('td', {'align': 'left', 'valign': None})
list1 = []
for obj in all_td1:
    list1.append(obj.contents[0].strip())
print(list1)

all_td2 = soup.find_all('td', {'align': 'center', 'valign': None})
list2 = []
for obj in all_td2:
    list2.append(obj.contents[0])
new_list2 = []
for i in range(1, len(list2), 4):
	if i >= 9:
		#print(list2[i])	#9, 13, 17, 21
		new_list2.append(list2[i].strip())
print(new_list2)

all_td3 = soup.find_all('td', {'align': 'right', 'valign': None})
list3 = []
for obj in all_td3:
    list3.append(obj.contents[0].strip())
print(list3)

content = ''
for i in range(len(list1)):
    content += str(list1[i]) + '\t' + str(new_list2[i])+ " 學分" + "\n成績：" + str(list3[i]) + '\n\n'
print(content)