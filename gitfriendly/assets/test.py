from bs4 import BeautifulSoup
import webbrowser



with open('modified_github_page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()


# Parsing the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# 1. Improve the "Skip to content" link
skip_to_content = soup.find("a", class_="js-skip-to-content")
if skip_to_content:
    skip_to_content['href'] = "#main-content"
    skip_to_content['role'] = "link"

# Assuming a 'main' content area for the skip to link to focus on
if not soup.find("main"):
    main_content = soup.new_tag("main", id="main-content")
    body_content = soup.body.extract()
    main_content.append(body_content)
    soup.body.append(main_content)

# 2. Add ARIA roles to navigation elements
nav_elements = soup.find_all("nav")
for nav in nav_elements:
    nav['role'] = 'navigation'

# 3. Add alt text to images
images = soup.find_all("img")
for img in images:
    if not img.has_attr('alt'):
        img['alt'] = "Descriptive text missing"  # Placeholder text

# Convert the updated BeautifulSoup object back to string
updated_html_content = str(soup)

# Save the updated HTML to a new file
new_html_file_path = 'accessible_modified_github_page.html'
with open(new_html_file_path, 'w', encoding='utf-8') as new_file:
    new_file.write(updated_html_content)
    # open the file in the browser
    webbrowser.open('file:///Users/adamsulemanji/Desktop/College/SPRING2024/CSCE689-AC/test/accessible_modified_github_page.html')
