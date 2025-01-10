# Uptodown - Android Apps Downloader (Scraping using BS4)
[![BDG](https://img.shields.io/badge/SSL_ACTX%20-GITHUB-blue.svg?style=flat)](https://github.com/SSL-ACTX/)
[![BDG](https://img.shields.io/badge/SSL_ACTX%20-EMAIL-red.svg?style=flat)](emailto:seuriin@gmail.com)

### Disclaimer:
This project is **for educational purposes only**. Use it responsibly and respect the ToS of any website you scrape from.

---

### Project Overview

This Python script allows you to search for Android apps on **Uptodown**, fetch available versions of the app, and download APK files using web scraping with **BeautifulSoup** and **requests**. It provides a simple CLI that guides you through searching for apps, selecting versions, and downloading APKs.

---

### Features

- **Search for apps**: Use a search query to find apps on Uptodown.
- **Fetch available versions**: Get a list of available versions for a selected app.
- **Download APKs**: Select a version and download the APK file with a progress bar.
- **Simple interface**: Simple command-line interface for user interaction.
- **App name sanitization**: Sanitizes app names to avoid issues with invalid filenames.

---

### Requirements

- Python 3.7+
- External libraries:
  - `requests`
  - `BeautifulSoup4` (from `bs4`)
  - `tqdm`

You can install the required dependencies using the following:

```bash
pip install requests beautifulsoup4 tqdm
```

---

### How to Use

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SSL-ACTX/SCR_Uptodown.git
   cd SCR_Uptodown
   ```

2. **Run the script**:

   ```bash
   python ud.py
   ```

3. **Search for an app**:
   - Enter the name of the app when prompted.
   
4. **Select the version**:
   - Choose an app version from the available list.
   
5. **Download the APK**:
   - Confirm the download to start the process.
   
   The download will begin, and you’ll see a progress bar indicating the progress.

### Example Output

```plaintext
Search App: Instagram

Available versions:
1. Version 234.0.0.0.16
2. Version 233.0.0.0.15

Select a version (1-2): 1
Fetching download details from: https://www.uptodown.com/android/versions/234.0.0.0.16
Download URL: https://dw.uptodown.net/dwn/instagram/234.0.0.0.16/instagram.apk
Do you want to download this version? (y/n): y

Starting download from https://dw.uptodown.net/dwn/instagram/234.0.0.0.16/instagram.apk...
Downloading: 100%|██████████| 50.0MB/50.0MB [00:03<00:00, 15.3MB/s]
Download complete! File saved as Instagram_v234.0.0.0.16.apk
```

---

### Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request. Feel free to open issues if you encounter bugs or have suggestions for improvements.

---

### License

This project is open-source and available under the [MIT License](LICENSE).
