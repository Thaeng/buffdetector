from patreon import scanentries
from patreon import download
from utils.util import log

SKIP = 0

if __name__ == '__main__':
    posts = scanentries.scan(skip=SKIP)
    log(f"Found {len(posts)} Posts")
    download.run(posts)
    exit()
