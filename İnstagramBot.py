from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from instagramUserInfo import username, password


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(6)  # Sayfanın yüklenmesi için bekle

        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        time.sleep(12)  # Giriş için bekle

    def get_followers(self):
        # Profil sayfasına git
        self.driver.get(f"https://www.instagram.com/{self.username}/")
        time.sleep(7)

        # Takipçi sayısını al
        followers_count = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span").get_attribute(
            "title")
        followers_count = int(followers_count.replace(",", ""))  # Eğer sayı virgüllüyse temizliyoruz
        print(f"Takipçi sayısı: ", followers_count)

        # Takipçiler butonuna tıkla
        followers_button = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]")
        followers_button.click()
        time.sleep(5)

        # Takipçi listesini scroll ederek takipçi sayısı kadar kullanıcı adı yazdır
        follower_list = self.driver.find_element(By.CLASS_NAME, "xyi19xy")  # Scroll yapılacak listeyi bul
        followers_fetched = 0  # Şu ana kadar yazdırılan takipçi sayısı

        while followers_fetched < followers_count:
            # Tüm görünen takipçileri bul
            followers = self.driver.find_elements(By.XPATH, "//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']")

            for follower in followers[followers_fetched:]:
                username = follower.text
                print(username)  # Kullanıcı adını yazdır
                followers_fetched += 1

                if followers_fetched >= followers_count:
                    break  # Tüm takipçileri yazdırdıysak döngüyü sonlandır

            # Sayfayı kaydır
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follower_list)
            time.sleep(2)  # Sayfa kaydırıldıktan sonra bekle


# Instagram bilgilerini `instagramUserInfo.py` dosyasından alıyoruz
instagram = InstagramBot(username, password)
instagram.login()  # Giriş yapılıyor
instagram.get_followers()  # Takipçileri alıyoruz
