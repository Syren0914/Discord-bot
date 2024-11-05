import google.generativeai as genai
import os


def ai_news():
    genai.configure(api_key = os.getenv("API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""Create a Discord-friendly post about an esoteric or niche technology. Make sure to vary the format and structure each time you use this prompt. Include the following elements:

    Engaging Title: Choose a creative title that draws attention.
    Brief Overview: Describe what the technology is, its origin, and its key features in a concise manner.
    Interesting Aspects: Highlight what makes this technology fascinating or valuable, especially in educational contexts.
    Commands or Features: Present a list or table of essential commands, features, or characteristics that define the technology.
    Famous Example: Provide an example of how the technology is used, perhaps with a notable program or application.
    Final Thoughts: Conclude with a thought-provoking statement about the relevance or implications of this technology in understanding broader programming concepts.
    Link for More Information: Add a reliable source link for readers who want to explore further.

    """)

    return response.text

