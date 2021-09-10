from datetime import datetime
from bs4 import BeautifulSoup
from typing import Collection
from pandas import DataFrame
import requests
import csv
import sys
import os
# Hem temiz bir başlangıç hem de yeniden başlatmalarda Press any key.. mesajını kaldırmak için.
os.system('cls')


def signature(x):
    try:
        if x == True:
            if w_filter and filter_empty_items < 3:
                print(
                    f'\nUser: {user_name}\nList: {list_name}\nFiltre uygulaması: Var\n---- Filtreler;\n{msg_decadeyear}{msg_genre}{msg_sortby}')
            else:
                print(
                    f'\nUser: {user_name}\nList: {list_name}\nFiltre uygulaması: Yok\n')
        else:
            print(
                f'\nFilename: {csv_name}\nFilm sayısı: {dongu_no-1}\nTüm filmler {csv_name + " dosyasına"} aktarıldı.')
        log = 'İmza yazdırma işlemleri tamamlandı.'
    except:
        print('İmza seçimi başarısız.')
        log = 'İmza yüklenemedi. Program yine de devam etmeyi deneyecek.'
    finally:
        logging(log)


def rst():
    try:
        os.system('echo Press and any key to reboot & pause >nul')
        os.system('echo Confirm reboot press any key again & pause >nul')
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    except:
        log = 'Programın yeniden başlatılmaya çalışılması başarısız.'
        print(log)
        logging(log)


def dir_check(l, e):
    # l= logdir_name, e = exdir_name
    # Log Dir
    if os.path.exists(l):
        logging(f'{l} klasörü halihazırda var.')
    else:
        os.makedirs(l)
        logging(f'{l} klasörü oluşturuldu')
        # Oluşturulmaz ise bir izin hatası olabilir
    # Exports Dir
    if os.path.exists(e):
        logging(f'{e} klasörü halihazırda var.')
    else:
        os.makedirs(e)
        logging(f'{e} klasörü oluşturuldu')
        # Oluşturulmaz ise bir izin hatası olabilir


def countrooms(r_article):
    try:
        data_count = 0
        for rooms in r_article:
            data_count += 1
        return data_count
    except:
        print('Sayım işlemi başarısız.')


def logging(r_message):
    try:
        f = open(f'{logdir_name}/{csv_name}.txt', "a")
        f.writelines(f'{r_message}\n')
        f.close()
    except:
        print('Loglama işlemi başarısız.')


def f_filmsayisi(r_lastPage_No):
    try:
        # > Son sayfaya bağlanmak için bir ön hazırlık.
        lastsoup = readpage(f'{url}{r_lastPage_No}')
        # > Sayfa kodları çekildi.
        lastarticles = lastsoup.find('ul', attrs={
            'class': 'poster-list -p70 film-list clear film-details-list'}).find_all("li")
        lastpage_fcount = countrooms(lastarticles)
        # < Film sayısı öğrenildi.
        # > Toplam film sayısını belirlemek.
        film_sayisi = ((int(r_lastPage_No)-1)*100)+lastpage_fcount
        logging(f"{csv_name} Bilgi: Film sayısı {film_sayisi} olarak bulunmuştur.")
        return film_sayisi
    except:
        print('Film sayısını elde ederken hata.')


def readpage(r_url):
    try:
        page_url = requests.get(r_url)
        # > Sayfa kodları çekildi.
        soup = BeautifulSoup(page_url.content.decode('utf-8'), 'html.parser')
        logging(f'{csv_name} Connect to: {r_url}')
        return soup
    except:
        print('Sayfa okunurken bir hata oluştu.')


def pullfilms(r_count, r_soup):
    try:
        # > Çekilen sayfa kodları, bir filtre uygulanarak daraltıldı.
        articles = r_soup.find('ul', attrs={
            'class': 'poster-list -p70 film-list clear film-details-list'}).find_all("li")
        dongu_no = r_count
        for rooms in articles:
            # Oda ismini çektik
            film = rooms.find(
                'h2', attrs={'class': 'headline-2 prettify'})
            film_adi = film.find('a').text
            # Film yılı bazen boş olabiliyor. Önlem alıyoruz"
            try:
                film_yili = film.find('small').text
            except:
                film_yili = "Yok"
            # Her seferinde Csv dosyasına çektiğimiz bilgileri yazıyoruz.
            print(f'{dongu_no}) {film_adi} ({film_yili})')
            writer.writerow(
                [str(dongu_no), str(film_adi), str(film_yili)])
            dongu_no += 1
        return dongu_no
    except:
        print('Film bilgilerini elde ederken bir hatayla karşılaşıldı.')


# > Kullanıcı eğer domainden değilde direkt olarak girerse yazıyı küçültüyoruz.
user_name = str(input("Username(Not display name): ")).lower()
list_name = str(input("Listname(Domain): ")).lower()

# > Dosya çakışma sorunları için farklı isimler ürettik.
zaman = datetime.now().strftime('%d%m%Y%H%M')
csv_name = f"{user_name}-({zaman})"
logdir_name = "logs"
exdir_name = "exports"
# Gerekli klasörlerin kontrolü
dir_check(logdir_name, exdir_name)
# > Domain'in parçalanması
main_protocol = "https://"
site_url = "letterboxd.com"
domain = main_protocol + site_url
mini_url = f'{domain}/{user_name}/list/{list_name}'
# Filter req
while True:
    filter_yn = input(f"Listeye filtre uygulanacak mı?: [Y/N]").lower()
    if filter_yn == "y":
        w_filter = True
        logging('Listeye filtre uygulanacak.')
        # filters
        filter_empty_items = 0
        # Year
        while True:
            decadeyear_dory = input(
                f"Want Decade or Year filter?: [D/Y/N]").lower()
            if decadeyear_dory == "d":
                i_decadeyear = input(f"Decade:")
                msg_decadeyear = f':Decader: {i_decadeyear}\n'
                w_decadeyear = f"/decade/{i_decadeyear}s"
                decadeyear_confirm = True
            elif decadeyear_dory == "y":
                i_decadeyear = input(f"Year: ")
                msg_decadeyear = f'Year: {i_decadeyear}\n'
                w_decadeyear = f"/year/{i_decadeyear}"
                decadeyear_confirm = True
            elif decadeyear_dory == "n":
                w_decadeyear = ''
                msg_decadeyear = ''
                print('Decade veya year filtresi uygulanmayacak.')
                filter_empty_items = 1
                decadeyear_confirm = True
            else:
                print("Anlaışlmadı. Tekrar deneeyin.")
                decadeyear_confirm = False
            # decade ve year işlemleri tamamsa çıkalım
            if decadeyear_confirm:
                break
        # Genre
        while True:
            genre_dory = input(f"Want genre filter?: [Y/N]").lower()
            if genre_dory == "y":
                i_genre = input(f"Genre: ")
                msg_genre = f'Genre: {i_genre}\n'
                w_genre = f"/genre/{i_genre}"
                genre_confirm = True
            elif genre_dory == "n":
                w_genre = ''
                msg_genre = ''
                print('Genre filtresi uygulanmayacak.')
                filter_empty_items += 1
                genre_confirm = True
            else:
                print("Anlaşılmadı. Tekrar deneyin.")
                genre_confirm = False
            if genre_confirm:
                break
        # Sory By
        while True:
            sortby_dory = input(f"Want Sort By filter?: [Y/N]").lower()
            if sortby_dory == "y":
                i_sortby = input(f"Sort By: ")
                msg_sortby = f'Sort By: {i_sortby}\n'
                w_sortby = f"/by/{i_sortby}"
                sortby_confirm = True
            elif sortby_dory == "n":
                w_sortby = ''
                msg_sortby = ''
                print('Sort By filtresi uygulanmayacak.')
                filter_empty_items += 1
                sortby_confirm = True
            else:
                sortby_confirm = False
                print("Anlaışlmadı. Tekrar deneyin.")
            if sortby_confirm:
                break
        # Filtre elemanları bittikten sonra while için filtre onayı
        filter_confirm = True
    # Filtre istemezse
    elif filter_yn == "n":
        w_filter, w_decadeyear, w_genre, w_sortby = False, "", "", ""
        filter_confirm = True
        logging('Listeye filtre uygulanmayacak.')
    # Filtre isteyip istemediği anlaşılmayınca
    else:
        filter_confirm = False
        print("Tam anlayamadık? Tekrar deneyin.")
        logging('Kullanıcı soruya cevap veremedi.')
    # While döngüsünden çıkmak için.
    if filter_confirm:
        break


all_filtres = f'{w_decadeyear}{w_genre}{w_sortby}'
logging(f'Uygulanan filtre: {all_filtres}')
url = f'{mini_url}/detail{all_filtres}/page/'
# Kontrol print(f'Kontrol: {all_filtres}\nKontrol: {url}')
# > Domain'in doğru olup olmadığı kullanıcıya sorulur,
# > doğruysa kullanıcı enter'a basar ve program verileri çeker.
signature(1)
logging(f'{csv_name} Bilgi: Karlışama imzası yazıldı')
ent = input(
    f"Link: {mini_url}\n> Press enter to confirm the entered information. (Enter)\n").lower()

if ent == "":
    # > Burada mini_url ile liste sayfa sayısını elde ediyoruz ve aşağısında film toplamı sayısını hesaplıyoruz
    logging('Saf sayfaya erişim başlatılıyor.')
    soup = readpage(mini_url)
    try:
        # > Not: Sayfa sayısını bulmak için li'leri sayma. Son sayıyı al.
        # > Son'linin içindeki bağlantının metnini çektik. Bu bize kaç sayfalı bir listemiz olduğunuz verecek.
        logging('Bilgi: Listedeki sayfa sayısı denetleniyor..')
        lastPage_No = soup.find(
            'div', attrs={'class': 'paginate-pages'}).find_all("li")[-1].a.text
        logging(
            f'Bilgi: Liste birden çok sayfaya {lastPage_No} sayfaya sahiptir.')
        f_filmsayisi(lastPage_No)
    except:
        # > Listede 100 ve 100'den az film sayısı olduğunda sayfa sayısı için bir link oluşturulmaz.
        lastPage_No = 1
        f_filmsayisi(lastPage_No)
        logging('Bilgi: Birden fazla sayfa yok, bu liste tek sayfadır.')
    finally:
        logging(
            f'Saf sayfa ile iletişim tamamlandı. Listedeki sayfa sayısının {lastPage_No} olduğu öğrenildi.')

    # Konumda klasör yoksa dosya oluşturmayacaktır.
    with open(f'{exdir_name}/{csv_name}.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Sıra", "Filmİsmi", "YayınYılı"])
        # Filmleri çekiyoruz
        dongu_no = 1
        for x in range(int(lastPage_No)):
            logging(f'{csv_name} Connecting to: {url}{str(x+1)}')
            current_soup = readpage(f'{url}{str(x+1)}')
            dongu_no = pullfilms(dongu_no, current_soup)
        # Açtığımız dosyayı manuel kapattık
        file.close()
    logging(f'{csv_name} Success!')
    signature(0)
    rst()
else:
    cancel_log = "Bilgileri doğrulamadığınız için oturum iptal edildi."
    print(cancel_log)
    logging(cancel_log)
    rst()
