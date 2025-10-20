import os
import json
import google.generativeai as genai

# Konfigurasi API key dari Secret Manager
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Fungsi untuk membaca file laporan dengan aman
def read_report(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Membaca data dari laporan Snyk dan ZAP
snyk_data = read_report('snyk_report.json')
zap_data = read_report('zap_report.json')

# Membuat prompt yang detail untuk AI
prompt = """
Anda adalah seorang ahli DevSecOps. Tugas Anda adalah menganalisis laporan keamanan dari Snyk (SCA) dan OWASP ZAP (DAST) berikut ini. Berikan ringkasan eksekutif dan rekomendasi perbaikan yang dapat ditindaklanjuti.

Format output yang saya inginkan:
1.  **Ringkasan Eksekutif:** Jelaskan secara singkat status keamanan aplikasi berdasarkan hasil scan.
2.  **Top 3 Isu Paling Kritis:** Sebutkan 3 temuan paling berisiko tinggi dari semua laporan.
3.  **Rekomendasi Utama:** Berikan langkah-langkah perbaikan yang harus diprioritaskan oleh tim developer.

Berikut adalah data laporannya:

**--- Laporan Snyk (Software Composition Analysis) ---**
{snyk_report}

**--- Laporan OWASP ZAP (Dynamic Application Security Testing) ---**
{zap_report}
""".format(snyk_report=json.dumps(snyk_data, indent=2) if snyk_data else "Tidak ada.",
           zap_report=json.dumps(zap_data, indent=2) if zap_data else "Tidak ada.")

# Membuat model dan mengirimkan prompt
print("🤖 Meminta ringkasan dari Gemini...")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)

# Mencetak hasil ringkasan
print("\n--- Ringkasan Keamanan oleh AI ---")
print(response.text)
print("---------------------------------")