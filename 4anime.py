import requests
import re, argparse, sys
from bs4 import BeautifulSoup as bs
from Downloader.DownloaderThreaded import FileDownloader

# initialize some variables
main_url = "https://4anime.to"
show_suffix = "/anime/{0}"
page_suffix = "/page/{0}"

def get_page_soup(url):
	""" Returns a beautifulsoup object from the given url"""
	page = requests.get(url)
	soup = bs(page.content, "html.parser")

	if soup.find("h1", {"class": "page-title"}) is not None:
		print("Show not found")
		exit()

	return soup

def info_printer(info):
	print(f"Title: \t\t {info['title'].replace('-', ' ').capitalize()}")
	print(f"Episodes: \t {info['num_eps']}")
	print(f"Genres: \t {info['genres']}")
	print(f"Type: \t\t {info['details'][0]}")
	print(f"Studio: \t {info['details'][1]}")
	print(f"Release Date: \t {info['details'][2]}")
	print(f"Status: \t {info['details'][3]}")
	print(f"Language: \t {info['details'][4]}")


def get_show_info(show):
	""" Returns the info of a show """
	parsed_show = show.lower()
	show_url = main_url + show_suffix.format(parsed_show)

	info_soup = get_page_soup(show_url)

	genres_string = "" 
	for genres in info_soup.find("div", {"class": "tags-mobile"}).findAll("a"):
		for genre in genres.contents:
			genres_string += f"{genre} "

	details = [] 
	for detail_div in info_soup.find("div", {"class": ["details", "flat-panel"]}).findAll("div", {"class", "detail"}):
		d = ""
		for detail in detail_div.findAll("a"):
			d += f"{detail.contents[0]} "
		details.append(d)
	
	num_of_episodes = len(info_soup.find("ul", {"class": ["episodes", "range", "active"]}).findAll("a"))

	info_printer({"title":show, "num_eps":num_of_episodes, "genres":genres_string, "details":details})
	exit()

def parse_frontpage_title(div):
	""" Gets the title of the recently added or popular of the weeks shows """
	shows = []

	for div in div.findAll("div", {"id": "headerDIV_4"}):
		for link in div.findAll("a"):
			if link.get('id') == "headerA_5":
				alt = link.get('alt')
				if alt is None:
					alt = link.find("img").get('alt')
				name = alt

			if link.get('id') == "headerA_8":
				data = link.contents[0]

		show = "{:<45} {:<20}".format(name, data)
		shows.append(show)
	
	return shows

def get_popular_week(page):
	""" Prints all the shows that contain the search input """
	search_soup = get_page_soup(main_url + page_suffix.format(page))
	popular_div = search_soup.find("div", {"id": "populartodaycontent"})
	popular_shows = parse_frontpage_title(popular_div)

	print(f"Popular this week. Page: {page} \n")
	for s in popular_shows:
		print(s)
	
	exit()

def get_recently_added(page):
	""" Prints all the episode that were recently added """
	search_soup = get_page_soup(main_url + page_suffix.format(page))
	recent_div = search_soup.find("div", {"id": "urcontent"})
	recent_shows = parse_frontpage_title(recent_div)

	print(f"Recently added shows. Page: {page} \n")
	for s in recent_shows:
		print(s)

	exit()

def get_episodes_from_show(show, episode=None):
	""" Download all the episodes from a given show """
	parsed_show = show.lower()
	show_url = main_url + show_suffix.format(parsed_show)

	show_soup = get_page_soup(show_url)

	links = show_soup.find("ul", {"class": ["episodes", "range", "active"]}).findAll("a")
	episode_urls = [l.get('href') for l in links]

	if episode is not None:
		if len(episode_urls) < episode: 
			print("Episode not found")
			exit()

		ep_url = episode_urls[episode - 1]
		download_episode(ep_url)
	else:
		for episode in episode_urls:
			download_episode(episode)

def download_episode(episode_url):
	""" Downloads the episode from the url """
	episode_soup = get_page_soup(episode_url)

	episode_url = episode_soup.find("source").get('src')
	file_name = re.search(r"me(.+)", episode_url).group(1)

	print("downloading episode: " + file_name)
	downloader.get_file(episode_url, file_name)

def get_arguments(args=None):
	""" Returns the arguments from the console """

	parser = argparse.ArgumentParser(description="4anime.to downloader")
	parser.add_argument("-d","--download", nargs="+", help="The show to download")
	parser.add_argument("-i","--info", nargs="+", help="Get Info from a specific show")
	parser.add_argument("-p","--popular", action='store_true', help="Returns the popular show of this week")
	parser.add_argument("-r","--recent", action='store_true', help="Returns the recently added shows of this week")
	parser.add_argument("--page", type=int, default=1, help="A specific page from the popular or recent page, default: 1")
	parser.add_argument("-e","--episode", type=int, help="A specific episode, default: all")
	parser.add_argument("-t","--threads", type= int, default=10, help="Number of maximum threads")

	r = parser.parse_args(args)
	return (r.download, r.info, r.popular, r.recent, r.page, r.episode, r.threads)

if __name__ == "__main__":
	download, info, popular, recent, page, episode, threads = get_arguments(sys.argv[1:])
	
	if popular:
		get_popular_week(page)

	if recent:
		get_recently_added(page)

	if info is not None:
		info = "-".join(info)
		get_show_info(info)
	
	download = "-".join(download)
	downloader = FileDownloader(max_threads=threads)
	get_episodes_from_show(download, episode=episode)
