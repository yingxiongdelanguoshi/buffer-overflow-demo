#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//溢出判断
void trick() {
    printf("请认真！\n");
}

//危险代码：计算机重启
void reboot(){
    int result;
    result = system("shutdown /r /t 0");
}

//危险代码：计算机关机
void colse(){
    int result;
    result = system("shutdown /s /t 0");
}

// 危险代码：下载学习通Windows版本
//可以构造更恶意的下载链接，比如上传更大的病毒文件下载到目标主机
void download_chaoxing() {
    printf("正在下载学习通Windows版本...\n");
    int result;
    // 使用PowerShell下载文件
    result = system("powershell -Command \"Invoke-WebRequest -Uri 'https://apps.chaoxing.com/' -OutFile 'chaoxing_installer.exe'");
    if (result == 0) {
        printf("下载完成！文件保存为 chaoxing_installer.exe\n");
    } else {
        printf("下载失败，请检查网络连接或URL是否正确。\n");
    }
}

//危险代码：删除学习通
//可以构造更恶意的删除命令，比如删除其他重要文件、操作系统源码等
void uninstall_chaoxing() {
    printf("正在尝试卸载学习通...\n");
    
    // 方法1: 使用wmic命令查找并卸载学习通
    int result1 = system("wmic product where \"name like '%学习通%'\" call uninstall /nointeractive");
    
    // 方法2: 尝试删除常见的学习通安装目录
    int result2 = system("rd /s /q \"%ProgramFiles%\\ChaoXing\" 2>nul");
    int result3 = system("rd /s /q \"%ProgramFiles(x86)%\\ChaoXing\" 2>nul");
    
    // 方法3: 删除开始菜单中的快捷方式
    int result4 = system("del /f /q \"%ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\*学习通*.lnk\" 2>nul");
    
    // 方法4: 结束学习通相关进程
    system("taskkill /f /im chaoxing.exe 2>nul");
    system("taskkill /f /im CXBrowser.exe 2>nul");
    
    printf("卸载命令已执行，请检查学习通是否已被移除。\n");
}

int main() {
    
    char buffer[16];
    
    gets(buffer);//不安全函数gets()
    
    return 0;
}