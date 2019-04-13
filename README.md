# 4anime.to-scraper
A scraper where you can download anime shows from 4anime.to 

# Usage

```
--show show name with dashes in between
--info show name with dashes in between
--episode defaults to all of them
--threads specify the amount of threads
```

# Example

```
python 4anime.py --show high-school-fleet --threads 5
python 4anime.py --show dororo --episode 3
```

```
python 4anime.py --info joshikausei

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
