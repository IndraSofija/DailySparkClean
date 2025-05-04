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

