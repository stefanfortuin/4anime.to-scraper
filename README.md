# WARNING
Since this is a webscraper this can and will break at some point.
Fixes to this won't be actively maintained

# 4anime.to-scraper
A scraper where you can download anime shows from 4anime.to 

# Usage

```
--download / -d Downloads the given show, defaults to downlaod all of the episodes
--info / -i Prints the info of a given show
--popular / -p Prints the popular shows of the week
--recent / -r Prints the recently added shows of the week
--episode / -e Download a specific episode from a show
--threads / -t Specify the amount of threads with which you want to download with
```

# Example

```
python 4anime.py -d high-school-fleet -t 5 / --download high-school-fleet -threads 5
python 4anime.py -d dororo -e 3 / --download dororo --episode 3
```

```
python 4anime.py --info joshikausei / -i joshikausei

Title:           Joshikausei
Episodes:        2
Genres:          Comedy School Slice of Life
Type:            TV Series
Studio:          Seven
Release Date:    Spring 2019
Status:          Currently Airing
Language:        Subbed
```

```
python 4anime.py -r 3

Recently added shows. Page: 3

Chou Kadou Girl ⅙: Amazing Stranger           Episode 02
Cardfight!! Vanguard (2018)                   Episode 49
Detective Conan                               Episode 936
Mix: Meisei Story                             Episode 02
Hitoribocchi no Marumaru Seikatsu             Episode 02
Midara na Ao-chan wa Benkyou ga Dekinai       Episode 02
Senryuu Shoujo                                Episode 02
```

Default file location is the working directory of the script in a created folder called /Downloads
