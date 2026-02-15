# 🏥 CHRONOCHECK - AI Medical Assistant

<div align="center">
  <h3>CHECK • CARE • CLARITY</h3>
  <p><i>AI-powered medical assistant with 10 language support</i></p>

  ![Python](https://img.shields.io/badge/Python-3.8+-blue)
  ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
  ![Astra](https://img.shields.io/badge/Powered_By-Astra_Langflow-blueviolet)

  <h3>🔗 <a href="https://rebwss8zaappg3bv862xhrd.streamlit.app/">Live Demo</a></h3>
</div>

> [!WARNING]
> **DISCLAIMER:** CHRONOCHECK is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician.

---

## 📋 **About**
CHRONOCHECK is a multi-agent healthcare companion that simplifies complex medical tasks:
- 🧠 **Medical Q&A:** Get instant answers to health-related queries.
- 📄 **Report Analysis:** Upload lab reports for easy-to-understand summaries.
- 🏥 **Hospital Finder:** Locates the nearest healthcare facilities.
- 💊 **Medicine Explainer:** Understand your prescriptions and dosage.
- 💰 **Bill Auditor:** Detects errors or overcharging in hospital bills.

**Supports 10 Indian languages** with a seamless bilingual toggle!

---

## 🚀 **Quick Start**

1. **Clone**
   ```bash
   git clone [https://github.com/kshitijaghan/chronocheck-.git](https://github.com/kshitijaghan/chronocheck-.git)
   cd chronocheck-
Install Dependencies

Bash
pip install -r requirements.txt
Run Application

Bash
streamlit run main_cloud.py
🔧 Configuration
The app uses Astra Langflow as the orchestration engine. To run your own version, create a .streamlit/secrets.toml file:

Ini, TOML
[api]
QNA_AGENT_URL = "your_url"
REPORT_ANALYZER_URL = "your_url"
PRESCRIPTION_ANALYZER_URL = "your_url"
BILL_ANALYZER_URL = "your_url"
HOSPITAL_FINDER_URL = "your_url"
APP_TOKEN = "your_token"
ORG_ID = "your_org_id"
🌐 Languages Supported
English, Hindi, Marathi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Punjabi.

📁 Sample Files
Test the agents using the files in the /sample_files folder:

📑 Lab Reports (for Report Analyzer)

📝 Prescriptions (for Medicine Explainer)

🧾 Hospital Bills (for Bill Auditor)

📞 Contact
Kshitija Ghan

Project Link: https://github.com/kshitijaghan/chronocheck-

<div align="center">
<p>Built with ❤️ using Langflow and Streamlit</p>
</div>
