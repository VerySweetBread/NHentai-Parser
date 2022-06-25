from flask import Flask, make_response
from requests import get
from bs4 import BeautifulSoup as Soup

app = Flask(__name__)

@app.route('/<int:hentai_id>')
def index(hentai_id):
    soup = Soup(get(f"https://nhentai.xxx/g/{hentai_id}").text)
    info = soup.find(id="info")
    data = {
            "title": info.find("h1").find("span").text,
        "description": info.find("h2").find("span").text,
        "id": info.find("h3").text,
        "cover": soup.find(id="cover").find("img").attrs['src'].split('/')[-2],
        "data": {}
    }
    info = {i.get_text(separator=".").split('.')[0].replace('\n', ''): i.find("span") for i in info.find(id="tags").find_all("div")}
    if "Tags" in info.keys():
        data["data"]["tags"] =          [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Tags'].find_all('a')]
    if "Artists" in info.keys():
        data["data"]["artists"] =       [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Artists'].find_all('a')]
    if "Languages" in info.keys():
        data["data"]["languages"] =     [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Languages'].find_all('a')]
    if "Parodies" in info.keys():
        data["data"]["parodies"] =      [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Parodies'].find_all('a')]
    if "Characters" in info.keys():
        data["data"]["characters"] =    [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Characters'].find_all('a')]
    if "Groups" in info.keys():
        data["data"]["groups"] =        [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Groups'].find_all('a')]
    if "Categories" in info.keys():
        data["data"]["categories"] =    [{"name": tag.find(class_="name").text, "count": tag.find(class_="count").text} for tag in info['Categories'].find_all('a')]
    data['data']["pages"] =     info["Pages:"].find(class_="name").text
    data["data"]["uploaded"] =  info["Uploaded:"].find(class_="nobold").text

    print(data)

    return data

@app.route('/cover/<int:hentai_id>')
def cover(hentai_id):
    response = make_response(get(f"https://cdn.nhentai.xxx/g/{hentai_id}/cover.jpg").content)
    response.headers.set('Content-Type', 'image/jpeg')
    return response
