from google import genai
from google.genai import types

def summarize_text(article):
    client = genai.Client(
        vertexai=True,
        project="intervest",
        location="global",
    )

    text1 = types.Part.from_text(text=f"""
    회사 투자팀을 위해 뉴스 article을 한 문단으로 요약해줘. 

    <rules>
    - 정확하게 기사에 있는 내용만 요약해. 
    - 프로패셔널하게 문장을 작성해 - 쓸데없이 길어지지 않도록.
    - 6문장 이내로 작성해줘.
    - 중요한 핵심을 잘 뽑아내야해.
    </rules>

    <article>
    {article}
    </article>""")

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
        temperature = 0.3,
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
        system_instruction=[types.Part.from_text(text="""너는 투자회사의 똑똑한 인턴이야. AI 분야에 많이 투자하는 곳이지.""")],
    )

    result = []
    for chunk in client.models.generate_content_stream(
        model = model,
        contents = contents,
        config = generate_content_config,
        ):
        if chunk.text:
            result.append(chunk.text)
    
    return ''.join(result)
