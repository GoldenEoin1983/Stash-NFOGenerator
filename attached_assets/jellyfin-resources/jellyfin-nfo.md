# Jellyfin NFO

# Local .nfo metadata

Jellyfin can read and write local .nfo metadata files to import or export metadata from and to other programs and tools.

## Naming .nfo files[​](#naming-nfo-files "Direct link to Naming .nfo files")

In order for Jellyfin to find the .nfo files, you have to name them correctly. The table below will help you name them.

| Media Type | Filename |
| --- | --- |
| Movies | `movie.nfo`, `VIDEO_TS.nfo` or for DVDs `<filename of the movie>.nfo` |
| TV Shows | `tvshow.nfo` |
| TV Season | `season.nfo` |
| Episode | `<filename of the episode>.nfo` |
| Music Artist | `artist.nfo` |
| Music Album | `album.nfo` |
| Music Video | see Movies |

## Reading metadata from .nfo files[​](#reading-metadata-from-nfo-files "Direct link to Reading metadata from .nfo files")

Jellyfin supports a common set of .nfo metadata tags. The following list may not be exhaustive.

caution

If there are multiple tags that map to the same internal Jellyfin data like `plot` and `review`, the last of these tags in the file will have priority.

note

It's currently not possible to disable .nfo metadata. Local metadata will always be fetched and has priority over remote metadata providers like TMDb.

note

User data importing is only possible for a single user. This user can be set in the .nfo settings.

| Tag | Note |
| --- | --- |
| name |  |
| title | same as name |
| localtitle | same as name |
| dateadded |  |
| originaltitle |  |
| sortname |  |
| criticrating |  |
| sorttitle |  |
| plot |  |
| biography | same as plot |
| review | same as plot |
| language |  |
| watched | please see the note about user data |
| playcount | please see the note about user data |
| lastplayed | please see the note about user data |
| countrycode |  |
| lockedfields |  |
| tagline |  |
| country |  |
| mpaa |  |
| customrating |  |
| runtime |  |
| aspectratio |  |
| lockdata |  |
| studio | multiple tags allowed |
| director | multiple tags allowed |
| credits | multiple tags allowed |
| writer | multiple tags allowed |
| actor | multiple tags allowed |
| trailer | kodi format |
| displayorder |  |
| year |  |
| rating | same as customrating |
| ratings | multiple child tags allowed; name attribute of each tag will specify wheter the rating is critics or community rating |
| aired |  |
| formed |  |
| premiered |  |
| releasedate |  |
| enddate |  |
| genre | multiple tags allowed. These tags will be ignored for music albums and music artists. |
| tag | multiple tags allowed |
| style | multiple tags allowed |
| fileinfo |  |
| uniqueid | type attribute specifies id provider |
| thumb | please see the [section about images](#image-paths-and-urls-in-nfo-files) |
| fanart | please see the [section about images](#image-paths-and-urls-in-nfo-files) |

Provider id tags are supported as well if they follow the scheme: `<PROVIDER_NAME`+ `id>`.

You can also use your .nfo files to help Jellyfin identify your media. You can just enter an IMDb, TMDb or TVDb link, to link the media to the specific provider id.

For more information about .nfo files, please also see the [Kodi wiki](https://kodi.wiki/view/NFO_files).

## Image paths and URLs in .nfo files[​](#image-paths-and-urls-in-nfo-files "Direct link to Image paths and URLs in .nfo files")

There are some small caveats to keep in mind when using .nfo files for your images.

* Jellyfin supports only one image for each artwork type. This means that only the first `thumb` tag for each artwork type is used.
* Artwork defined in .nfo files with local paths or URLs have priority over remote image providers and images in the media folders.