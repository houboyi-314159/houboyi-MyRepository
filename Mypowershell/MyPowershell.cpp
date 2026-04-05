#include <iostream>
#include <string>
#include <regex>
#include <filesystem>
#include <windows.h>

namespace fs = std::filesystem;

void print_help()
{
    std::cout << "可用命令：\n"
        << "  cd \"path\"      切换目录\n"
        << "  cd ..           返回上级目录\n"
        << "  ls              列出文件\n"
        << "  rm [-r] \"name\" 删除文件或目录\n"
        << "  cls             清屏\n"
        << "  help            显示帮助\n"
        << "  exit            退出\n";
}

void print_help_rm()
{
    std::cout << "rm [-r] \"target\"\n"
        << "  -r  递归删除目录\n";
}

void print_help_ls()
{
    std::cout << "ls\n"
        << "  列出当前目录内容\n";
}

void set_color(int color)
{
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, color);
}

int main()
{
    std::string path = fs::absolute("C:\\").string();
    std::string input_path;
    std::string code;
    std::smatch match;

    std::regex cd_pattern("^cd\\s+\"([^\"]+)\"$");
    std::regex ls_pattern("^ls$");
    std::regex rm_pattern("^rm\\s+(-r\\s+)?\"([^\"]+)\"$");

    std::cout << "Welcome to MyPowershell!\n";

    while (true)
    {
        std::cout << "MYPS " << path << "> ";
        std::getline(std::cin, code);

        if (code == "exit")
            break;

        if (code == "help")
            print_help();
        else if (code == "rm -?")
            print_help_rm();
        else if (code == "ls -?")
            print_help_ls();

        else if (code == "cls")
        {
            system("cls");
        }

        else if (code == "cd ..")
        {
            path = fs::absolute(fs::path(path).parent_path()).string();
        }

        else if (std::regex_match(code, match, cd_pattern))
        {
            // ✅ 路径标准化（解决 .\Windows 问题）
            input_path = fs::absolute(
                fs::path(path) / match[1].str()
            ).string();

            if (!fs::exists(input_path))
            {
                set_color(12);
                std::cout << "路径不存在\n";
                set_color(7);
            }
            else
            {
                path = input_path;
            }
        }

        else if (std::regex_match(code, ls_pattern))
        {
            try {
                for (auto& e : fs::directory_iterator(path))
                    std::cout << e.path().filename().string() << "\n";
            }
            catch (...) {}
        }

        else if (std::regex_match(code, match, rm_pattern))
        {
            try {
                if (match[1].matched)
                    fs::remove_all(path + "\\" + match[2].str());
                else
                    fs::remove(path + "\\" + match[2].str());
            }
            catch (...) {
                set_color(12);
                std::cout << "删除失败\n";
                set_color(7);
            }
        }

        else
        {
            set_color(12);
            std::cout << "错误命令\n";
            set_color(7);
        }
    }
}