import requests
import re


baseURL = 'https://th.wikipedia.org'
response = requests.get(f'{baseURL}/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%84%E0%B8%97%E0%B8%A2')


# get all province links
provinces = ['พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'อุบลราชธานี']

achors = []
for province in provinces:
    reg = f'<a href=".*" title="รายชื่อวัดในจังหวัด{province}">'
    match = re.findall(reg, response.text)
    achors.append(match[0])

links = []
for achor in achors:
    reg = r'"(.*?)"'
    # ( .* -> any string ?) -> have single ")" 
    match = re.search(reg, achor)
    links.append(match.groups(1)[0])

HTMLs = []
for link in links:
    url = f'{baseURL}{link}'
    HTML = requests.get(url).text
    HTMLs.append(HTML)


ans = {}
lis = []
# get all วัด in link
for province, HTML in zip(provinces, HTMLs):
    # RegX เอา tag <li> ที่มีคำว่า วัด หรือ สำนัก อยู่ระหว่าง tag และต้องมาก่อนคำว่า "รายชื่อวัดในประเทศไทยแบ่งตามจังหวัด" หรือต้องมาก่อน footer นั้นเอง
    reg = r'<li>.*(?:วัด|สำนัก).*?<(?=[\s\S]*รายชื่อวัดในประเทศไทยแบ่งตามจังหวัด)'     
    finds = re.findall(reg, HTML)
    
    def transform(x):
        reg = r'>((?:วัด|สำนัก).*?)<'
        regDistrict = r'>(.*?) ตำบล'
        if re.search(" ตำบล", x): # check if string include ตำบล จะมาในกรณีที่ เป็น <li> ที่ไม่เป็น <a>
            res = re.findall(regDistrict, x)[0].strip()
            if re.search(r"(?:<a|<b)", res): # กรณียังไม่หลุดเป็น ชื่อจังหวัด เพราะ regular ข้างต้น ยังมี <a>หรือ <b>อยู่ | เพราะมี ตำบลมาก่อน tag ปิด
                if re.search('<b', res): # ถ้า <b> tag
                    return re.split("b>", res)[1] # split แล้วเอาหลัง b> มา เพราะตอน transform ไม่มี tag ปิดอยู่แล้ว
                return re.findall(reg, res)[0]
            return res
        else:
            res = re.findall(reg, x)[0].strip()
            if re.search(r"(?:<a|<b)", res):
                if re.search('<b', res):
                    return re.split("b>", res)[1]
                return re.findall(reg, res)[0]
            return res

    temples = list(map(transform, finds))
    if temples[-1] == 'วัดไทย': # เอาตรงเพิ่มเติมออก
        temples.pop()
    ans[province] = temples
    lis.extend(temples)

#     with open(f'{province}.csv', 'w', encoding='UTF8') as f:
#         f.write('ชื่อวัด\n')
#         for temple in temples:
#             f.write(f'{temple}\n')

# with open(f'yoowhat-temples.csv', 'w', encoding='UTF8') as f:
#     for temple in lis:
#         f.write(f'{temple}\n')


    