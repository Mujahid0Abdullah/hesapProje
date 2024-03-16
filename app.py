# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, request, jsonify, render_template
from flask_cors  import CORS
import itertools


print("Merhaba! 😊 Ahmet Kurc ve Zaid Alabdullah 9/A tarafından oluşturuldu.")


def hesapla_denklem(denklem):
    try:
        result = eval(denklem)
        return result if result is not None else float('inf')  # None yerine float('inf') kullan
    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None


def denklemleri_uret(sayilar, hedef):
    islemler = ['+', '-', '*', '/']
    cozumler = []

    for permutasyon in itertools.permutations(sayilar):
        for ops in itertools.product(islemler, repeat=len(sayilar) - 1):
            denklem = ''.join(str(sayi) + islem for sayi, islem in zip(permutasyon, ops)) + str(permutasyon[-1])
            sonuc = hesapla_denklem(denklem)
            if sonuc is not None and abs(sonuc - hedef) < 1e-6:
                cozumler.append(denklem)

    return cozumler if cozumler else ["Çözüm bulunamadı."]


def input_al(mesaj, tip=None, min_=None, max_=None):
    while True:
        try:
            kullanici_girdisi = input(mesaj)
            if tip is not None:
                kullanici_girdisi = tip(kullanici_girdisi)
            if min_ is not None and kullanici_girdisi < min_:
                print(f"Lütfen {min_} veya daha büyük bir sayı girin.")
                continue
            if max_ is not None and kullanici_girdisi > max_:
                print(f"Lütfen {max_} veya daha küçük bir sayı girin.")
                continue
            return kullanici_girdisi
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")


def ana_program():
    while True:
        hedef = input_al("Hedef sayıyı girin: ", int)
        sayi_adedi = input_al("Kaç sayı kullanmak istiyorsunuz? ", int, 1)

        # Kullanıcıdan sayıları manuel olarak girmesini isteyin
        sayilar = [input_al(f"{i + 1}. sayıyı girin: ", int) for i in range(sayi_adedi)]

        print(f"Kullanılacak sayılar: {sayilar}")
        denklemler = denklemleri_uret(sayilar, hedef)

        print("Hesaplama tamamlandı. İşte sonuçlar:")
        for denklem in denklemler:
            print(f"{denklem} = {hedef}")

        tekrar_dene = input_al("Tekrar denemek ister misiniz? (Evet için 'e' veya 'E' girin): ", str)
        if tekrar_dene.lower() != 'e':
            break

app = Flask(__name__)
CORS(app)

@app.route('/')
def ana_sayfa():
    return render_template('web.html')

@app.route("/hesapla", methods=["POST"])
def hesapla_post():
    veri = request.get_json()
    hedef = veri["hedef"]
    sayilar = veri["sayilar"]

    denklemler = denklemleri_uret(sayilar, hedef)

    return jsonify({"denklemler": denklemler})


if __name__ == "__main__":
    #ana_program()
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
