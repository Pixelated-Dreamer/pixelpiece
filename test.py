import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.generativeai as genai
from streamlit_option_menu import option_menu

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# --- Gmail Setup ---
def get_gmail_service():
    creds = None
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    except:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_labels(service):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    return [label["name"] for label in labels]

def get_senders_from_label(service, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    label_id = None
    for label in labels:
        if label["name"] == label_name:
            label_id = label["id"]
            break
    if not label_id:
        return []

    results = service.users().messages().list(userId="me", labelIds=[label_id], maxResults=100).execute()
    messages = results.get("messages", [])

    senders = {}
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From"]).execute()
        for header in msg_data["payload"]["headers"]:
            if header["name"] == "From":
                senders.setdefault(header["value"], []).append(msg["id"])
    return senders

def get_last_emails(service, sender_ids, max_count=3):
    emails = []
    for msg_id in sender_ids[:max_count]:
        msg_data = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        snippet = msg_data.get("snippet", "")
        emails.append(snippet)
    return emails

# --- Gemini Setup ---
genai.configure(api_key="AIzaSyCmpSfdm0DVMx9O2d-PVDCrhx_UQfqJwTo")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def summarize_emails(emails):
    combined_text = "\n\n".join(emails)
    prompt = f"""
    You are an expert AI news editor. Here are some emails/news snippets:

    {combined_text}

    Please combine these into one long, engaging, and detailed news-style article.
    Make it flow like a professional newsletter with smooth transitions, interesting storytelling,
    and highlight key insights.
    """
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---
st.set_page_config(layout="wide")
service = get_gmail_service()

with st.sidebar:
    st.header("Filters")
    all_labels = get_labels(service)
    label_choice = option_menu("Choose a Gmail label:", all_labels)

    selected_senders = []
    if label_choice:
        senders_dict = get_senders_from_label(service, label_choice)
        sender_list = list(senders_dict.keys())
        selected_senders = st.multiselect("Select senders:", sender_list)

if st.button("Generate Combined News"):
    all_emails = []
    for sender in selected_senders:
        msg_ids = senders_dict[sender]
        last_emails = get_last_emails(service, msg_ids, max_count=3)
        all_emails.extend(last_emails)

    if all_emails:
        summary = summarize_emails(all_emails)
        st.subheader("📰 Combined AI News")
        st.text_area("Output", value=summary, height=2500)
    else:
        st.warning("No emails found for the selected senders.")
