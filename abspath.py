'''
已成功链接到c源代码
'''
import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import subprocess
import sys

window = tk.Tk()
window.title("数据安全课程设计")
window.geometry("1000x800")

# 进度条相关变量
progress_bars = []
loading_label = None

# 输入变量相关控件
input_labels = []
input_entries = []
submit_button = None  # 添加提交按钮变量

def start():
    tk.messagebox.showwarning(
        title='提醒',message='本软件包含缓冲区溢出漏洞，仅供实验使用')
    b1_start.place_forget()
    show_progress()

def show_progress():
    global loading_label
    # 创建"加载中"标签
    loading_label = tk.Label(window, text="加载中……", font=("Arial", 60))
    loading_label.place(x=500, y=280, anchor='center')
    
    # 创建进度条标签
    for i in range(20):
        label = tk.Label(window, bg='lightblue', width=4, height=2)
        label.place(x=200 + i*30, y=500)
        progress_bars.append(label)
    
    # 启动进度条动画线程
    threading.Thread(target=animate_progress, daemon=True).start()

def animate_progress():
    # 依次点亮进度条
    for i in range(20):
        # 使用after方法确保UI更新在主线程中进行
        window.after(i*100, 
                    lambda idx=i: progress_bars[idx].config(bg='blue'))
        time.sleep(0.1)
    
    # 全部完成后变红
    window.after(2000, finish_progress)

def finish_progress():
    for bar in progress_bars:
        bar.config(bg='red')
    
    # 1秒后清除进度条和加载中文字，并显示软件使用说明
    window.after(1000, clear_progress_and_show_instructions)

def clear_progress_and_show_instructions():
    global loading_label
    # 清除进度条
    for bar in progress_bars:
        bar.place_forget()
    # 清除加载中文字
    if loading_label:
        loading_label.place_forget()
    
    # 显示软件使用说明弹窗
    tk.messagebox.showinfo(title='README', 
        message='您可以在软件内设置想要的校园跑打卡数据')
    
    # 在主窗口中加载输入变量
    show_input_fields()

def show_input_fields():
    global submit_button
    # 定义要显示的变量名称
    variables = [
        "用户名", "日期", "时间", "地点", "天气", "温度",
        "运动里程", "训练时长", "运动消耗", "总时长", "平均步频"
    ]
    
    # 创建标签和输入框
    for i, var_name in enumerate(variables):
        # 创建标签
        label = tk.Label(window, text=var_name, font=("Arial", 12))
        label.place(x=200, y=100 + i*40)
        input_labels.append(label)
        
        # 创建输入框
        entry = tk.Entry(window, font=("Arial", 12))
        entry.place(x=300, y=100 + i*40)
        input_entries.append(entry)
    
    # 创建提交按钮
    submit_button = tk.Button(window, text="提交", font=("Arial", 16), 
                             command=on_submit_click)
    submit_button.place(x=500, y=100 + len(variables)*40 + 20, anchor='center')

def hex_to_binary(hex_str):
    """将十六进制字符串转换为二进制字节"""
    # 移除可能存在的空格和换行符
    hex_str = hex_str.strip().replace(' ', '').replace('\n', '')
    # 确保是偶数长度
    if len(hex_str) % 2 != 0:
        raise ValueError("十六进制字符串长度必须为偶数")
    try:
        return bytes.fromhex(hex_str)
    except ValueError:
        raise ValueError("输入包含无效的十六进制字符")

def on_submit_click():
    """提交按钮点击事件处理函数"""
    # 创建一个新的顶层窗口用于输入激活码
    activation_window = tk.Toplevel(window)
    activation_window.title("输入激活码")
    activation_window.geometry("300x150")
    
    # 添加提示标签
    label = tk.Label(activation_window, text="请输入激活码:", font=("Arial", 12))
    label.pack(pady=10)
    
    # 添加输入框
    activation_entry = tk.Entry(activation_window, font=("Arial", 12), width=25)
    activation_entry.pack(pady=10)
    
    # 添加确认按钮
    def confirm_activation():
        activation_code = activation_entry.get()
        activation_window.destroy()
        # 调用C程序并传递激活码作为参数
        execute_c_program(activation_code)
    
    confirm_button = tk.Button(activation_window, text="确认", font=("Arial", 12),
                              command=confirm_activation)
    confirm_button.pack(pady=10)

#相对路径
#def apppath():
#    '''返回exe地址'''
#    if getattr(sys, 'frozen', False):
#        return os.path.dirname(sys.executable)
#    else:
#        return os.path.dirname(os.path.abspath(__file__))

def execute_c_program(activation_code):
    """执行C程序并传递激活码作为参数"""
    try:
        # 将十六进制激活码转换为二进制
        try:
            binary_payload = hex_to_binary(activation_code)
        except ValueError as e:
            tk.messagebox.showerror("输入错误", f"激活码格式错误: {e}")
            return
        
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 切换到包含try.c的目录（假设在同一个目录或指定目录）
        # 你可能需要根据实际情况调整这个路径
#    target_dir = script_dir  # 或者指定其他目录
        c_file_path = r"C:\\Users\\39761\\Desktop\\codeforkeshe\\fake.c"
        exe_file_path = r"C:\\Users\\39761\\Desktop\\codeforkeshe\\fake.exe"

        # 编译try.c文件
#        print("正在尝试编译try.c...")
        compile_process = subprocess.run(["gcc",c_file_path, 
                                      "-o", exe_file_path,
                                      "-static"], 
                                       cwd=script_dir,
                                       capture_output=True, text=True)
        
#        if compile_process.returncode != 0:
#            tk.messagebox.showerror("编译错误", f"编译try.c时出现错误:\n{compile_process.stderr}")
#            return
        
        # 执行编译后的程序，并将激活码作为参数传递
        result = subprocess.run([exe_file_path], 
                              input=binary_payload, 
                              cwd=script_dir,
                              shell=True,
                              capture_output=True,
                              encoding='utf-8',
                              timeout=10)
        
        # 显示执行结果
        result_message = f"程序执行结果:\n"
        result_message += f"{"标准输出:", result.stdout}\n"
#        if result.stderr:
#            result_message += f"{result.stderr.decode(errors='ignore')}\n"
#        result_message += f"{result.returncode}"
        
        tk.messagebox.showinfo("执行结果", result_message)
        
    except subprocess.TimeoutExpired:
        tk.messagebox.showerror("超时错误", "程序执行超时")
    except FileNotFoundError as e:
        tk.messagebox.showerror("文件错误", f"找不到文件: {e}")
    except Exception as e:
        tk.messagebox.showerror("执行错误", f"执行过程中发生错误: {e}")

b1_start =tk.Button(window, text='从这里开始',bg='yellow',
                    fg='red',font=('',80),command=start)
b1_start.place(x=500, y=400, anchor='center')
#设置开始按键
#b1_start.destroy()
#删除开始按键，布局新的窗口界面

window.mainloop()
