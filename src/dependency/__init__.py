from os import getenv
import sys

if getenv('LOCAL_ENV'):
    try:
        input_file = open('input.txt', 'r')
        output_file = open('output.txt', 'w')

        sys.stdin = input_file
        sys.stdout = output_file
    except Exception as e:
        print(f"Error opening files: {e}")


def print_arr(arr: list, seperator=' '):
    for i in arr:
        print(i, end=seperator)
    print()


def ni():
    return int(input())


def na():
    return list(map(int, input().split()))


def ns():
    return input()


def main():
    try:
        t = ni()
        for _ in range(t):
            # Write code here
            n = ni()


    except Exception as e:
        print("ERROR: ", e)


if __name__ == '__main__':
    main()
