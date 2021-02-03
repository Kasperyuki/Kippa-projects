import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def img_down():
    URL = 'https://testbed.fmi.fi/'
    page = requests.get(URL)

    #page_html = page.read()
    soup = BeautifulSoup(page.content, 'html.parser')


    #results = soup.find(onload='anim_start()')
    results = soup.body.find(cellpadding='20')
    #results = soup.body.find()

    page_elems = results.find_all('td')

    #for page_ele in page_elems:
    final_elem = page_elems[1].find('img', class_='animimg')

    
    url_text = f"{final_elem}"
    

    url_all = url_text.split(" ")
    url_img = url_all[6][5:][:-1]
    print(url_img)

    response = requests.get(url_img)
    time = datetime.now()
    fix = timedelta(hours=8, minutes=15)
    real_time = time - fix

    file = open(f"\images\{real_time.strftime('%Y%m%d%H%M')}.png", "wb")
    file.write(response.content)
    file.close()
    #soup_img = BeautifulSoup(page_img.content, 'html.parser')
    #print(soup_img)

    #print(final_elem)
    #print()
    page.close()

def img_down_custom(bday,hour,minute,img_count):
    #URL = 'https://testbed.fmi.fi/'
    #page = requests.get(URL)

    #page_html = page.read()
    #soup = BeautifulSoup(page.content, 'html.parser')


    #results = soup.find(onload='anim_start()')
    #results = soup.body.find(cellpadding='20')
    #results = soup.body.find()

    #page_elems = results.find_all('td')

    #for page_ele in page_elems:
    #final_elem = page_elems[1].find('img', class_='animimg')

    
    #url_text = f"{final_elem}"
    
    url_img = "https://2.img.fmi.fi/php/img.php?A=dA4ndr1aWdr1aW70RXdRUXRLUWd9ULdq1Uqd1qWq1dRU4rU1qR71UdbHhvJvNJNNJNSlJ.r/D"
    months = {1: "JN", 2: "Jv", 3: "JM", 4: "Jz", 5: "JI", 6: "J_", 7: "JS", 8: "JF", 9: "JY", 10: "NJ", 11: "NN", 12: "Nv"}
    days = {1: "JN", 2: "Jv", 3: "JM", 4: "Jz", 5: "JI", 6: "J_", 7: "JS", 8: "JF", 9: "JY", 10: "NJ", 11: "NN", 12: "Nv", 13: "NM", 14: "Nz", 15: "Nl", 16: "N_", 17: "NS", 18: "NF", 19: "NY", 20: "vJ", 21: "vN"}
    hours = {0: "vv", 1: "vM", 2: "JJ", 3: "JN", 4: "Jv", 5: "JM", 6: "Jz", 7: "Jl", 8: "J_", 9: "JS", 10: "JF", 11: "JY", 12: "NJ", 13: "NN", 14: "Nv", 15: "NM", 16: "Nz", 17: "Nl", 18: "N_", 19: "NS", 20: "NF", 21: "NY", 22: "vJ", 23: "vN"}
    mins = {0: "JJ", 5: "Jl", 10: "NJ", 15: "Nl", 20: "vJ", 25: "vl", 30: "MJ", 35: "Ml", 40: "zJ", 45: "zl", 50: "lJ", 55: "ll"}
    
    print(bday[6:8])
    time = datetime(2021, int(bday[4:6]), int(bday[6:8]))
    #day = int(bday[6:8])
    #hour = int(bday[4:6])
    #minute = int(bday[6:8])
    #hour = 0
    #minute = 0
    #day_txt = days[day]
    #hour_txt = hours[hour]
    #min_txt = mins[minute]

    #hour = 0
    #minute = 0

    #if hour == 0:
    #    day = day - 1
    #    day_txt = days[day]
    day = int(bday[6:8])
    kk = int(bday[4:6])
    
    #288
    #for i in range(288):
    for i in range(int(img_count)):
        #hour = int(bday[4:6])
        #minute = int(bday[6:8])
        time = datetime(2021, int(kk), int(int(bday[6:8])), hour, minute)
        if hour == 0 and minute == 0:
            day = day - 1
            day_txt = days[day]
        month_txt = months[kk]
        day_txt = days[day]
        hour_txt = hours[hour]
        min_txt = mins[minute]
        url_end = f"{month_txt}{day_txt}{hour_txt}{min_txt}"
        url_day = f"{url_img[0:96]}{url_end}{url_img[-4:-1]}D"
        #url_all = url_text.split(" ")
        #url_img = url_all[6][5:][:-1]
        print(url_day)

        response = requests.get(url_day)
        

        #time = datetime.now()
        #fix = timedelta(hours=8, minutes=15)
        #real_time = time - fix

        file = open(f"{time.strftime('%Y%m%d%H%M')}.png", "wb")
        #file = open(f"TEST_DOWN_{hour}{minute}.png", "wb")
        file.write(response.content)
        file.close()

        minute += 5
        if minute == 60:
            minute = 0
            hour += 1
            if hour == 2:
                day += 1
        
    #soup_img = BeautifulSoup(page_img.content, 'html.parser')
    #print(soup_img)

    #print(final_elem)
    #print()
    #page.close()

if __name__ == "__main__":
    paiva = input("Mikä päivä (YYYYMMDD): ")
    tunti = int(input("Tunti: "))
    minuutti = int(input("Minuutti: "))
    img_count = int(input("Kuvien määrä (1pv = 288):"))
    img_down_custom(paiva,tunti,minuutti,img_count)
    #img_down()
