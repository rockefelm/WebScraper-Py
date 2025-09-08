import sys
import importlib.util

get_html_spec = importlib.util.spec_from_file_location("get_html", "./src/get_html.py")
get_html = importlib.util.module_from_spec(get_html_spec)
get_html_spec.loader.exec_module(get_html)


def main():
    
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    html = get_html.get_html(sys.argv[1])
    print(html)


if __name__ == "__main__":
    main()
