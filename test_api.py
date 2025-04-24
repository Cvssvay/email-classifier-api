# test_api.py
import requests
import json
import argparse

def test_api(url, email_text):
    """Test the email classification API"""
    
    # Prepare the request payload
    payload = {
        "email_body": email_text
    }
    
    try:
        # Send the request
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Request successful!")
            result = response.json()
            
            # Print the results in a readable format
            print("\n===== RESULTS =====")
            print(f"CATEGORY: {result['category_of_the_email']}")
            print("\nMASKED EMAIL:")
            print(result['masked_email'])
            
            print("\nMASKED ENTITIES:")
            for entity in result['list_of_masked_entities']:
                print(f"  - {entity['classification']}: '{entity['entity']}' at position {entity['position']}")
            
            return result
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Test Email Classification API')
    parser.add_argument('--url', type=str, default='http://127.0.0.1:8000/', 
                        help='URL of the API endpoint (default: http://127.0.0.1:8000/)')
    parser.add_argument('--email', type=str, required=True,
                        help='Email text to classify')
    
    args = parser.parse_args()
    
    test_api(args.url, args.email)

if __name__ == "__main__":
    main()