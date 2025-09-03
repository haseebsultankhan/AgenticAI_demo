import pandas as pd
import re

def match_whole_word(text, word):
    """Match only whole words, case insensitive."""
    return bool(re.search(rf'\b{re.escape(word)}\b', str(text).lower()))

def search_location(keyword: str, df: pd.DataFrame):
    keyword = keyword.strip().lower()

    # Step 1: Special handling for "international"
    if keyword == "international":
        result = df[df['region'].str.lower() == 'international']
    else:
        # Step 2: Match city
        result = df[df['City'].apply(lambda x: match_whole_word(x, keyword))]

        # Step 3: If city match fails, match location
        if result.empty:
            result = df[df['location'].apply(lambda x: match_whole_word(x, keyword))]

        # Step 4: If location match fails, match address
        if result.empty:
            result = df[df['address'].apply(lambda x: match_whole_word(x, keyword))]

    # Step 5: Output
    print(f"Locations for '{keyword}':")
    if not result.empty:
        result = result[['location', 'address', 'phone', 'City']].rename(
            columns={
                'location': 'Location Name',
                'address': 'Address',
                'phone': 'Phone',
                'City': 'City'
            }
        ).reset_index(drop=True)

        for i, row in result.iterrows():
            print(f"{i + 1}. {row['Location Name']}\n"
                  f"   Address: {row['Address']}\n"
                  f"   Phone: {row['Phone']}\n"
                  f"   City: {row['City']}\n")
    else:
        print(f"No locations found for the location '{keyword}'\n")

# Load dataset
df = pd.read_excel('data/locations_with_region_city.xlsx')

# Main loop
if __name__ == "__main__":
    try:
        user_input = input().strip()
        if not user_input:
            print("Please enter a non-empty keyword.\n")
        else:
            search_location(user_input, df)
    except KeyboardInterrupt:
        print("\nExited by user.")
