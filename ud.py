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
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Function to clean and fix the URL (regex) -- ESSENTIAL >
def normalize_url(url):
    """Ensure the URL starts with https:// and fix multiple slashes."""
    url = re.sub(r'^(https?:){2,}', '', url).strip()
    url = 'https://' + url if not url.startswith('https://') else url
    return re.sub(r'https?://+', 'https://', url)

# Configure session with retries and backoff
def create_session():
    """Create and configure a session with retry logic."""
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

# Function to sanitize app name for use in filenames
def sanitize_filename(filename):
    """Sanitize the app name for use as a valid filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Download app APK with a progress bar
def download_apk(session, download_url, app_name, version):
    """Download the APK file with a progress bar."""
    sanitized_filename = sanitize_filename(f"{app_name}_v{version}.apk")
    print(f"Starting download from {download_url}...")
    try:
        with session.get(download_url, stream=True, timeout=30) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            with open(sanitized_filename, "wb") as file, tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
                for chunk in response.iter_content(1024):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))
        print(f"Download complete! Saved as {sanitized_filename}")
    except requests.RequestException as e:
        print(f"Failed to download APK: {e}")

# Fetch download URL for a specific app version
def fetch_download_url(session, version_page_url, headers, app_name, version):
    """Fetch the download URL for a specific app version."""
    try:
        response = session.get(normalize_url(version_page_url), headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        download_button = soup.find('button', {'id': 'detail-download-button'})
        if download_button:
            download_url = normalize_url(download_button['data-url']).replace("https://", "https://dw.uptodown.net/dwn/")
            print(f"Download URL: {download_url}")
            if input("Download this version? (y/n): ").lower() == 'y':
                download_apk(session, download_url, app_name, version)
    except requests.RequestException as e:
        print(f"Failed to fetch version details: {e}")

# Fetch and list available versions of an app
def list_versions(session, app_link, headers, app_name):
    """Fetch available versions of the app."""
    try:
        response = session.get(f"{normalize_url(app_link)}/versions", headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        versions = [(version.find('span', class_='version').get_text(strip=True), version['data-url'])
                    for version in soup.find_all('div', {'data-url': True}) if version.find('span', class_='version')]
        if versions:
            for idx, (version, _) in enumerate(versions):
                print(f"{idx + 1}. Version {version}")
            selected_version = int(input(f"\nSelect version (1-{len(versions)}): ")) - 1
            if 0 <= selected_version < len(versions):
                fetch_download_url(session, f"https:{versions[selected_version][1]}", headers, app_name, versions[selected_version][0])
    except requests.RequestException as e:
        print(f"Failed to fetch versions: {e}")

# Search for apps on the selected platform and list results
def search_apps(session, search_query, headers, platform):
    """Search for apps on the selected platform."""
    platform_urls = ["android", "windows", "mac"]
    search_url = f"https://en.uptodown.com/{platform_urls[platform - 1]}/search"
    
    try:
        response = session.post(search_url, headers=headers, data={'q': search_query}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        apps = [(item.find('div', class_='name').get_text(strip=True), item.find('a')['href'])
                for item in soup.find_all('div', class_='item')[:10]]
        if apps:
            for idx, (app_name, app_link) in enumerate(apps):
                print(f"{idx + 1}. {app_name} - {app_link}")
            selected_app = int(input(f"\nSelect app (1-{len(apps)}): ")) - 1
            if 0 <= selected_app < len(apps):
                list_versions(session, apps[selected_app][1], headers, apps[selected_app][0])
    except requests.RequestException as e:
        print(f"Failed to search for apps: {e}")

# Main entry point
def main():
    """Main function to start the app download process."""
    search_query = input("\nSearch for an app: ")
    platform = int(input("Select platform (1: Android, 2: Windows, 3: Mac): "))
    if platform not in [1, 2, 3]:
        print("Invalid selection!")
        return
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    with create_session() as session:
        search_apps(session, search_query, headers, platform)

if __name__ == "__main__":
    main()
