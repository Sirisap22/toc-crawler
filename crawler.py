import requests
import re

class TemplesCrawler:
    
    def __init__(self):
        self.baseURL = 'https://th.wikipedia.org'
        self.indexPage = requests.get(f'{self.baseURL}/wiki/หมวดหมู่:รายชื่อวัดไทย').text
        self.provinces = ['พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'อุบลราชธานี']
        self.temples = {}
        self.initTemplesByProvinces()
    
    def initTemplesByProvinces(self):
        URLs = self.getWikipediaThaiTemplesLinks()
        for URL, province in zip(URLs, self.provinces):
            temples = self.getTempleNames(URL)
            self.temples[province] = temples
        
    
    def saveToCSV(self, province):
        if (province not in self.provinces):
            return
        with open(f'{province}.csv', 'w', encoding='UTF8') as f:
            f.write('ชื่อวัด\n')
            for temple in self.temples[province]:
                f.write(f'{temple}\n')
        

    def getWikipediaThaiTemplesLinks(self):
        reg = r'<a href="(.*?)" title="รายชื่อวัดในจังหวัด(พังงา|พัทลุง|พิจิตร|พิษณุโลก|อุบลราชธานี)">'
        matches = re.findall(reg, self.indexPage)
        links = list(map(lambda match: f"{self.baseURL}{match[0]}", matches))

        return links
    
    def getTempleNames(self, URL):
        HTML = requests.get(URL).text
        reg = r'<li>.*(?:วัด|สำนัก).*?<(?=[\s\S]*รายชื่อวัดในประเทศไทยแบ่งตามจังหวัด)'  
        finds = re.findall(reg, HTML)

        pattern = r'[\u0E00-\u0E7F]+[-\s\d]*(?!ตำบล)[\u0E00-\u0E7F]*'
        matches = []
        for find in finds:
            matches.append(re.findall(pattern, find)[0])
        
        if matches[-1] == 'วัดไทย': # เอาตรงเพิ่มเติมออก
            matches.pop()
        return list(dict.fromkeys(list(map(lambda x: x.strip(), matches)))) # remove duplicates

if __name__ == "__main__":
    crawler = TemplesCrawler()
    print(crawler.temples.keys())
    print(crawler.temples['พิจิตร'])