# DailySparkClean

🚀 **DailySparkClean** ir FastAPI backend aplikācija, kas izmanto OpenAI GPT-3.5-turbo modeli, lai ģenerētu iedvesmojošus, motivējošus vai izglītojošus tekstus, pamatojoties uz lietotāja ievadītu pieprasījumu.

## 🔧 Funkcionalitāte

- `/generate` – POST pieprasījums, kas pieņem `prompt` kā JSON lauku un atgriež GPT-ģenerētu atbildi.
- `/` – GET pieprasījums, kas parāda, ka API darbojas.
- `/network-test` – GET pieprasījums, lai pārbaudītu savienojumu ar OpenAI API serveriem.

## 🌐 Tehnoloģijas

- Python 3.11
- FastAPI
- OpenAI Python SDK (`openai`)
- Railway (hosting)
- GitHub (versiju kontrole)

## 📦 Instalācija (vietējai izstrādei)

```bash
git clone https://github.com/IndraSofija/DailySparkClean.git
cd DailySparkClean
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload

## 🔗 API piekļuves adrese

Tavu backend aplikāciju var sasniegt caur šo adresi:

👉 **https://dailysparkclean-production-74eb.up.railway.app**

- Lai ģenerētu tekstu, sūti POST pieprasījumu uz:
https://dailysparkclean-production-74eb.up.railway.app/generate

- Header:Content-Type: application/json

- Body piemērs:
```json
{
  "prompt": "Dod man spēka vārdus šodienai"
}
Šo adresi vari izmantot frontendā, testēšanā (piemēram, ar ReqBin vai Postman), kā arī automatizācijā.

# Wake up commit for Railway cron sync
Trigger Railway cron activation

## 🚀 DailySpark Backend – Statusa Pārskats

### ✅ Paveiktais

- FastAPI backend izveidots un darbojas Railway vidē (`lucky-strength` instance).
- API maršruti:
  - `GET /` – servera statusa pārbaude
  - `POST /generate` – dzirksteles ģenerēšana ar OpenAI API
  - `GET /network-test` – savienojuma pārbaude ar OpenAI serveri
  - `GET /reset-daily-sparks` – dienas dzirksteles atjaunošanas simulācija
- Crone konfigurācija (`railway.json`):
  - `reset-daily-sparks` maršruts tiek automātiski izsaukts katru dienu 00:00 UTC.
- Ieviessts ģenerēšanas limits (viena dzirkstele dienā = 86400 sekundes).
- `print()` testēšanas rindiņas aizstātas ar `logging`, lai saglabātu tīru produkcijas kodu.
- Railway instances sakoptas: saglabāts tikai viens oficiāls backend projekts (`lucky-strength`).
- Visi maršruti testēti ar ReqBin – tostarp kļūdu scenāriji.

---

### 🔜 Plānotie darbi

- [ ] Ievietot reālu `user_id` no frontend (vietā, kur šobrīd ir `default_user`)
- [ ] Pievienot personalizēto dzirksteļu ģenerēšanu (Pro funkcionalitāte)
- [ ] Saglabāto dzirksteļu arhīvs (`/save`, `/history`)
- [ ] Stripe maksājumu integrācija ar Webhook loģiku
- [ ] Automatizēta dzirksteļu uzskaite datubāzē
- [ ] Lietotāju autentifikācija un piekļuves kontrole (ja nepieciešams)
- [ ] Drošības mehānismi: rate limiting, request validācija, API piekļuves kontrole



