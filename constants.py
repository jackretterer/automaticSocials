# constants.py

GET_QUOTES_PROMPT = """
You will be given a transcript of a speech, interview, or conversation. Your task is to create inspirational, heartwarming, and informative quotes from this transcript. The quotes should be relatable and impactful. Make them so people would share them.

Guidelines for creating quotes:
1. Select or paraphrase impactful statements that convey wisdom, encouragement, or valuable information.
2. Ensure each quote can stand alone and make sense without additional context.
3. Aim for a mix of short, punchy quotes and slightly longer, more detailed ones.
4. Maintain the original speaker's voice and intent.
5. Create 5 quotes.

Format your output as a JSON list of quote objects. Each quote object should have two properties:
- "quote": The text of the quote
- "type": The category of the quote (either "inspirational", "heartwarming", or "informative")
- "title": The title of the quote

Here's an example of how your output should be structured:

[
  {
    "quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "type": "inspirational",
    "title": "Success is not final"
  },
  {
    "quote": "In the depth of winter, I finally learned that there was in me an invincible summer.",
    "type": "heartwarming",
    "title": "I am invincible"
  },
  {
    "quote": "The average person uses only 10 percent of their brain capacity.",
    "type": "informative",
    "title": "What could you if you had 100 percent of your brain capacity?"
  }
]

Return only the JSON, without any additional text or explanation.
"""

