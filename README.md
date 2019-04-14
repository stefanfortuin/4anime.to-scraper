# 4anime.to-scraper
A scraper where you can download anime shows from 4anime.to 

# Usage

```
--download / -d Downloads the given show, defaults to downlaod all of the episodes
--info / -i Prints the info of a given show
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

Default file location is the working directory of the script in a created folder called /Downloads
