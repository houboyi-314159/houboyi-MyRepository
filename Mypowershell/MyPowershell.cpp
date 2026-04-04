#include <iostream>
#include <string>
#include <regex>
#include <filesystem>

namespace fs = std::filesystem;

void print_help()
{
    std::cout << "可用命令：\n"
        << "  cd \"path\"      切换目录\n"
        << "  ls              列出文件\n"
        << "  rm [-r] \"name\" 删除文件或目录\n"
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

int main()
{
    std::string path = "C:\\";
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
        else if (std::regex_match(code, match, cd_pattern))
            path = match[1].str();
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
                std::cout << "删除失败\n";
            }
        }
    }
}