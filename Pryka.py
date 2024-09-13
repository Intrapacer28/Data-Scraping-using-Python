import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json

# Function to navigate to a collection page and print product URLs
def process_collection(collection_url, collection_directory):
    # Send an HTTP GET request to the collection URL
    collection_response = requests.get(collection_url)

    # Check if the collection request was successful (status code 200)
    if collection_response.status_code == 200:
        print(f'Successfully navigated to the collection page: {collection_url}')

        # Parse the HTML content of the collection page
        collection_soup = BeautifulSoup(collection_response.text, 'html.parser')

        # Specify the class containing the product information
        product_class = 'nm-shop-loop-thumbnail-link'

        # Find all elements with the specified class
        product_elements = collection_soup.find_all('a', {'class': product_class})

        # Iterate through each product element
        for product_element in product_elements:
            # Extract and print the product URL
            product_url = product_element.get('href')
            full_product_url = urljoin(collection_url, product_url)
            print(f'Product URL: {full_product_url}')

            # Notify about successful navigation to the product page
            process_product(full_product_url, collection_directory)

    else:
        print(f'Failed to navigate to the collection page. Status code: {collection_response.status_code}')

# Function to navigate to a product page and download images
def process_product(product_url, collection_directory):
    # Send an HTTP GET request to the product URL
    product_response = requests.get(product_url)

    # Check if the product request was successful (status code 200)
    if product_response.status_code == 200:
        print(f'Successfully navigated to the product page: {product_url}')

        # Parse the HTML content of the product page
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        # Specify the class containing the product image information
        image_class = 'woocommerce-product-gallery__image'

        # Find all div elements with the specified class
        image_elements = product_soup.find_all('div', {'class': image_class})

        # Extract the product name from the page
        product_name_element = product_soup.find('h1', {'class': 'product_title'})
        product_name = product_name_element.text.strip() if product_name_element else 'Unknown_Product'

        # Create a directory for the product within the collection directory
        product_folder = os.path.join(collection_directory, product_name)
        if not os.path.exists(product_folder):
            os.makedirs(product_folder)

        # Extract the image URLs from the src attribute of img tags and download images
        for index, element in enumerate(image_elements, start=1):
            img_tags = element.find_all('img')
            for img_tag in img_tags:
                img_url = img_tag.get('src')
                # Ensure the image URL is not None
                if img_url:
                    # Construct the absolute image URL
                    full_image_url = urljoin(product_url, img_url)

                    # Determine the file extension (assuming it's always a valid image format)
                    file_extension = full_image_url.split('.')[-1]
                    filename_prefix = f"{index}"

                    # Download and save the image
                    download_image(full_image_url, product_folder, filename_prefix)

        # Specify the class containing the metadata information
        metadata_class = 'nm-tabs-panel-inner entry-content'

        # Find all elements with the specified class
        metadata_elements = product_soup.find_all('div', {'class': metadata_class})

        # Extract the metadata text from the p tags within the specified class
        metadata_text = [p.get_text(separator='\n', strip=True) for metadata_element in metadata_elements
                         for p in metadata_element.find_all('p')]

        # Save metadata to a JSON file in the respective product folder
        metadata_filename = os.path.join(product_folder, 'metadata.json')
        with open(metadata_filename, 'w', encoding='utf-8') as metadata_file:
            json.dump(metadata_text, metadata_file, ensure_ascii=False, indent=4)

        # Notify when metadata is successfully saved
        print(f'Successfully saved metadata for product page: {product_url}')

    else:
        print(f'Failed to navigate to the product page. Status code: {product_response.status_code}')


# Function to download and save images
def download_image(url, folder, filename_prefix):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
    else:
        # Extract the file extension from the URL
        file_extension = url.split('.')[-1].split('?')[0]
        # Construct the filename without special characters
        filename = f"{filename_prefix}.{file_extension}"
        # Remove invalid characters from the filename
        filename = "".join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)
        image_path = os.path.join(folder, filename)

        try:
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            print(f"Image saved: {image_path}")
        except Exception as e:
            print(f"Failed to save image. Error: {e}")

# URL of the starting page
url = 'https://pryka.in/'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Specify the partial class name containing the list information
    partial_list_class = 'menu-item-type-taxonomy'

    # Find the list element that contains the specified partial class
    list_element = soup.find('li', class_=lambda x: x and partial_list_class in x)

    # Check if a list element is found
    if list_element:
        # Create a directory for the website
        website_directory = 'Pryka.in'
        if not os.path.exists(website_directory):
            os.makedirs(website_directory)

        # Find all anchor tags within the list element
        collection_elements = list_element.find_all('a')

        # Iterate through each anchor tag
        for collection_element in collection_elements:
            # Extract collection name from the anchor tag
            collection_name = collection_element.text.strip()

            # Create a directory for each collection in the website directory
            collection_directory = os.path.join(website_directory, collection_name)
            if not os.path.exists(collection_directory):
                os.makedirs(collection_directory)

                # Print the collection name
                print(f'Collection Name: {collection_name}')

                # Extract and print the collection URL
                collection_url = collection_element.get('href')
                full_collection_url = urljoin('https://pryka.in', collection_url)
                print(f'Collection URL: {full_collection_url}')

                # Process the collection page (navigate and print product URLs)
                process_collection(full_collection_url, collection_directory)

    else:
        print(f'No list element with class containing "{partial_list_class}" found.')

else:
    # Print an error message if the request was not successful
    print(f'Failed to fetch page. Status code: {response.status_code}')
