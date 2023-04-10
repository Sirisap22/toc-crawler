import requests
import re

class TemplesCrawler:
    
    def __init__(self):
        self.baseURL = 'https://th.wikipedia.org'
        self.indexPage = requests.get(f'{self.baseURL}/wiki/%E0%B8%AB%E0%B8%A1%E0%B8%A7%E0%B8%94%E0%B8%AB%E0%B8%A1%E0%B8%B9%E0%B9%88:%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%84%E0%B8%97%E0%B8%A2').text
        self.provinces = ['พังงา', 'พัทลุง', 'พิจิตร', 'พิษณุโลก', 'อุบลราชธานี']
        self.temples = {}
        self.initTemplesByProvinces()
    
    def initTemplesByProvinces(self):
        for province in self.provinces:
            URL = self.getWikipediaThaiTemplesLink(province)
            temples = self.getTempleNames(URL)
            self.temples[province] = temples
        
    
    def saveToCSV(self, province):
        if (province not in self.provinces):
            return
        with open(f'{province}.csv', 'w', encoding='UTF8') as f:
            f.write('ชื่อวัด\n')
            for temple in self.temples[province]:
                f.write(f'{temple}\n')
        

    def getWikipediaThaiTemplesLink(self, province):
        reg = r'<a href="(.*?)" title="รายชื่อวัดในจังหวัด' + f'{province}">'
        match = re.findall(reg, self.indexPage)
        link = match[0]

        return f"{self.baseURL}{link}"
    
    def getTempleNames(self, URL):
        HTML = requests.get(URL).text
        reg = r'<li>.*(?:วัด|สำนัก).*?<(?=[\s\S]*รายชื่อวัดในประเทศไทยแบ่งตามจังหวัด)'  
        finds = re.findall(reg, HTML)

        pattern = r'[\u0E00-\u0E7F]+'
        matches = []
        for find in finds:
            matches.append(re.findall(pattern, find)[0])
        
        if matches[-1] == 'วัดไทย': # เอาตรงเพิ่มเติมออก
            matches.pop()
        return list(dict.fromkeys(matches)) # remove duplicates

if __name__ == "__main__":
    crawler = TemplesCrawler()
    print(crawler.temples.keys())
    print(crawler.temples['พิจิตร'])