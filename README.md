# Spotify YouTube Playlist Converter / Spotify YouTube Çalma Listesi Dönüştürücü

## 🌍 English

This project is a web application that allows you to convert Spotify playlists to YouTube playlists.

### Features

- Automatically transfer Spotify playlists to YouTube
- Song matching and verification
- User-friendly interface
- Secure authentication with OAuth2

### Installation

1. Clone the project:
```bash
git clone https://github.com/ibrhimulu/Spotify-Youtube-Conventer.git
cd Spotify-Youtube-Conventer
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Linux/Mac:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` file:
- Add your Spotify API credentials
- Generate a secret key

6. Set up Google API credentials:
- Create a project in Google Cloud Console
- Enable YouTube Data API v3
- Create OAuth 2.0 credentials
- Add `client_secret.json` to project directory

### Usage

1. Start the application:
```bash
python app.py
```

2. Go to `http://127.0.0.1:5000` in your browser

3. Log in with your Spotify account

4. Select the playlist you want to convert

5. Log in with your YouTube account

6. Start the conversion process

## 🌍 Türkçe

Bu proje, Spotify çalma listelerini YouTube çalma listelerine dönüştürmenizi sağlayan bir web uygulamasıdır.

### Özellikler

- Spotify çalma listelerini otomatik olarak YouTube'a aktarma
- Şarkı eşleştirme ve doğrulama
- Kullanıcı dostu arayüz
- OAuth2 ile güvenli kimlik doğrulama

### Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/ibrhimulu/Spotify-Youtube-Conventer.git
cd Spotify-Youtube-Conventer
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# Linux/Mac için:
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyası oluşturun:
```bash
cp .env.example .env
```

5. `.env` dosyasını düzenleyin:
- Spotify API bilgilerinizi ekleyin
- Secret key oluşturun

6. Google API bilgilerini ayarlayın:
- Google Cloud Console'dan bir proje oluşturun
- YouTube Data API v3'ü etkinleştirin
- OAuth 2.0 kimlik bilgilerini oluşturun
- `client_secret.json` dosyasını proje dizinine ekleyin

### Kullanım

1. Uygulamayı başlatın:
```bash
python app.py
```

2. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin

3. Spotify hesabınızla giriş yapın

4. Dönüştürmek istediğiniz çalma listesini seçin

5. YouTube hesabınızla giriş yapın

6. Dönüştürme işlemini başlatın

## 📄 License / Lisans

This project is licensed under the MIT License. See the `LICENSE` file for more information.

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın. 
