import os
import sys

VERSION = '1.0, 2013-06-26'

breadth = 0
now_length = 0
now_depth = 0
max_length = 0
max_depth = 0

longest_file = ''
deepest_path = ''


def _get_depth(_, dirname, files):
    """
    Function called during `os.path.walk` directory traversal.

    `os.path.walk` is deprecated, but `os.walk` is not yet implemented in
    ShedSkin.

    @param dirname: The name of the directory currently being examined.
    @type  dirname: str
    @param files: The list of file names residing within the current directory.
    @type  files: list or iterable
    """
    global breadth
    global now_length, now_depth, max_length, max_depth
    global longest_file, deepest_path
    fullname = ''

    # "Breadth" is the total number of directories that have been examined.
    breadth += 1

    # "Length" is the longest path name encountered during the traversal.
    if files:
        for filename in files:
            fullname = dirname + os.path.sep + filename
            now_length = max(max_length, len(fullname))
            if max_length < now_length:
                max_length = now_length
                longest_file = fullname
    else: # No files in this directory; check the name of the directory itself
        now_length = max(max_length, len(dirname))
        if max_length < now_length:
            max_length = now_length
            longest_file = dirname

    # "Depth" is the largest subdirectory chain encountered during traversal.
    now_depth = len(dirname.split(os.sep))
    now_depth = max(max_depth, now_depth - 1)

    if max_length < now_length:
        max_length = now_length
        longest_file = dirname

    if max_depth < now_depth:
        max_depth = now_depth
        deepest_path = dirname

    print_update(breadth, max_length, max_depth)


def print_header():
    """
    Prints a table header to be displayed during directory traversal.
    """
    print 'breadth of dirs examined    longest pathname    deepest directory'
    print '                       0                   0                    0'


def print_update(breadth, length, depth):
    """
    Updates the results table with the new information.

    Will only work on consoles that support ANSI escape character sequences.
    Otherwise, will print a line-by-line series of updates. Workable, but ugly.

    @param breadth: The number of directories that have been examined.
    @type  breadth: int
    @param length: The current largest length of a path, in characters.
    @type  length: int
    @param depth: The current deepest level in a path, in subdirectories.
    @type  depth: int
    """
    sys.stdout.write('\x1b[#F') # move the cursor back to the previous line
    for _ in range(24 - len(str(breadth))):
        sys.stdout.write(' ')
    sys.stdout.write(str(breadth))
    for _ in range(20 - len(str(length))):
        sys.stdout.write(' ')
    sys.stdout.write(str(length))
    for _ in range(21 - len(str(depth))):
        sys.stdout.write(' ')
    sys.stdout.write(str(depth))
    print '' # newline


def print_footer():
    """
    Prints the footer for the results table, containing the longest path and
    deepest directory encountered.
    """
    global longest_file, deepest_path
    print ''
    print 'longest file: %s' % longest_file
    print 'deepest path: %s' % deepest_path


def main():
    """
    Program entry.
    """
    path = '.'

    if len(sys.argv) > 1:
        path = sys.argv[1]

    if path == "--help" or path == "--version":
        print """
deep
Version %s
Written by Mark R. Gollnick <mark.r.gollnick@gmail.com> &#10013;
Boost Software License, Version 1.0: boost.org/LICENSE_1_0.txt
Determines the maximum depth of the current (or a specified) directory tree.

usage:

    deep [dir]

output:

    breadth of dirs examined    longest pathname    deepest directory
                        1000                  55                    5

    longest file: C:\\some\\really\\long\\filename_that_should_be_renamed.txt
    deepest path: C:\\dwarves\\digging\\deep\\deeper\\deepest\\balrog.log
""" % VERSION

    else:
        print_header()
        os.path.walk(path, _get_depth, '')
        print_footer()


if __name__ == "__main__":
    main()
