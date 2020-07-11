import parser
import sys

if __name__ == '__main__':
    url = sys.argv[1]
    page_num = int(sys.argv[2])
    info = parser.get_thread_info(url, page_num)
    parser.print_info(info)
