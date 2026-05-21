
import os
import sys
import openai

# Best practice is to keep your API key secure in an environment variable.
# On your Alpine terminal, run: export OPENAI_API_KEY="your-key"
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("Warning: OPENAI_API_KEY environment variable not found.")
    print("Please set it in your terminal or temporarily insert your key in the script.")
    # You can paste your key below temporarily if you prefer:
    # api_key = "sk-proj-your-key-here"

# Auto-detect OpenAI library version to prevent ImportErrors
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    IS_MODERN_SDK = True
except ImportError:
    # Fallback for older package versions (< v1.0.0)
    openai.api_key = api_key
    IS_MODERN_SDK = False

def chat_with_gpt(prompt):
    try:
        if IS_MODERN_SDK:
            # Code for modern SDK versions (>= 1.0.0)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            # Code for legacy SDK versions (< 1.0.0)
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini", # Still works with older clients!
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting AI: {e}"

if __name__ == "__main__":
    print("=========================================================")
    print(" Welcome to Sage AI! (Type 'exit', 'quit', or 'bye' to end) ")
    print(f" SDK Status: {'Modern Client' if IS_MODERN_SDK else 'Legacy Client (Auto-Compatibility Mode)'}")
    print("=========================================================")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
            
        # Clean check to see if the user wants to leave
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("SAGE: Goodbye! Have a wonderful day!")
            break
            
        if not user_input:
            continue
            
        response = chat_with_gpt(user_input)
        print(f"\nSAGE: {response}")

