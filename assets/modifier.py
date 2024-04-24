import requests
from bs4 import BeautifulSoup
import webbrowser

def clean(url):
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the page, status code: {response.status_code}"

    # dump clean html to file
    with open('github_page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

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

    # Remove unnecessary elements
    for selector in ['div > header', 'footer', '.flash']:
        element = soup.select_one(selector)
        if element:
            element.decompose()

    # Improve navigation by adding ARIA landmarks
    navigation_elements = soup.find_all('nav')
    for index, nav in enumerate(navigation_elements):
        nav['role'] = 'navigation'
        nav['aria-label'] = f'Navigation {index + 1}'

    # Ensure images have alt attributes
    for img in soup.find_all('img'):
        if not img.get('alt', '').strip():
            img['alt'] = 'Image description missing'

    # Add semantic elements
    main_content = soup.select_one('#main-content')
    if main_content:
        main_content.name = 'main'

    # Find all style tags and inline styles to remove animations
    for style in soup.find_all('style'):
        css_text = style.string
        # Remove any CSS animations and transitions
        css_text = css_text.replace('animation:', '/* disabled animation: */')
        css_text = css_text.replace('transition:', '/* disabled transition: */')
        style.string = css_text

    for tag in soup.find_all(style=True):
        inline_style = tag['style']
        # Remove any inline CSS animations and transitions
        if 'animation' in inline_style or 'transition' in inline_style:
            inline_style = inline_style.replace('animation', '/* disabled animation')
            inline_style = inline_style.replace('transition', '/* disabled transition')
            tag['style'] = inline_style

    # Disable JavaScript that could trigger animations
    for script in soup.find_all('script'):
        if 'animation' in script.text or 'transition' in script.text:
            script.decompose()  # Remove scripts that mention animations

    # Remove headers, footers, and unnecessary elements
    for selector in ['header', 'footer', '.flash', 'div#footer', 'nav[role="navigation"]']:
        for element in soup.select(selector):
            element.decompose()

    # Set the language of the page
    html = soup.find('html')
    html['lang'] = 'en'

    # Add skip navigation link
    body = soup.find('body')
    skip_nav = soup.new_tag('a', href="#main", **{'class': 'skip-link'})
    skip_nav.string = "Skip to main content"
    body.insert(0, skip_nav)

    # Main content area
    # main = soup.new_tag('main', id='main')
    # content_selector = '#js-repo-pjax-container, #repository-container-header, #start-of-content'
    # for content in soup.select(content_selector):
    #     main.append(content.extract())
    # body.insert(1, main)

    # Enhance accessibility in forms and inputs
    for input_tag in soup.find_all('input'):
        if 'type' not in input_tag.attrs or input_tag['type'] == 'text':
            label = soup.new_tag('label')
            label['for'] = input_tag['id']
            label.string = 'Enter your information:'
            input_tag.insert_before(label)

    # Remove all JavaScript to prevent dynamic content change issues
    for script in soup.find_all('script'):
        script.decompose()

    # Improve link accessibility
    for a in soup.find_all('a'):
        if not a.get('title'):
            a['title'] = a.get_text(strip=True)

    # Remove inline styles that may include animations
    for tag in soup.find_all(style=True):
        del tag['style']

    # Remove SVG icons
    for svg in soup.find_all('svg'):
        svg.decompose()

    # Remove IMG tags that are often used for icons
    for img in soup.find_all('img'):
        img.decompose()

    # Remove animations from all style tags (for inline and internal CSS)
    for style in soup.find_all('style'):
        css = style.string
        if css:
            # Remove animations and transitions
            css = css.replace('animation:', '/* disabled animation: */')
            css.replace('transition:', '/* disabled transition: */')
            style.string = css

    # Also, consider removing links to external JS files that might control animations
    for script in soup.find_all('script'):
        script.decompose()

        # Adding tabindex="0" to elements that should be focusable
    for link in soup.find_all('a'):
        link['tabindex'] = '0'

    for btn in soup.find_all('button'):
        btn['tabindex'] = '0'

    # Ensuring all input elements are focusable and have labels
    for input_elem in soup.find_all('input'):
        input_elem['tabindex'] = '0'
        if not input_elem.has_attr('id'):
            input_elem['id'] = input_elem.get('name', 'input') + '_id'
        if not soup.find('label', {'for': input_elem['id']}):
            # Create a label if none exists
            label = soup.new_tag('label')
            label['for'] = input_elem['id']
            label.string = 'Input:'
            input_elem.insert_before(label)

    # Adding visual focus indicators via internal CSS
    styles = soup.find('style')
    if not styles:
        styles = soup.new_tag('style')
        soup.head.append(styles)
    
    packages_section = soup.find('div', {'id': 'section_id_or_class'})
    if packages_section:
        packages_section.decompose()


    # Set viewport for mobile accessibility
    meta_viewport = soup.new_tag('meta', attrs={'name': 'viewport', 'content': 'width=device-width, initial-scale=1'})
    head = soup.find('head')
    head.append(meta_viewport)

    # dump clean html to file
    updated_html_content = str(soup)
    with open('cleaned_github_page.html', 'w', encoding='utf-8') as file:
        file.write(updated_html_content)

    # open up the cleaned html in browser
    # webbrowser.open('file:///Users/adamsulemanji/Desktop/College/SPRING2024/CSCE689-AC/GitFriendly/assets/cleaned_github_page.html')
    webbrowser.open('file:/Users/nikki/Library/CloudStorage/OneDrive-TexasA&MUniversity/YEAR FOUR/SPRING 2024/CSCE 432/GitFriendly/assets/cleaned_github_page.html')



clean('https://github.com/adamsulemanji/GitFriendly')