import requests
import json
import os
from urllib.parse import urlparse
import copy

def create_dir(folder_name):
    """Create directory if it does not exist."""
    os.makedirs(folder_name, exist_ok=True)

def set_slug(itm_type, base_payload_value):
    """Set the slug based on the item type."""
    if itm_type == "clothing":
        base_payload_value["variables"]["slug"] = "/clothing"
    else :
        base_payload_value["variables"]["slug"] = "/shoes"
    return base_payload_value

def set_page_number(page_number, base_payload_value):
    """Set the page number in the payload."""
    base_payload_value["variables"]["page"] = page_number
    return base_payload_value


def set_designers(base_payload_value, designer):
    ''' Set the designer in the payload.'''
    base_payload_value["variables"]["designers"] = designer
    return base_payload_value

def send_request(url, headers, base_payload_value):
    """Send a POST request to the API."""
    response = requests.post(url, headers=headers, data=json.dumps(base_payload_value))
    if response.status_code != 200:
        print(f"Failed to fetch page {base_payload_value['variables']['page']}: {response.status_code}")
        return None
    return response.json()

def get_product(data):
    '''Extract products from the response data.'''
    products = data.get("data", {}).get("xProductListingPage", {}).get("products", [])
    return products


def get_images(results, nbr_of_images, images_list, Filter):
    '''Extract image URLs from the product results with optional price filter.'''
    for item in results:
        price = item.get("mainPrice", 0)
        print(price)
        if not Filter or price < 100000:
            images = item.get("displayImages", [])
            if images:
                # Replace to get higher-res image
                img_url = images[0].replace("/512/512/", "/1024/1024/")
                images_list.append(img_url)
            if len(images_list) >= nbr_of_images:
                break
    return images_list


def download_images(images_list, save_folder, prefix="img"):
    '''Download images from the list and save them to the specified folder.'''
    os.makedirs(save_folder, exist_ok=True)
    for idx, img_url in enumerate(images_list, start=1):
        try:
            img_data = requests.get(img_url, timeout=10)
            if img_data.status_code == 200:
                ext = os.path.splitext(urlparse(img_url).path)[1]
                file_name = f"{prefix}{idx:03d}{ext}"
                file_path = os.path.join(save_folder, file_name)
                with open(file_path, "wb") as f:
                    f.write(img_data.content)
                print(f"Saved {file_name}")
            else:
                print(f"Failed to download {img_url} - status code: {img_data.status_code}")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")


def create_images_list(url, headers, base_payload_value, save_folder, max_nbr_of_images, item_type, Filter= False):
    '''Create a list of image URLs by fetching data from the API.'''
    create_dir(save_folder)
    images_list = []
    page_number = 1
    base_payload_value = set_slug(item_type,base_payload_value)
    while len(images_list) < max_nbr_of_images:

        base_payload_value = set_page_number(page_number, base_payload_value)

        data = send_request(url, headers, base_payload_value)

        if not data:
            break

        products = get_product(data)
        if not products:
            break

        images_list = get_images(products, max_nbr_of_images, images_list, Filter)

        page_number += 1

    print(f"Collected {len(images_list)} image URLs.")
    download_images(images_list, save_folder)




'''--- Main execution block to run the script and collect images from different categories.'''
if __name__ == "__main__":

    # Endpoint
    url = "https://api.mytheresa.com/api"

    # Headers
    headers = {
    "accept": "*/*",
    "accept-language": "en",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://www.mytheresa.com",
    "referer": "https://www.mytheresa.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "x-country": "LB",
    "x-geo": "LB",
    "x-region": "BY",
    "x-section": "women",
    "x-store": "INT"
    }

    # GraphQL payload
    base_payload = {
    "query": """query XProductListingPageQuery($categories: [String], $colors: [String], $designers: [String], $fta: Boolean, $materials: [String], $page: Int, $patterns: [String], $reductionRange: [String], $saleStatus: SaleStatusEnum, $size: Int, $sizesHarmonized: [String], $slug: String, $sort: String) {
      xProductListingPage(categories: $categories, colors: $colors, designers: $designers, fta: $fta, materials: $materials, page: $page, patterns: $patterns, reductionRange: $reductionRange, saleStatus: $saleStatus, size: $size, sizesHarmonized: $sizesHarmonized, slug: $slug, sort: $sort) {
        pagination {
          currentPage
          totalPages
          totalItems
        }
        products {
          name
          designer
          slug
          displayImages
          mainPrice
        }
      }
    }""",
    "variables": {
        "categories": [],
        "colors": [],
        "designers": [],
        "fta": None,
        "materials": [],
        "page": 1,
        "patterns": [],
        "reductionRange": [],
        "saleStatus": None,
        "size": 60,
        "sizesHarmonized": [],
        "slug": "",
        "sort": None
    }

    }

    # part1: Collecting images for clothing
    images_list_random = create_images_list(url, headers, copy.deepcopy(base_payload), "Task1/women_clothing",1000, "clothing")

    # part2: Collecting images for saint_laurent clothing
    base_payload_designer = set_designers(copy.deepcopy(base_payload), "Saint Laurent")
    images_list_designer = create_images_list(url, headers, base_payload_designer, "Task1/saint_laurent", 50,"clothing")

    # part3: Collecting images for price range clothing
    images_list_price_range = create_images_list(url, headers, copy.deepcopy(base_payload), "Task1/under_1000",20,"clothing",True)

    # part4: Collecting images for shoes
    images_list_shoes = create_images_list(url, headers, copy.deepcopy(base_payload), "Task1/shoes", 100,"shoes")


