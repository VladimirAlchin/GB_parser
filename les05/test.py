from bs4 import BeautifulSoup as bs


a = open('f.txt', 'r', encoding='utf-8')
b = a.read()

soup = bs(b, "lxml")
item_list = soup.find_all("div", {"class": "_post"})
for i in item_list:
    post_text = i.find("div", {"class": "wall_post_text"})
    if post_text != None:
        print(post_text.text)
        post_date = i.find("span", {"class": "rel_date"})
        if post_date != None:
            print(post_date.text)
        post_link = i.attrs
        print('https://vk.com/wall' + post_link['data-post-id'])
        photo_link = i.find("div", {"class": 'page_post_sized_thumbs'})
        photo_link_other ='https://vk.com/tokyofashion?z=photo'
        for j in photo_link.find_all('a'):
            try:
                print(photo_link_other + j.attrs['data-photo-id'])
            except:
                break

        post_likes = i.find("a", {"class": "like"}).attrs['data-count']
        print(post_likes)

        post_share = i.find("a", {"class": "share"}).attrs['data-count']
        print(post_share)

        post_views = i.find("div", {"class": "like_views _views"}).text
        print(post_views)






    # post_link = ''
    # post_link_image = []
    # post_like = ''
    # post_repost = ''
    # post_view = ''
