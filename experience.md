My Learning Experience While Building This Chatbot

While building this chatbot, I didn’t just write code — I struggled, tested, and improved step by step.

🔹 1. Understanding RAG (Retrieval-Augmented Generation)

At first, I didn’t understand how chatbots answer from PDFs.
Then I learned:

PDF → text → chunks
chunks → embeddings (numeric vectors)
stored in FAISS
query → similarity search → context → LLM

This helped me understand how AI + search work together.

🔹 2. Confusion About Guardrails (Very Important)

Initially, I added guardrails using keywords, like:

python
AI
SQL
programming

Problem:

When I asked:
“What is cloud computing?”
“What is DevOps?”

The chatbot said:

“I only answer tech-related questions.”

Even though these ARE tech questions!

🔹 3. Why This Happened
My chatbot was using a manual keyword list
It only recognized words in that list
It failed for:
cloud computing
DevOps
quantum computing

I realized:

 “We cannot manually define all tech knowledge.”

🔹 4. Trying Semantic Detection (Second Attempt)

I tried improving it using semantic similarity (embeddings)

Idea:

Compare user question with “tech corpus”
If similar → allow answer

Problem:

Threshold tuning was difficult
Still blocked valid questions
Made system unnecessarily complex
🔹 5. Final Decision (Most Important Learning)

I removed all guardrails and trusted the LLM + system prompt.

Final logic:

If PDF uploaded → answer from PDF
Else → answer normally using LLM

Result:

Works for ALL tech questions
No manual keyword headache
Cleaner and more professional
🔹 6. Other Challenges I Faced
Understanding FAISS vector search
Handling Streamlit session state
PDF parsing issues (empty pages, formatting)
Managing API keys securely (.env)
Confusion between:
local storage vs cloud storage
embeddings vs text
🔹 7. What I Learned
How RAG systems actually work
Why embeddings are important
Why over-restricting AI is harmful
How to design a clean AI pipeline
How to build and deploy a real AI app