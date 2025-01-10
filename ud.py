####################################################################
#                                                                  #
#     Uptodown - Android Apps Downloader (Scraping using BS4)      #
#         GitHub: SSL-ACTX    Email: seuriin@gmail.com             #
#                                                                  #
#         (!) Disclaimer! For educational purposes only            #
#                                                                  #
#  P.S. I tried my best to make the code as readable as possible.  #
#                                                                  #
####################################################################
import requests
import re
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

# Function to clean and fix the URL (regex) -- ESSENTIAL >
def fix_url(url):
    """Ensure the URL starts with https:// and fix multiple slashes."""
    url = re.sub(r'^(https?:){2,}', '', url).strip()
    url = 'https://' + url if not url.startswith('https://') else url
    
    return re.sub(r'https?://+', 'https://', url)

# Fetch the download URL for a specific version of the app
def fetch_version_download_url(version_page_url, headers, app_name, version):
    """Fetch the download URL for a specific app version."""
    version_page_url = fix_url(version_page_url)
    print(f"Fetching download details from: {version_page_url}...")
    
    response = requests.get(version_page_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch version page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    download_button = soup.find('button', {'id': 'detail-download-button'})
    
    if download_button:
        download_url = fix_url(download_button['data-url'])
        download_url = download_url.replace("https://", "https://dw.uptodown.net/dwn/")  # Reformat URL
        
        print(f"Download URL: {download_url}")
        if input("Do you want to download this version? (y/n): ").lower() == 'y':
            download_file(download_url, app_name, version)
        else:
            print("Download canceled.")
    else:
        print("Download button not found.")

# App name sanitization function (regex)
def sanitize_filename(name):
    """Sanitize the app name for use as a valid filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Download func with TQDM as progress bar
def download_file(url, app_name, version):
    """Download the app APK with a progress bar."""
    sanitized_name = sanitize_filename(f"{app_name}_v{version}.apk")
    print(f"Starting download from {url}...")
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024
        
        with open(sanitized_name, "wb") as file, tqdm(
            total=total_size, unit='B', unit_scale=True, desc="Downloading"
        ) as bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))

        print(f"Download complete! File saved as {sanitized_name}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# Fetch and list available versions of the app
def fetch_versions(app_link, headers, app_name):
    """Fetch available versions of the app and display them."""
    versions_page_url = f"{app_link}/versions"
    print(f"Fetching available versions from: {versions_page_url}")
    
    response = requests.get(versions_page_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch versions page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    versions_list = soup.find_all('div', {'data-url': True})
    
    if not versions_list:
        print("No versions found.")
        return
    
    print("\nAvailable versions:")
    versions = [
        (v.find('span', class_='version').get_text(strip=True), v['data-url']) 
        for v in versions_list if v.find('span', class_='version')
    ]

    for index, (version_text, _) in enumerate(versions):
        print(f"{index + 1}. Version {version_text}")
    
    try:
        select_version = int(input(f"\nSelect a version (1-{len(versions)}): ")) - 1
        if 0 <= select_version < len(versions):
            fetch_version_download_url(f"https:{versions[select_version][1]}", headers, app_name, versions[select_version][0])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Search for apps and list results
def search_apps(search_query, headers, limit_results=10):
    """Search for apps and list search results."""
    search_url = "https://en.uptodown.com/android/search"
    response = requests.post(search_url, headers=headers, data={'q': search_query})

    if response.status_code != 200:
        print(f"Failed to fetch search results. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    search_results = soup.find_all('div', class_='item')[:limit_results]

    if not search_results:
        print("No search results found.")
        return
    
    print("\nSearch Results:")
    app_links = []
    for index, item in enumerate(search_results):
        app_name = item.find('div', class_='name').get_text(strip=True)
        app_link = item.find('a')['href']
        print(f"{index + 1}. {app_name} - {app_link}")
        app_links.append((app_name, app_link))

    try:
        select_app = int(input(f"\nSelect an app (1-{len(search_results)}): ")) - 1
        if 0 <= select_app < len(search_results):
            selected_app_name, selected_app_url = app_links[select_app]
            fetch_versions(selected_app_url, headers, selected_app_name)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Main entry point
def main():
    """Main function to start the app download process."""
    search_query = input("\nSearch App: ")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_apps(search_query, headers)

if __name__ == "__main__":
    main()
