# Creative Data Labeling with Gemini AI

A Flask web application for creative, AI-powered data labeling. Upload your CSV, define labeling rules, and let Google Gemini do the heavy lifting!

---

## 🚀 Features

- **CSV Upload:** Securely upload and preview your data.
- **Custom Labeling:** Define rules and let Gemini label your data.
- **Sample Output:** Instantly see labeled examples and raw AI output.
- **API-Ready:** All actions available via JSON endpoints.

---

## 🛠️ Requirements

- Python 3.8+
- Google Gemini API Key (`GOOGLE_API_KEY` environment variable)
- Python packages: `flask`, `pandas`, `google`, `werkzeug`

---

## 📦 Installation

git clone https://github.com/jfuladotcom/CreativeDataLabeling.git

cd CreativeDataLabeling

pip install flask pandas google werkzeug

Set your Gemini API key:

export GOOGLE_API_KEY="your-gemini-api-key-here"

---

## 🏃‍♂️ Usage

1. **Start the app:**

python app.py



2. **Open in your browser:**

http://127.0.0.1:5000/

3. **Upload a CSV and follow the on-screen instructions.**

---

## ⚙️ Environment Variables

- `GOOGLE_API_KEY` – Your Gemini API key (required).

---

## ❗ Notes

- **Max upload size:** 16MB
- **Allowed files:** CSV only
- Make sure your Gemini API key is valid and active.

---

## 🐞 Error Handling

- Returns JSON error messages for:
  - Invalid file uploads
  - Missing data or prompt
  - Gemini API failures
- Handles 404 and 500 errors gracefully.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)
- [Google Gemini API](https://ai.google.dev/)
- [Werkzeug](https://werkzeug.palletsprojects.com/)

---

**Happy labeling!** 🎉
