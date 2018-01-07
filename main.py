from bs4 import BeautifulSoup
import requests
from sanic import Sanic
from sanic.response import json

def get_trending(language=""):
	html = requests.get(f'https://github.com/trending/{language}').text
	# with open("trending.html") as f:
	# 	html = "".join(f.readlines()).replace("\n","")
	soup = BeautifulSoup(html, 'html.parser')
	repos = []
	for el in soup.find_all("li", class_="border-bottom"):
		title = el.contents[1].find("a").get_text().replace(" ", "").replace("\n", "")
		url = f'https://github.com{el.contents[1].find("a").get("href")}'
		stars = el.find("a", class_="d-inline-block").contents[2].strip()
		description = el.find("p", class_="text-gray").get_text().strip()
		try:
			language = el.find(itemprop="programmingLanguage").get_text().strip()
			repos.append({
				"title": title,
				"url": url,
				"stars": stars,
				"description": description,
				"language": language
			})
		except:
			continue
	return repos

app = Sanic()

@app.route("/")
async def trending(request):
	try:
		repos = get_trending()
		return json(repos)
	except Exception as e:
		return json({"message": e}, status=501)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)