import random
import re
import time

import numpy
from selenium import webdriver
import csv


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def write_in_csv(filename, data, n):
    with open(filename + '.csv', mode='a+') as wr_file:
        scriitor = csv.writer(wr_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        scriitor.writerow([data, n])


def makes_decision(flag, data):
    # bad
    if flag == 'warning':
        write_in_csv('bad', data, 0)
    # good
    elif flag == 'success':
        write_in_csv('good', data, 1)
    # put neutral data with gauss distribution
    else:
        if numpy.random.normal() > 0.0:
            write_in_csv('good', data, 1)
        else:
            write_in_csv('bad', data, 0)


def getMatches(driver):
    all_discusion = driver.find_elements_by_xpath("//*[contains(text(), 'Discussion')]")
    feeling = []
    new_links = []
    my_texts = []
    for discusion in all_discusion:
        feeling.append(
            str(discusion.find_element_by_xpath('..').find_element_by_tag_name("span").get_attribute("class")).replace(
                'badge badge-', ''))
        new_links.append(discusion.get_attribute("href"))

    match = []

    # for each link get my text
    count = 0
    for link in new_links:
        driver.get(link)
        wait_some_sec()
        try:
            leaf = driver.find_element_by_tag_name("blockquote")
            my_texts.append(striphtml(leaf.text).replace('Privacy Policy', '').replace('Terms of Service', '').replace(
                'Data Policy', ''))
            match.append({'feel': feeling[count], 'clause': my_texts[count]})
            count += 1
        except:
            print("Unusefull info.")
        print(f"Complete {count}/{len(new_links)}")

    return match


def wait_some_sec():
    wait_time = random.randint(0, 9)
    print(f"Wait {wait_time}")
    time.sleep(wait_time)


if __name__ == '__main__':
    driver = webdriver.Chrome("./ph-chrome/chromedriver")
    driver.get('https://tosdr.org/')

    all_sites = driver.find_elements_by_xpath("//*[contains(text(), 'More details')]")

    collector = []
    count = 0
    keep_index = 0
    n_pages = len(all_sites)
    for i in range(200, 300):
        try:
            wait_some_sec()
            all_sites = driver.find_elements_by_xpath("//*[contains(text(), 'More details')]")
            all_sites[i].click()
            items = getMatches(driver)
            collector.append(items)

            # WRITE DATA IN CSV_FILE:
            for item in items:
                print(item)
                makes_decision(item['feel'], item['clause'])

            count += 1
            # reset on the initial site
            wait_some_sec()
            driver.get('https://tosdr.org/')
            print(f"Complete collect data: {count}/{len(all_sites)}")

        except Exception as e:
            print(e)

    print("Done.")
