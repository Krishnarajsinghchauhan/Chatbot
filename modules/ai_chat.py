import google.generativeai as bard
from config import BARD_API_KEY

bard.configure(api_key=BARD_API_KEY)

def chat_with_ai(prompt):
    """Directly uses Bard (Gemini) for generating responses."""
    if not prompt.strip():  # Prevent sending empty input to Bard
        return "Sorry, I couldn't understand."

    try:
        model = bard.GenerativeModel("gemini-2.0-flash")  # Adjust model name if necessary
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else "Sorry, Bard didn't return a valid response."
    except Exception as e:
        print("Bard Error:", e)
        return "Sorry, I couldn't process that."