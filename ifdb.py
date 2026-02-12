"""
IFDB (Internet Fanedit Database) Scraper for Kodi
Scrapes movie metadata from fanedit.org using Google Custom Search API
"""

import json
import re
import sys
import urllib.parse
import urllib.request
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')


def log(msg, level=xbmc.LOGDEBUG):
    """Log a message to the Kodi log"""
    xbmc.log(f'[{ADDON_ID}]: {msg}', level=level)


def get_params():
    """Parse plugin parameters from sys.argv"""
    params = {}
    if len(sys.argv) > 2:
        params_str = sys.argv[2]
        if params_str:
            param_string = params_str[1:]  # Remove leading '?'
            if param_string:
                params = dict(urllib.parse.parse_qsl(param_string))
    return params


def search_movie(title, year, handle):
    """
    Search for movies using Google Custom Search API
    
    Args:
        title: Movie title to search for
        year: Release year (optional)
        handle: Kodi plugin handle
    """
    log(f"Searching for: {title} ({year})", xbmc.LOGINFO)
    
    # Get API credentials from settings
    api_key = ADDON.getSetting('api_key')
    search_engine_id = ADDON.getSetting('search_engine_id')
    
    if not api_key or not search_engine_id:
        log("API credentials not configured", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            "IFDB Scraper Error",
            "Please configure API credentials in addon settings",
            xbmcgui.NOTIFICATION_ERROR
        )
        return
    
    # Build search query
    search_query = title
    if year:
        search_query = f"{title} {year}"
    
    # URL encode the query
    encoded_query = urllib.parse.quote(search_query)
    
    # Build API URL
    api_url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?key={api_key}"
        f"&cx={search_engine_id}"
        f"&q={encoded_query}"
    )
    
    log(f"API URL: {api_url}", xbmc.LOGDEBUG)
    
    try:
        # Fetch search results
        with urllib.request.urlopen(api_url, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if 'items' not in data:
            log("No search results found", xbmc.LOGINFO)
            return
        
        # Process search results
        for item in data['items']:
            item_title = item.get('title', '')
            item_url = item.get('link', '')
            
            # Only include results from fanedit.org
            if 'fanedit.org' not in item_url:
                continue
            
            # Create list item
            listitem = xbmcgui.ListItem(item_title, offscreen=True)
            
            # Set URL for getdetails action
            url = f"?action=getdetails&url={urllib.parse.quote(item_url)}"
            
            # Add to results
            xbmcplugin.addDirectoryItem(
                handle=handle,
                url=url,
                listitem=listitem,
                isFolder=True
            )
    
    except urllib.error.HTTPError as e:
        log(f"HTTP Error: {e.code} - {e.reason}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            "IFDB Scraper Error",
            f"API request failed: {e.reason}",
            xbmcgui.NOTIFICATION_ERROR
        )
    except Exception as e:
        log(f"Error searching: {str(e)}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            "IFDB Scraper Error",
            f"Search failed: {str(e)}",
            xbmcgui.NOTIFICATION_ERROR
        )


def get_details(url, handle):
    """
    Get movie details from fanedit.org page
    
    Args:
        url: URL of the fanedit.org page
        handle: Kodi plugin handle
    """
    log(f"Getting details from: {url}", xbmc.LOGINFO)
    
    try:
        # Fetch page content
        req = urllib.request.Request(url)
        # Use generic User-Agent that works across Kodi versions
        req.add_header('User-Agent', 'Kodi (https://kodi.tv)')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        
        # Create list item
        listitem = xbmcgui.ListItem(offscreen=True)
        infotag = listitem.getVideoInfoTag()
        infotag.setMediaType('movie')
        
        # Extract title
        title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if title_match:
            title = title_match.group(1).strip()
            infotag.setTitle(title)
            log(f"Title: {title}", xbmc.LOGDEBUG)
        
        # Extract plot/synopsis
        plot_match = re.search(
            r'<div class="jrBriefsynopsis jrFieldRow">[\s\S]*?<div class="jrFieldValue">(.*?)</div>',
            html,
            re.DOTALL
        )
        if plot_match:
            plot = re.sub(r'<[^>]+>', '', plot_match.group(1))  # Strip HTML tags
            plot = plot.strip()
            infotag.setPlot(plot)
            log(f"Plot: {plot[:50]}...", xbmc.LOGDEBUG)
        
        # Extract year
        year_match = re.search(
            r'<div class="jrFaneditreleasedate jrFieldRow">[\s\S]*?<div class="jrFieldValue">[\s\S]*?([0-9]{4})',
            html
        )
        if year_match:
            year = int(year_match.group(1))
            infotag.setYear(year)
            log(f"Year: {year}", xbmc.LOGDEBUG)
        
        # Extract genres
        genre_section_match = re.search(
            r'<div class="jrGenre jrFieldRow">[\s\S]*?<ul class="jrFieldValueList">(.*?)</ul>',
            html,
            re.DOTALL
        )
        if genre_section_match:
            genre_html = genre_section_match.group(1)
            genres = re.findall(r'<li><a[^>]*>([^<]+)</a></li>', genre_html)
            if genres:
                infotag.setGenres(genres)
                log(f"Genres: {', '.join(genres)}", xbmc.LOGDEBUG)
        
        # Extract directors (faneditors)
        director_section_match = re.search(
            r'<div class="jrFaneditorname jrFieldRow">[\s\S]*?<ul class="jrFieldValueList">(.*?)</ul>',
            html,
            re.DOTALL
        )
        if director_section_match:
            director_html = director_section_match.group(1)
            directors = re.findall(r'<li><a[^>]*>([^<]+)</a></li>', director_html)
            if directors:
                infotag.setDirectors(directors)
                log(f"Directors: {', '.join(directors)}", xbmc.LOGDEBUG)
        
        # Extract rating
        rating_match = re.search(
            r'<span[^>]*>Rating:[\s]*([\d.]+)[\s]*/[\s]*10',
            html
        )
        if rating_match:
            rating = float(rating_match.group(1))
            infotag.setRating(rating)
            log(f"Rating: {rating}", xbmc.LOGDEBUG)
        
        # Extract votes
        votes_match = re.search(
            r'<span[^>]*>\(([0-9]+)[\s]*votes?\)</span>',
            html
        )
        if votes_match:
            votes = int(votes_match.group(1))
            # Note: Kodi's InfoTagVideo doesn't have a dedicated votes field for user ratings
            # The rating is stored above with setRating() which is the primary metadata
            log(f"Votes: {votes}", xbmc.LOGDEBUG)
        
        # Extract tagline
        tagline_match = re.search(
            r'<li><strong>Tagline:</strong>[\s]*([^<]+)</li>',
            html
        )
        if tagline_match:
            tagline = tagline_match.group(1).strip()
            infotag.setTagLine(tagline)
            log(f"Tagline: {tagline}", xbmc.LOGDEBUG)
        
        # Extract thumbnail/poster
        thumb_match = re.search(
            r'<div class="jrListingMainImage">[\s\S]*?<a href="([^"]+)"[^>]*class="fancybox"',
            html
        )
        if thumb_match:
            thumb_url = thumb_match.group(1)
            listitem.setArt({'thumb': thumb_url, 'poster': thumb_url})
            log(f"Thumbnail: {thumb_url}", xbmc.LOGDEBUG)
        
        # Add the item
        xbmcplugin.addDirectoryItem(
            handle=handle,
            url=url,
            listitem=listitem,
            isFolder=False
        )
    
    except Exception as e:
        log(f"Error getting details: {str(e)}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            "IFDB Scraper Error",
            f"Failed to get details: {str(e)}",
            xbmcgui.NOTIFICATION_ERROR
        )


def main():
    """Main entry point for the scraper"""
    log(f"IFDB Scraper called with args: {sys.argv}", xbmc.LOGDEBUG)
    
    params = get_params()
    action = params.get('action', '')
    
    handle = int(sys.argv[1])
    
    if action == 'find':
        # Search for movies
        title = params.get('title', '')
        year = params.get('year', '')
        search_movie(title, year, handle)
        xbmcplugin.endOfDirectory(handle)
    
    elif action == 'getdetails':
        # Get movie details
        url = params.get('url', '')
        if url:
            get_details(url, handle)
        xbmcplugin.endOfDirectory(handle)
    
    elif action == 'NfoUrl':
        # Handle NFO URL (not implemented for this scraper)
        log("NfoUrl action called (not implemented)", xbmc.LOGINFO)
        xbmcplugin.endOfDirectory(handle)
    
    else:
        log(f"Unknown action: {action}", xbmc.LOGWARNING)
        xbmcplugin.endOfDirectory(handle)


if __name__ == '__main__':
    main()
