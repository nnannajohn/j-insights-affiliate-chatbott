import time  # Import time to fix the NameError
import requests
import json
from SimplerLLM.language.llm import LLM, LLMProvider

# Initialize the LLM (Language Model)
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="chatgpt-4o-latest")

def get_url_content(url: str) -> str:
    retries = 3  # Retry 3 times if fetching fails
    for attempt in range(retries):
        try:
            print(f"DEBUG: Fetching URL: {url}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br"
            }
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()  # Raise an error for HTTP errors like 403
            print("DEBUG: Fetched content successfully.")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: Error fetching URL: {e}")
            time.sleep(30)  # Increase the delay to 30 seconds between retries
    print(f"DEBUG: Failed to fetch content from {url} after retries.")
    return ""

def extract_hosting_info(content: str) -> str:
    if not content.strip():
        print("DEBUG: Content is empty. Skipping extraction.")
        return ""
    print("DEBUG: Sending content to LLM...")
    prompt = f"""
    Analyze the following web page content and extract relevant hosting information:
    {content[:500]}  # Send the first 500 characters to avoid token limits
    """
    try:
        response = llm_instance.generate_response(max_tokens=16000, prompt=prompt)
        print(f"DEBUG: LLM response: {response}")  # Print full response
        print("DEBUG: LLM response received.")
        return response
    except Exception as e:
        print(f"DEBUG: Error with LLM extraction: {e}")
        return ""

def main():
    print("DEBUG: Starting main workflow...")
    urls = [
        "https://www.hostinger.com/wordpress-hosting",
        "https://clients.verpex.com/aff/?a_aid=refid&a_aid=Jinsights",
        "https://www.vpsbg.eu/aff/7cb495",
    ]
    
    all_services = []

    for url in urls:
        content = get_url_content(url)
        if not content:
            print(f"DEBUG: No content fetched for {url}. Skipping.")
            continue
        text_info = extract_hosting_info(content)
        if not text_info:
            print(f"DEBUG: Failed to extract info for {url}.")
            continue
        
        print(f"DEBUG: Extracted Info: {text_info}")
        all_services.append(text_info)

    with open('wordpress_hosting_services.json', 'w') as f:
        json.dump(all_services, f, indent=2)
        print("DEBUG: All data has been saved to 'wordpress_hosting_services.json'.")

if __name__ == "__main__":
    main()
