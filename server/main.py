import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Function to fetch and modify HTML from a given URL
def fetch_and_modify_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the page, status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove the header using the CSS selector
    header = soup.select_one('div > header')
    if header:
        header.decompose()  # This removes the element from the tree

    # Using CSS selectors to locate the contributor's list
    contributor_list_selector = 'div > div > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(5) > div > ul'
    contributors_ul = soup.select_one(contributor_list_selector)

    if contributors_ul:
        # Find all the 'a' elements within the ul that contain contributor information
        contributor_links = contributors_ul.select('li > a[data-hovercard-type="user"]')

        # Create a new ul element to store our list of contributors' usernames
        new_contributors_list = soup.new_tag('ul')

        # Loop over all the contributor 'a' elements and extract the username
        for link in contributor_links:
            username = link.img['alt'].lstrip('@') if link.img else 'unknown'
            # Create a new li element for each contributor, add tabindex attribute, and add it to the new_contributors_list
            li = soup.new_tag('li', tabindex="0")
            li.string = username
            new_contributors_list.append(li)

        # Replace the old avatars list with our new text-based list
        contributors_ul.replace_with(new_contributors_list)

    return soup


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/clean", methods=['POST'])
def clean():
    print("Request received")
    data = request.json
    url = data.get('url', '')

    # Fetch and modify HTML
    modified_soup = fetch_and_modify_html(url)

    if isinstance(modified_soup, BeautifulSoup):
        # Convert the modified BeautifulSoup object to a string
        html_content = str(modified_soup)
        return jsonify({"modifiedHtml": html_content})
    else:
        # Return the error message if retrieval was unsuccessful
        return jsonify({"error": modified_soup}), 500


if __name__ == "__main__":
    app.run(debug=True)
