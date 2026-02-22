# DMM Python SDK (WIP)

A high-performance, strictly-typed Python wrapper for the DMM Affiliate API. Built heavily on [`msgspec`](https://jcristharif.com/msgspec/) for blazing-fast JSON serialization/deserialization and robust schema validation.

## Quick Start

This example demonstrates how to initialize the `DMMClient`, build a strictly-typed request, execute it using a `requests.Session`, and decode the raw JSON response back into safe Python objects.

```python
import requests
import msgspec

# Import your client and models
from dmm import (
    DMMClient,
    DMMSiteCode,
    DMMItemListRequestParams,
    DMMItemListResponseBody,
)

def main():
    session = requests.Session()

    # 1. Initialize the client with your raw credentials
    client = DMMClient(api_id="YOUR_API_ID", affiliate_id="YOUR_AFFILIATE_ID")

    # 2. Build parameters using the strictly-typed SDK model
    item_list_request_params = DMMItemListRequestParams(site=DMMSiteCode.FANZA)

    # 3. Generate the request data via the client
    item_list_request_data = client.create_item_list_request_data(item_list_request_params)

    # 4. Execute the HTTP request using a requests.Session
    print(f"Fetching data from {item_list_request_data.url}...")
    response = session.send(item_list_request_data.to_requests_prepared_request())
    response.raise_for_status()

    # 5. Decode the raw bytes (response.content) directly into the msgspec Response model
    item_list_response_body = msgspec.json.decode(response.content, type=DMMItemListResponseBody)

    # 6. Enjoy full IDE autocompletion and safe nested data structures!
    print(f"\nTotal items found: {item_list_response_body.result.total_count}")
    print("-" * 40)

    for item in item_list_response_body.result.items:
        print(f"Title: {item.title}")
        print(f"Content ID: {item.content_id}")

        # Safely access normalized integer values
        if item.price_info.price:
            print(f"Price Starts at: {item.price_info.price_start_at}")

        # Thanks to the SDK design, 'actresses' is guaranteed to be an iterable list
        actress_names = [actress.name for actress in item.item_info.actresses]
        if actress_names:
            print(f"Actresses: {', '.join(actress_names)}")

        print("-" * 40)

if __name__ == "__main__":
    main()
```
