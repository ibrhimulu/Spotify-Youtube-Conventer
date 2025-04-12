# Spotify YouTube Playlist Dönüştürücü

Bu proje, Spotify çalma listelerini YouTube çalma listelerine dönüştürmenizi sağlayan bir web uygulamasıdır.

## Özellikler

- Spotify çalma listelerini otomatik olarak YouTube'a aktarma
- Şarkı eşleştirme ve doğrulama
- Kullanıcı dostu arayüz
- OAuth2 ile güvenli kimlik doğrulama

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/spotify-youtube-conventer.git
cd spotify-youtube-conventer
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

## Kullanım

1. Uygulamayı başlatın:
```bash
python app.py
```

2. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin

3. Spotify hesabınızla giriş yapın

4. Dönüştürmek istediğiniz çalma listesini seçin

5. YouTube hesabınızla giriş yapın

6. Dönüştürme işlemini başlatın


## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
