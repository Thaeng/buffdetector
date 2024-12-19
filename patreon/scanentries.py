import re

from patreon.class_post import Post
from utils.util import log


def read_relevant_lines_old():
    f = open("../patreon/resource/demofile.html", "r", encoding="utf8")
    html_s = f.read()
    html_s_removed_new_line = ''.join(html_s.splitlines())
    return re.findall("<span data-tag=\"post-title\".*?</a", html_s_removed_new_line)


def read_relevant_lines():
    f = open("../patreon/resource/demofile.html", "r", encoding="utf8")
    html_s = f.read()
    html_s_removed_new_line = ''.join(html_s.splitlines())
    return re.findall("<span data-tag=\"post-title\".*?data-tag=\"post-published-at\".*?</span>",
                      html_s_removed_new_line)


def create_posts_from_lines(lines) -> []:
    posts = []
    for line in lines:
        title_info_str = re.search("<span data-tag=\"post-title\".*?</a", line).group()
        title = re.search("[0-9]\">.*?<", title_info_str).group()[3:-1] \
            .replace(" ", "_") \
            .replace("/", "_") \
            .replace(".", "") \
            .replace(":", "") \
            .replace("!", "") \
            .replace("?", "") \
            .replace("~", "") \
            .replace("*", "") \
            .replace("\"", "") \
            .replace("\'", "")
        url = re.search("<a href=.*?>", title_info_str).group()[9:-2]

        published = re.search("post-published.*?</span>", line).group()
        published = re.search("<span>.*?</span>", published).group()
        published = published \
            .replace("<span>", "") \
            .replace("</span>", "") \
            .replace(",", "") \
            .replace(" ", "_")

        if any(is_url_equal(post, url) for post in posts):
            continue

        post = Post(title, url, published)
        posts.append(post)
        print(post)

    return posts


def is_url_equal(post: Post, url) -> bool:
    if post.url == url:
        log(f"Found Duplicate Post [{post}]")
        return True
    return False


def scan(skip:int=0):
    lines = read_relevant_lines()
    print(len(lines))
    filtered = []
    for i in range(0, len(lines)):
        if i <= (skip-1):
            continue
        filtered.append(lines[i])
    #[103/129]
    print(len(filtered))
    return create_posts_from_lines(filtered)


if __name__ == '__main__':
    scan()
