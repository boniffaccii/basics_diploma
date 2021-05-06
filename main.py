import requests
from pathlib import Path
import datetime
import json
import os


class VkDownloader:
    def __init__(self, token: str):
        self.token = token

    def save_photo(self, photos: dict):
        res_dic = {}
        photo_sizes = ['w', 'z', 'y', 'r', 'x', 'm', 's']
        check = photos.get('filename')

        if Path(f"./download/{check}.jpg").exists():
            photos.update({'filename': f"{check}_{datetime.date.today()}"})
        for size in photo_sizes:
            if photos.get(size, False):
                with open(f"./download/{photos.get('filename')}.jpg", 'wb') as f:
                    photo = requests.get(photos.get(size))
                    f.write(photo.content)
                res_dic.update({'file_name': f"{photos.get('filename')}.jpg"})
                res_dic.update({'size': f"{size}"})
                t = open(f"./download/{photos.get('filename')}.json", 'w')
                t.close()
                with open(f"./download/{photos.get('filename')}.json", 'r+') as r:
                    try:
                        data = json.loads(r)
                    except:
                        data = []
                        json.dump(data, r)
                data.append(res_dic)
                with open(f"./download/{photos.get('filename')}.json", 'w') as r:
                    json.dump(data, r)
                break

    def download(self, vk_id: str):
        """Метод скачивает фотографии с профиля vk_id"""
        p = requests.get(f"https://api.vk.com/method/users.get?{vk_id}&v=5.21&access_token={self.token}")
        params = f"owner_id={p.json()['response'][0]['id']}&album_id=profile&extended=1&photo_sizes=1"
        s = requests.get(f"https://api.vk.com/method/photos.get?{params}&v=5.21&access_token={self.token}")
        items_return = s.json()['response']['items']
        m = 1
        for item in items_return:
            filename = item['likes']['count']
            photo_items = {}
            photo_items.update({'filename' : filename})
            for size in item['sizes']:
                photo_items.update({size['type'] : size['src']})

            print(f"Нашли фото {m}")
            self.save_photo(photo_items)
            print(f"Скачали фото {m}")
            m += 1



class YaUploader:
  def __init__(self, token: str, g=5):
    self.token = token
    self.g = g

  def upload(self):
    """Метод загруджает файлы на яндекс диск"""
    wdir = 'download'
    disk_dir = f"upload_{datetime.date.today()}"
    requests.put(f"https://cloud-api.yandex.net/v1/disk/resources?path={disk_dir}",
                              headers={'Accept': 'application/json', 'Authorization': self.token,
                                       'Content-Type': 'application/json'})
    a = os.listdir(f"./{wdir}")
    k = 1
    u = 0
    print('Загружаем фотографии на Я.Диск')
    print('Количество загружаемых фото ' + str(self.g))
    for file in a:
        if '.jpg' in file and u < self.g:
            print(f"Загружаем фотографию {k}")
            file_name = f"./{wdir}/{file}"
            stat = requests.get(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={disk_dir}/{file}",
                                headers={'Accept': 'application/json', 'Authorization': self.token})
            send_url = stat.json()['href']
            with open(file_name, 'rb') as fi:
                requests.put(send_url, data=fi, headers={'Accept': 'application/json'})
            k += 1
            u += 1


if __name__ == '__main__':

    t_ya = ''
    t_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    dowloader = VkDownloader(t_vk)
    dowload = dowloader.download('begemot_korovin')
    uploader = YaUploader(t_ya, 3)
    upload = uploader.upload()

