import tkinter as tk
import threading
import webbrowser
import time
import psutil
import datetime

'''
# 打印程序说明
print("请认真阅读教程，设置好浏览器后再开始操作！")

# 检测浏览器是否处于打开状态
def is_edge_running():
    # 在Windows上，Edge的进程名通常是'msedge.exe'
    edge_process_names = ['msedge.exe', 'MicrosoftEdge.exe']
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in edge_process_names:
            return False
    return True


# 获取用户输入的专题网址
urls_input = input("输入专题网址，用空格分隔多个网址: ")

# 使用split方法分割字符串，获得专题网址列表
urls = urls_input.split()  # 分割网址字符串

# 初始化计数器
counter = 0

# 遍历网址列表
for url in urls:
    counter += 1  # 增加计数器，用于记录是第几次循环

    # 打开新的浏览器标签页
    webbrowser.open_new_tab(url)
    print(f"已打开第{counter}个专题的网页，正在进行学习")

    # 等待指定的时间
    time.sleep(1200)
    print(f"第{counter}个专题已学习1200秒，准备开始检测是否学习完毕")

    # 循环检查条件，直到满足
    while not is_edge_running():

        # 使用datetime模块获取并打印当前时间
        now = datetime.datetime.now()
        print("此刻时间:", now.strftime('%H:%M:%S'),f"第{counter}个专题还未学习完成，600秒后将再次检测")

        time.sleep(600)  # 等待600秒
    print(f"第{counter}个专题已学习完毕，准备开始学习下一个专题")
print("所有专题学习完毕，请关闭软件。")

'''

class LearningApp:
    def __init__(self, master):

        # 设置不同的字体大小
        label_font = ('Arial', 16)  # 标签字体大小
        button_font = ('Arial', 13)  # 按钮字体大小
        log_font = ('Arial', 11)  # 日志显示区字体大小

        self.master = master
        master.title("Learning App")

        self.running = False
        self.stop_flag = threading.Event()  # 使用Event对象来控制线程的停止

        # 左侧的输入框和按钮
        self.left_frame = tk.Frame(master)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.left_frame, text="请输入专题网址，用空格分隔多个网址:", font=label_font)
        self.label.pack(pady=20)

        # 使用Text控件代替Entry，设置wrap=tk.WORD以实现自动换行
        self.text_input = tk.Text(self.left_frame, width=80, height=5, wrap=tk.WORD)
        self.text_input.pack()

        # 创建一个新框架来容纳两个按钮
        button_frame = tk.Frame(self.left_frame)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="开始学习", command=self.start_learning, width=20, height=2,font=button_font)
        self.start_button.grid(row=0, column=0, sticky="ew", padx=5)

        self.stop_button = tk.Button(button_frame, text="终止", command=self.stop_learning, state=tk.DISABLED, width=20, height=2,font=button_font)
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=5)

        # 添加日志显示区域
        self.log_text = tk.Text(self.left_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.configure(state=tk.DISABLED)  # 设置为只读状态

        # 右侧的信息显示区域
        self.right_frame = tk.Frame(master, bg='lightgray')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        today = datetime.date.today().strftime("%Y-%m-%d")
        # 使用Message控件，设置wraplength参数使得文本自动换行
        self.info_message = tk.Message(self.right_frame,text="软件信息\n\n版本: 1.0\n\n作者:GitHub@caspiankexin\n\n软件说明：请联系作者了解使用教程。\n\n免责声明：软件仅供技术学习交流，不得进行传播和滥用，不得用于违规活动。\n\n提醒：仅在win11环境下测试，其他系统效果未知。",justify=tk.LEFT, bg='lightgray', width=200,font=log_font)  # 200可以根据实际需要调整
        self.info_message.pack(padx=40, pady=10, fill=tk.BOTH)

        # 设置窗口大小和位置
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # 调整窗口大小，这里使用屏幕宽度和高度的3/4作为示例
        master.geometry(f"{int(screen_width * 0.75)}x{int(screen_height * 0.75)}")

    def append_to_log(self, message):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)  # 自动滚动到底部
        self.log_text.configure(state=tk.DISABLED)

    def start_learning(self):
        if self.running:
            self.append_to_log("警告: 学习已经在进行中！")
            return

        self.running = True
        self.stop_flag.clear()  # 清除停止标记
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # 在读取输入时，确保移除换行符
        urls_input = self.text_input.get("1.0", "end-1c").replace("\n", " ")
        urls = urls_input.split()

        # 启动新线程来执行学习任务
        thread = threading.Thread(target=self._learning_thread, args=(urls,))
        thread.start()

    def _learning_thread(self, urls):
        # 初始化计数器
        counter = 0

        for url in urls:
            if self.stop_flag.is_set():
                break

            counter += 1

            # 打开新的浏览器标签页
            webbrowser.open_new_tab(url)
            self.append_to_log(f"正在打开第{counter}个专题的网页进行学习")

            # 等待指定的时间
            try:
                time.sleep(600)  # 注意这里的时间单位是秒
                self.append_to_log(f"第{counter}个专题已学习600秒，准备检测是否学习完毕")

                # 循环检查条件，直到满足
                while self.is_edge_running() and not self.stop_flag.is_set():
                    # 使用datetime模块获取并打印当前时间
                    now = datetime.datetime.now()
                    self.append_to_log(
                        f"此刻时间: {now.strftime('%H:%M:%S')} 第{counter}个专题还未学习完成，600秒后将再次检测")
                    time.sleep(600)  # 注意这里等待的时间单位是秒
                self.append_to_log(f"第{counter}个专题已学习完毕，准备开始学习下一个专题")
            except Exception as e:
                self.append_to_log(f"错误: {str(e)}")
                break

        if not self.stop_flag.is_set():
            self.append_to_log("所有专题学习完毕，请关闭软件。")
        else:
            self.append_to_log("程序已终止。")

        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def stop_learning(self):
        self.stop_flag.set()  # 设置停止标记，这将使线程退出循环
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def is_edge_running(self):
        edge_process_names = ['msedge.exe', 'MicrosoftEdge.exe']
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] in edge_process_names:
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = LearningApp(root)
    root.mainloop()