from google import genai
from google.genai import types
import json

def summarizer(url):
  client = genai.Client(
      vertexai=True,
      project="intervest",
      location="global",
  )

  text1 = types.Part.from_text(text=f"""
    You are given a url to an article.
    Your task is to read the article and give summary in Korean.
    Make sure to extract the key-point in the article.

    Input url article is given below.
    <url>
    {url}
    </url>

    <rules>
    1. Use concise sentences.
    2. Complete with 3 sentences.
    3. Always give response in Korean.
    4. Keep pronouns like name, company in English.
    5. Only use the content in the article
    </rules>

    <output>
    json format
    "title": short title,
    "summary": summarized content,
    "url": link to the article
    </output>""")

  model = "gemini-2.0-flash-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        text1
      ]
    )
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 0.5,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    response_mime_type = "application/json",
    response_schema = {"type":"OBJECT","properties":{"response":{"type":"STRING"}}},
    system_instruction=[types.Part.from_text(text="""You are Korean-English multi-lingual analyst intern. The firm specializes in AI investments.""")],
  )

  response = client.models.generate_content(
    model = model,
    contents = contents,
    config = generate_content_config,
  )

    # First parse the outer response object
  outer_json = json.loads(response.text)
  # Then parse the inner JSON string from the "response" field
  parsed = json.loads(outer_json["response"])
  inner_json = parsed[0] if isinstance(parsed, list) else parsed
  return inner_json

if __name__ == "__main__":
  url = "https://techcrunch.com/2025/04/04/chatgpt-adoption-skyrockets-in-india-but-monetization-may-be-trailing/"
  result = summarizer(url)
  print(json.dumps(result, indent=2, ensure_ascii=False))
