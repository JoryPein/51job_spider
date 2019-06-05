import requests
import os
import threading
from queue import Queue
from urllib.parse import quote


def save_html(task):
    count = task.get('count')
    url = task.get('url')
    try:
        print(f'downloading page{count}...')
        resp = requests.get(url)
        resp_content = resp.content
        with open(f'{my_dir}page{count}.html', 'wb') as fp:
            fp.write(resp_content)
    except:
        print(f'missed {url}')


class MyThread(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()

    def run(self):
        while True:
            try:
                task = self.queue.get_nowait()
                save_html(task)
                self.queue.task_done()
            except Exception:
                break


class MyThreadPool:

    def __init__(self, task_queue, size):
        self.thread_pool = []
        for i in range(size):
            self.thread_pool.append(MyThread(task_queue))

    def joinAll(self):
        for thread_ in self.thread_pool:
            if thread_.isAlive():
                thread_.join()


my_dir = 'page/'
if not os.path.exists(my_dir):
    os.mkdir(my_dir)


def result_page_url():
    keyword = quote(quote('销售'))
    page_range = 2000
    for page_num in range(0, page_range):
        url = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{page_num+1}.html'
        yield url


def main():
    task_queue = Queue()
    for count, url in enumerate(result_page_url()):
        task = {
            'count': count+1,
            'url': url
        }
        task_queue.put(task)

    pool = MyThreadPool(task_queue=task_queue, size=800)
    pool.joinAll()


if __name__ == '__main__':
    main()
