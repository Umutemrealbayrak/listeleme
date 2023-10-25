import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)


base_url = "base_url"


username = "username"
password = "password"


ticket_data = {
    "kullaniciAdi": "kullaniciadi",
    "sifre": "sifre"
}


def get_ticket():
    ticket_url = base_url + "TicketAl"
    response = requests.post(ticket_url, auth=(username, password), data=ticket_data)
    if response.status_code == 200:
        return response.json().get("ID")
    else:
        return None


def get_klasor_listesi(ticket_id):
    klasor_url = base_url + "KlasorListesiGetir"
    params = {"ticketID": ticket_id}
    response = requests.get(klasor_url, auth=(username, password), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_dosya_listesi(ticket_id):
    dosya_url = base_url + "DosyaListesiGetir"
    params = {"ticketID": ticket_id}
    response = requests.get(dosya_url, auth=(username, password), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def read_results():
    try:
        with open("sonuclar.txt", "r") as dosya:
            return dosya.read()
    except FileNotFoundError:
        return "Sonuç dosyası bulunamadı."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        kullanici_adi = request.form.get("kullaniciAdi")
        sifre = request.form.get("sifre")

        if kullanici_adi != ticket_data["kullaniciAdi"] or sifre != ticket_data["sifre"]:
            return "Hatalı kullanıcı adı veya şifre. Lütfen tekrar deneyin."

        
        ticket_id = get_ticket()

        if ticket_id:
           
            klasor_listesi = get_klasor_listesi(ticket_id)

           
            dosya_listesi = get_dosya_listesi(ticket_id)

            
            sonuclar = ""

            if request.form.get("klasorButonu") and klasor_listesi:
                sonuclar += "<h2>Klasör Listesi:</h2>"
                sonuclar += "<table>"
                sonuclar += "<thead><tr><th>ID</th><th>Adı</th></tr></thead>"
                sonuclar += "<tbody>"
                for klasor in klasor_listesi:
                    klasor_id = klasor.get("ID")
                    klasor_ad = klasor.get("Adi")
                    sonuclar += "<tr onclick='highlightRow(this)'><td>{}</td><td>{}</td></tr>".format(klasor_id, klasor_ad)
                sonuclar += "</tbody></table>"

            if request.form.get("dosyaButonu") and dosya_listesi:
                sonuclar += "<h2>Dosya Listesi:</h2>"
                sonuclar += "<table>"
                sonuclar += "<thead><tr><th>ID</th><th>Adı</th><th>Boyut</th></tr></thead>"
                sonuclar += "<tbody>"
                for dosya in dosya_listesi:
                    dosya_id = dosya.get("ID")
                    dosya_ad = dosya.get("Adi")
                    dosya_boyut = dosya.get("Boyut")
                    sonuclar += "<tr onclick='highlightRow(this)'><td>{}</td><td>{}</td><td>{}</td></tr>".format(dosya_id, dosya_ad, dosya_boyut)
                sonuclar += "</tbody></table>"

            
            with open("sonuclar.txt", "w") as dosya:
                dosya.write(sonuclar)

            
            if request.form.get("klasorButonu"):
                return sonuclar
            elif request.form.get("dosyaButonu"):
                return sonuclar
            else:
                return read_results()
        else:
            return "Ticket alınamadı."
    else:
        
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Divvy Drive Dosya ve Klasör Listesi</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                h1, h2 {
                    text-align: center;
                }
                form {
                    text-align: center;
                }
                pre {
                    background-color: #f0f0f0;
                    padding: 10px;
                    white-space: pre-wrap;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }
                .login-form {
                    border: 1px solid #ccc;
                    padding: 20px;
                    max-width: 300px;
                    margin: 0 auto;
                    background-color: #f9f9f9;
                }
                .login-form label {
                    display: block;
                    text-align: left;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .login-form input[type="text"], .login-form input[type="password"] {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 15px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                .login-form input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: block;
                    width: 100%;
                    cursor: pointer;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background-color: #f2f2f2;
                }
            </style>
            <script>
                function highlightRow(row) {
                    row.style.backgroundColor = "#ffff99";
                }
            </script>
        </head>
        <body>
            <h1>Divvy Drive Dosya ve Klasör Listesi</h1>

            <div class="login-form">
                <form method="post">
                    <label for="kullaniciAdi">Kullanıcı Adı:</label>
                    <input type="text" id="kullaniciAdi" name="kullaniciAdi" required>
                    <label for="sifre">Şifre:</label>
                    <input type="password" id="sifre" name="sifre" required>
                    <input type="submit" name="klasorButonu" value="Klasör Listesi">
                    <input type="submit" name="dosyaButonu" value="Dosya Listesi">
                </form>
            </div>

            {% if sonuclar %}
                <h2>Sonuçlar:</h2>
                <pre>{{ sonuclar }}</pre>
                <br>
            {% endif %}

        </body>
        </html>
        """)

if __name__ == "__main__":
    app.run()
