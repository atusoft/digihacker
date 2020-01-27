import os
import sys

source = sys.argv[1]
dest = sys.argv[2]

src_fd = os.open(source, os.O_RDONLY)
dest_fd = os.open(dest, os.O_RDWR | os.O_CREAT)

offset = 0
statinfo = os.stat(source)
count = statinfo.st_size
print(count)
bytesSent = 0
while offset < count:
    bytesSent = os.sendfile(dest_fd, src_fd, offset, count)
    print("% d bytes sent / copied successfully." % bytesSent)
    offset += bytesSent

os.close(src_fd)
os.close(dest_fd)
