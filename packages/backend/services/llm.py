import openai
from backend.config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(question: str, context_chunks: list):
    """
    Constructs a prompt with context and gets answer from GPT.
    """
    context_text = "\n\n---\n\n".join([c['text'] for c in context_chunks])
    
    system_prompt = "You are a helpful assistant. Answer the user's question based ONLY on the context provided below. If the answer is not in the context, say 'I don't know'."
    
    user_prompt = f"""
    Context from PDF:
    {context_text}
    
    User Question: 
    {question}
    """    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Or "gpt-3.5-turbo" if you want cheaper
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with AI: {e}"