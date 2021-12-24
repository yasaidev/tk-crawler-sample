from typing import Dict, List
from requests_html import AsyncHTMLSession, HTMLSession
import tkinter
import asyncio
import threading
from dataclasses import dataclass
import os


class GUI:
    # GUI class
    def __init__(self, master):
        # make dir for save
        os.makedirs('./html', exist_ok=True)

        # load utl_list.txt
        self.url_dic_list: Dict[str, bool] = {}
        with open('url_list.txt', 'r') as f:
            for line in f:
                if(line.strip() != ''):
                    self.url_dic_list.update({line.strip(): False})

        self.master = master
        master.title("tk_crawler_sample")
        master.geometry("400x400")
        self.button = tkinter.Button(
            master, text="Crawl", command=self.crawler)
        self.button.pack()
        self.label = tkinter.Label(master, text="Done URLs:")
        self.label.pack()
        self.text = tkinter.Text(master)
        self.text.pack()

    def html_get(self, url: str) -> None:
        # html get function
        with HTMLSession() as session:
            try:
                response = session.get(url)
            except:
                # update url_dic_list
                self.url_dic_list.update({url: True})
                return None

            self.text.insert(tkinter.END, url + '\n')

            # save html to file with domain from url as filename
            with open("./html/"+url.split('/')[2] + '.html', 'w', encoding='UTF-8') as f:
                f.write(response.html.html)

            # update url_dic_list
            self.url_dic_list.update({url: True})

            # check if all urls are done
            if(all(self.url_dic_list.values())):
                self.text.insert(tkinter.END, 'Done!')
                self.button.config(state=tkinter.NORMAL)
                return None

    # crawl function
    def crawler(self):
        # disable button (cannot click twice)
        # when crawling done button will be enabled (in html_get function)
        self.button.config(state=tkinter.DISABLED)

        # make threads
        threads = [threading.Thread(target=self.html_get, args=(x,))
                   for x in self.url_dic_list.keys()]

        # run threads parallelly
        for thread in threads:
            thread.start()
            # joinでスレッドが終了するまで待つと，ブロッキング（処理待ち）が発生してGUIスレッドに制御が戻らないので固まる
            # thread.join()

    # asyncio verはAttributeError: __aexit__でエラーが出るので一旦放置
    # async def html_get_async(self, url: str) -> str:
    #     # async html get function
    #     async with AsyncHTMLSession() as session:
    #         response = await session.get(url)
    #         self.text.insert(tkinter.END, url + '\n')
    #         # save html to file with domain from url as filename
    #         with open(url.split('/')[2] + '.html', 'w') as f:
    #             f.write(response.html.html)
    #         return response.html.html

    # def crawler_async(self):
    #     # load url_list.txt
    #     url_list = []
    #     with open('url_list.txt', 'r') as f:
    #         for line in f:
    #             url_list.append(line.strip())

    #     # pararell crawl
    #     task_list = [self.html_get_async(x) for x in url_list]

    #     # make a loop
    #     loop = asyncio.new_event_loop()

    #     # run the loop
    #     loop.run_until_complete(asyncio.wait(task_list))
    #     self.text.insert(tkinter.END, 'Done!')


if __name__ == "__main__":
    root = tkinter.Tk()
    gui = GUI(root)
    root.mainloop()
