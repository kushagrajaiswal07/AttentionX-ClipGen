import google.generativeai as genai
import json

# TODO: Paste your API key here again!
GEMINI_API_KEY = "YOUR_API_KEY_HERE" 
genai.configure(api_key=GEMINI_API_KEY)

def get_highlights(segments):
    print("Connecting to Gemini 1.5 Flash...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    transcript_data = json.dumps(segments, indent=2)

    prompt = f"""
    You are an expert short-form video editor for TikTok and Reels. 
    Analyze the following video transcript segments with timestamps.
    Find the 3 most engaging "golden nuggets" (emotional peaks).
    
    CRITICAL INSTRUCTION: You MUST combine multiple consecutive segments together to form a complete thought. 
    Each of the 3 highlights MUST be between 15 and 45 seconds long.
    
    Also, write a 3 to 5 word, catchy, ALL CAPS "hook" headline for each highlight to make viewers stop scrolling.
    
    Transcript Data:
    {transcript_data}

    Return ONLY a raw JSON array of objects with 'start', 'end', and 'hook' keys. No markdown.
    Example format: [{{"start": 12.5, "end": 45.0, "hook": "DO THIS EVERY DAY"}}]
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()

        highlights = json.loads(response_text)
        formatted_highlights = []

        for h in highlights:
            start = float(h['start'])
            end = float(h['end'])
            hook = str(h.get('hook', 'WATCH THIS NOW')) # Grab the hook, with a fallback
            
            if end - start < 15:
                center_time = (start + end) / 2
                start = max(0, center_time - 7.5)
                end = center_time + 7.5
                
            formatted_highlights.append((start, end, hook)) # Now returning 3 items!

        print(f"Highlights with Hooks: {formatted_highlights}")
        return formatted_highlights

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return [(0, 15, "MUST WATCH"), (15, 30, "MIND BLOWING SECRET"), (30, 45, "NEVER DO THIS")]