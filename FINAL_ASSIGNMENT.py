from bs4 import BeautifulSoup
import requests, csv


source = requests.get('https://www.coursef.com').text
soup = BeautifulSoup(source, 'lxml')

bottom_divs = soup.find_all('div', class_='col-md-3')
main_cat_divs =  soup.find_all('div', class_='card-body')
div_collection = main_cat_divs + bottom_divs

csvfile =  open("DATA.csv", "w", encoding='utf-8', newline="") 
writer = csv.writer(csvfile)
writer.writerow(["TITLE","LINK"])

check_repitition = []


def navigateSubLinks(current_sub_link):

    samp_soup = BeautifulSoup(requests.get(f'https://www.coursef.com/{current_sub_link}').text, 'lxml')
    if current_sub_link.find('%') > 0:
        right_end = min(current_sub_link.find('&'),current_sub_link.find('%'))
    else:
        right_end = current_sub_link.find('&')

    part_link = 'https://www.coursef.com/'+current_sub_link[current_sub_link.find('=')+1:right_end].replace('+','-')
    check_repitition.append(part_link)

    try:
        part_title = samp_soup.find('h1').text
        writer.writerow([part_title,part_link])
        
    except AttributeError:
        part_title = "No Title" #I found some dead end links which keeps on loading.... and returns a fail statement that's why the deadlink has no attribute of h1, so not storing that in csv



    # FOR CHAINING THROUGH LINKS
    for a in samp_soup.find_all('a',class_='kw_related'):
        if a.get('data-link').find('%') > 0:
            right_end = min(a.get('data-link').find('&'),a.get('data-link').find('%'))
        else:
            right_end = a.get('data-link').find('&')
        x = 'https://www.coursef.com/'+a.get('data-link')[a.get('data-link').find('=')+1:right_end].replace('+','-')
        if x not in check_repitition:
            navigateSubLinks(a.get('data-link'))


# FOR CATEGORIZED COURSES
for div in div_collection:

    for p in div.find_all('p'):

        course_link_val = 'https://www.coursef.com'+ p.find('a').get('href')
        soup1 = BeautifulSoup(requests.get(course_link_val).text, 'lxml')
        title = soup1.find('h1').text
        writer.writerow([title,course_link_val])

        for a in soup1.find_all('a',class_='kw_related'):
            navigateSubLinks(a.get('data-link'))


# # FOR COURSES IN PAGINATORS
paginator = 1
while requests.get(f'https://www.coursef.com/course?page={paginator}').text: #will be true until the page exists (goes till last page)
    sourceC = requests.get(f'https://www.coursef.com/course?page={paginator}').text
    soupC = BeautifulSoup(sourceC, 'lxml')

    for div in soupC.find_all('div', class_='col-md-3'):

        for link in div.find_all('a', class_='stretched-link'):
            course_link_val = link.get('href')
            course_title_source = requests.get(course_link_val).text
            soup1C = BeautifulSoup(course_title_source, 'lxml')
            course_link = course_link_val
            sample_title = "No Title"
            try:
                title = soup1C.find('h1').text
            except AttributeError: #if the course is without title. I found one at "https://www.coursef.com/course?page=14"
                title = sample_title

            writer.writerow([title,course_link])
    paginator += 1


# FOR BLOGS IN PAGINATORS
blog_paginator = 1
while requests.get(f'https://www.coursef.com/blog?page={blog_paginator}').text: #will be true until the page exists (goes till last page)
    sourceB = requests.get(f'https://www.coursef.com/blog?page={blog_paginator}').text
    soupB = BeautifulSoup(sourceB, 'lxml')

    for link in soupB.find_all('a', class_='stretched-link'):
        course_link_val = link.get('href')
        course_title_source = requests.get(course_link_val).text
        soup1B = BeautifulSoup(course_title_source, 'lxml')
        blog_link = course_link_val
        sample_title = "No Title"
        try:
            title = soup1B.find('h1').text
        except AttributeError: #if the blog is without title.
            title = sample_title

        writer.writerow([title,blog_link])
blog_paginator += 1


# TOP KEYWORDS
div1 = soup.find_all('div', class_='col-md-4')[1]
for div in div1.find_all('div', class_='text-truncate'):
    for a in div.find_all('a'):
        link_val = 'https://www.coursef.com/'+ a.get('href')
        soupx = BeautifulSoup(requests.get(link_val).text, 'lxml')
        title = soupx.find('h1').text

        writer.writerow([title,link_val])

        for a in soupx.find_all('a',class_='kw_related'):
            navigateSubLinks(a.get('data-link'))

csvfile.close()





