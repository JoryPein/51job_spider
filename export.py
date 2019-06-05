import os
from bs4 import BeautifulSoup
import xlwt


def walk_dir():
    dir_ = './page'
    for item in os.listdir(dir_):
        filename = os.path.normpath(os.path.join(dir_, item))
        if os.path.exists(filename):
            yield filename


def read_soup(location):
    with open(location, 'r') as fp:
        content = fp.read()
    return BeautifulSoup(content, features="lxml")


def get_data():
    for filename in walk_dir():
        soup = read_soup(filename)
        dw_table = soup.find('div', {'class': 'dw_table'})

        for count, item in enumerate(dw_table.findAll('div', {'class': 'el'})):
            if count == 0:
                continue
            span = item.findAll('span')
            data = {
                'work': span[0].text.strip(),
                'detail': span[0].find('a')['href'].strip(),
                'company':span[1].text.strip(),
                'location':  span[2].text.strip(),
                'salary': span[3].text.strip(),
                'date': span[4].text.strip() 
            }
            yield data


def main():
    path_ = 'data/'
    if not os.path.exists(path_):
        os.mkdir(path_)
    c = 0
    count = 0
    worksheet = None
    for data in get_data():
        if count == 0:
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('My Worksheet')
            for index, item in enumerate(['职位', '详情', '公司', '地址', '薪水', '发布日期']):
                worksheet.write(count, index, item)

        count += 1
        for index, item in enumerate(['work', 'detail', 'company', 'location', 'salary', 'date']):
            worksheet.write(count, index, data.get(item))

        if count >= 1000:
            c += 1
            workbook.save(f'{path_}job{c}.xls')
            count = 0


if __name__ == '__main__':
    main()
