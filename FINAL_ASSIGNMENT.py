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

check_repetition = []

def navigateSubLinks(current_sub_link):

    samp_soup = BeautifulSoup(requests.get(f'https://www.coursef.com/{current_sub_link}').text, 'lxml')
    part_link = 'https://www.coursef.com/'+current_sub_link[current_sub_link.find('=')+1:current_sub_link.find('&')].replace('+','-')
    check_repetition.append(part_link)

    try:
        part_title = samp_soup.find('h1').text
    except AttributeError:
        part_title = "No Title"

    writer.writerow([part_title,part_link])

    # FOR CHAINING THROUGH LINKS
    for a in samp_soup.find_all('a',class_='kw_related'):
        x = 'https://www.coursef.com/'+a.get('data-link')[a.get('data-link').find('=')+1:a.get('data-link').find('&')].replace('+','-')
        if x not in check_repetition:
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


# FOR BLOGS AND COURSES IN PAGINATORS
paginator = 1
while requests.get(f'https://www.coursef.com/course?page={paginator}').text: #will be true until the page exists (goes till last page)
    sourceCB = requests.get(f'https://www.coursef.com/course?page={paginator}').text
    soupCB = BeautifulSoup(sourceCB, 'lxml')

    for div in soupCB.find_all('div', class_='col-md-3'):

        for link in div.find_all('a', class_='stretched-link'):
            course_link_val = link.get('href')
            course_title_source = requests.get(course_link_val).text
            soup1CB = BeautifulSoup(course_title_source, 'lxml')
            course_link = course_link_val
            sample_title = "No Title"
            try:
                title = soup1CB.find('h1').text
            except AttributeError: #if the course is without title. I found one at "https://www.coursef.com/course?page=14"
                title = sample_title

            writer.writerow([title,course_link])
    paginator += 1

csvfile.close()


