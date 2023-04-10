import requests
import re


provinces = ['พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'อุบลราชธานี']

def getWikipediaThaiTemples(provinces):
    baseURL = 'https://th.wikipedia.org'
    response = requests.get(f'{baseURL}/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%84%E0%B8%97%E0%B8%A2')

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
    return list(dict.fromkeys(matches)) # remove duplicates

def getDuplicates(listOfTemples):
    from collections import Counter
    counts = Counter(listOfTemples)
    results = []
    for key in counts:
        if counts[key] > 1:
           results.append(key) 
    return results

if __name__ == "__main__":
    URLs = getWikipediaThaiTemples(['พัทลุง'])
    temples = getTempleNames(URLs[0])