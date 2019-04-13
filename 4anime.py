import requests
import re, argparse, sys
from bs4 import BeautifulSoup as bs
from Downloader.DownloaderThreaded import FileDownloader

# initialize some variables
main_url = "https://4anime.to"
show_suffix = "/anime/{0}"

def get_page_soup(url):
	""" Returns a beautifulsoup object from the given url"""
	page = requests.get(url)
	soup = bs(page.content, "html.parser")
	return soup

def get_all_episodes_from_show(show):
	""" Download all the episodes from a given show """

	# Build the show url
	parsed_show = show.lower().replace(" ", "-")
	show_url = main_url + show_suffix.format(parsed_show)

	# Get the show page
	show_soup = get_page_soup(show_url)

	# Acquire all the episode urls from the show page
	links = show_soup.find("ul", {"class": ["episodes", "range", "active"]}).findAll("a")
	episode_urls = [l.get('href') for l in links]

	for i, episode in enumerate(episode_urls):
		print("downloading episode: " + str(i))
		download_episode(episode)

def get_one_episode_from_show(show, episode):
	""" Download a specific episode from a show."""
	# Build the show url
	show_url = main_url + show_suffix.format(show)

	# Get the show page
	show_soup = get_page_soup(show_url)

	# Acquire the episode url from the show page
	array_index = int(episode) - 1
	links = show_soup.find("ul", {"class": ["episodes", "range", "active"]}).findAll("a")
	episode_url = links[array_index].get('href')
	
	print("downloading episode: " + episode)
	download_episode(episode_url)

def download_episode(episode_url):
	""" Downloads the episode from the url """

	episode_page = requests.get(episode_url)
	episode_soup = bs(episode_page.content, "html.parser")

	episode_url = episode_soup.find("source").get('src')
	file_name = re.search(r"me(.+)", episode_url).group(1)

	downloader.get_file(episode_url, file_name)

def get_arguments(args=None):
	""" Returns the arguments from the console """

	parser = argparse.ArgumentParser(description="4anime.to downloader")
	parser.add_argument("--show", help="The show to download")
	parser.add_argument("--episode", help="A specific episode, default: all")
	parser.add_argument("--threads", help="Number of maximum threads")

	results = parser.parse_args(args)
	return (results.show,
			results.episode,
			results.threads)

if __name__ == "__main__":
	show, episode, threads = get_arguments(sys.argv[1:])

	if threads is None:
		downloader = FileDownloader()
	else:
		downloader = FileDownloader(max_threads=int(threads))
	
	if episode is None:
		get_all_episodes_from_show(show)
	else:
		get_one_episode_from_show(show, episode)
