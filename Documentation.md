# Pryka Scraper Documentation

## Overview

The Pryka Scraper is a Python script that scrapes Pryka.in for product information. It collects product URLs, images, and metadata for each product in various collections.

## Modules and Dependencies

- `requests`: For sending HTTP requests to Pryka.in.
- `bs4` (BeautifulSoup): For parsing the HTML content of the web pages.
- `os`: For directory management.
- `json`: For saving product metadata in JSON format.
- `urllib.parse.urljoin`: For combining URLs to ensure absolute paths.

## Key Functions

### `process_collection(collection_url, collection_directory)`
This function processes a collection page by:
- Sending a GET request to the collection URL.
- Parsing the HTML to find product links.
- Iterating over product links and sending them to `process_product` for further processing.

### `process_product(product_url, collection_directory)`
This function processes a product page by:
- Sending a GET request to the product URL.
- Extracting product images and downloading them.
- Extracting and saving product metadata in a JSON file.

### `download_image(url, folder, filename_prefix)`
Downloads an image from the given URL and saves it to the specified folder with a unique filename.

## How It Works

1. **Navigating the Main Page**:
   - The script sends a GET request to `https://pryka.in/` and looks for product collections.
   
2. **Processing Collections**:
   - For each collection, a separate folder is created. The product URLs are extracted, and the script navigates to each product page.
   
3. **Processing Products**:
   - For each product, images are downloaded and saved in the respective folder. Product metadata is also collected and saved in a JSON file.
   
4. **Saving Images and Metadata**:
   - Images are downloaded using the `requests.get()` method, and metadata is saved in JSON format for each product.

## Error Handling

- If the script encounters an HTTP error (e.g., the server is down), it prints the error details and moves to the next item.

## Future Improvements

- Add multi-threading for faster scraping.
- Handle pagination for collections with more products.

## Conclusion

This script can be extended to handle more complex scraping scenarios, including paginated collections or sites with AJAX-loaded content.
