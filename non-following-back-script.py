import glob
import zipfile
from bs4 import BeautifulSoup

class InstagramAnalyzer:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path
    
    def find_zip_file(self):
        zip_files = glob.glob("*.zip")
        if zip_files:
            return zip_files[0]
        else:
            return None
    
    def extract_html_files(self):
        zip_file_path = self.find_zip_file()
        if zip_file_path is None:
            raise FileNotFoundError("No se encontraron archivos ZIP en el directorio actual.")
        
        following_data = None
        followers_data = None
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if 'following.html' in filename:
                    following_data = zip_ref.read(filename)
                elif 'followers_1.html' in filename:
                    followers_data = zip_ref.read(filename)
        return following_data, followers_data


    def parse_html(self, following_data, followers_data):
        all_urls = []
        for data in [following_data, followers_data]:
            soup = BeautifulSoup(data, 'html.parser')
            urls = [a['href'].replace('https://www.instagram.com/', '') for a in soup.find_all('a')]
            all_urls.append(urls)
        return all_urls
    
    def find_non_following_back(self, following, followers):
        non_following_back = [user for user in following if user not in followers]
        return non_following_back

    def analyze(self):
        following_data, followers_data = self.extract_html_files()
        following, followers = self.parse_html(following_data, followers_data)
        non_following_back = self.find_non_following_back(following, followers)
        with open('non-following-back.txt', 'w') as f:
            for user in non_following_back:
                f.write(user + '\n')

if __name__ == "__main__":
    analyzer = InstagramAnalyzer("")
    analyzer.analyze()