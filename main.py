import requests
from pprint import pprint

class VkDownloader:
    def __init__(self,token : str):
        self.token = token

    def download(self, vk_id: str):
        """Метод скачивает фотографии с профиля vk_id"""
        p = requests.get(f"https://api.vk.com/method/users.get?{vk_id}&v=5.21&access_token={self.token}")
        params = f"owner_id={p.json()['response'][0]['id']}&album_id=profile&extended=1"
        s = requests.get(f"https://api.vk.com/method/photos.get?{params}&v=5.21&access_token={self.token}")
        pprint(s.json()['response'])


class YaUploader:
  def __init__(self, token: str):
    self.token = token

  def upload(self, file_path: str):
    """Метод загруджает файл file_path на яндекс диск"""
    over_write = '&overwrite=true'
    file_name = file_path.split('\\')[-1]
    stat = requests.get(f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={file_name+over_write}', headers={'Accept': 'application/json', 'Authorization': self.token})
    send_url = stat.json()['href']
    with open(file_path, 'rb') as file:
      requests.put(send_url, data=file, headers={'Accept': 'application/json'})
    return print(f"Файл {file_path} отправлен на Яндекс диск")


if __name__ == '__main__':
    t_ya = 
    t_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    dowloader = VkDownloader(t_vk)
    dowload = dowloader.download('begemot_korovin')
#    uploader = YaUploader(t_ya)
 #   upload = uploader.upload(photos)
