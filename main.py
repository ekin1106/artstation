import re
import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

class art():
    def __init__(self,url):
        self.url = url

    def get_pro(self):
        '''得到trending里所有的作品链接,返回列表'''
        req = requests.session()
        web = req.get(self.url).json()
        author_page = web['data']
        p_link = []
        for author_get_link in author_page:
            link = author_get_link['permalink']
            re_link = re.search(r'.*/artwork/(.*)',link)
            project_link = 'https://www.artstation.com/projects/{}.json'.format(re_link.group(1))
            p_link.append(project_link)
        return p_link

    def save_img(self,pro_link):
        req = requests.session()
        web = req.get(pro_link).json()
        assets = web['assets']
        image_url = []
        for i in assets:
            i = i['image_url']
            print(i)
            image_url.append(i)
        return image_url

    def down(self,all_link):
        req = requests.session()
        try:
            f_name = re.search(r'[a-zA-z]*://cdn\w.artstation.com/p/assets/images/images/+\d+/\d+/\d+/large/+(.*.jpg)+.*',all_link)
            f_name = f_name.group(1)
            pic = req.get(all_link).content
            with open(f_name,'wb') as f:
                f.write(pic)
                f.close()
        except:
            pass

if __name__ == '__main__':
    url = 'https://www.artstation.com/projects.json?page=0&sorting=trending'
    art = art(url)
    album_p = art.get_pro()
    pool = ThreadPool(10)
    all_save = pool.map(art.save_img, album_p)
    pool.close()
    pool.join()
    all_pic_link = []
    for i_link in all_save:
        '''将all_save中的列表extend到一个列表中'''
        for img_link in i_link:
            all_pic_link.append(img_link)
    print(all_pic_link)
    pool = ThreadPool(10)
    pool.map(art.down,all_pic_link)
    pool.close()
    pool.join()
