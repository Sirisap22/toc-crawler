import requests
import re


provinces = ['พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'อุบลราชธานี']

def getWikipediaThaiTemples(provinces):
    baseURL = 'https://th.wikipedia.org'
    response = requests.get(f'{baseURL}https://th.wikipedia.org/wiki/หมวดหมู่:รายชื่อวัดไทย')

    # get all province links
    links = []
    for province in provinces:
        reg = r'<a href="(.*?)" title="รายชื่อวัดในจังหวัด' + f'{province}">'
        match = re.findall(reg, response.text)
        links.append(match[0])

    return list(map(lambda x: f"{baseURL}{x}", links))

def getTempleNames(URL):
    HTML = requests.get(URL).text
    reg = r'<li>.*(?:วัด|สำนัก).*?<(?=[\s\S]*รายชื่อวัดในประเทศไทยแบ่งตามจังหวัด)'     
    finds = re.findall(reg, HTML)

    # pattern = r'[\u0E00-\u0E7F\s]+'
    # pattern = r"[\u0E00-\u0E7F]+[-\s]?[\u0E00-\u0E7F]*"
    # pattern = r"[\u0E00-\u0E7F]+[-\s\d]*[\u0E00-\u0E7F]*"
    pattern = r"[\u0E00-\u0E7F]+[-\s\d]*(?!ตำบล)[\u0E00-\u0E7F]*"
    matches = []
    for find in finds:
        matches.append(re.findall(pattern, find)[0])
    
    if matches[-1] == 'วัดไทย': # เอาตรงเพิ่มเติมออก
        matches.pop()
    return list(dict.fromkeys(list(map(lambda x: x.strip(), matches)))) # remove duplicates

def getDuplicates(listOfTemples):
    from collections import Counter
    counts = Counter(listOfTemples)
    results = []
    for key in counts:
        if counts[key] > 1:
           results.append(key) 
    return results

if __name__ == "__main__":
    URLs = getWikipediaThaiTemples(provinces)
    for idx, URL in enumerate(URLs):
        temples = getTempleNames(URL)
        # print(temples)

        with open(f'{provinces[idx]}.csv', 'w', encoding='UTF8') as f:
            f.write('ชื่อวัด\n')
            for temple in temples:
                f.write(f'{temple}\n')



