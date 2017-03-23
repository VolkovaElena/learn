#!/usr/bin/env python3.5

s0 = ["null", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
s1 = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
s2 = [None, None, "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
s3 = [None, "one hundred", "two hundred", "three hundred", "four hundred", "five hundred", "six hundred",
      "seven hundred", "eight hundred", "nine hundred"]


def transform_triplet(num, is_last=True):
    num_len = len(num)
    result = []
    for c in num:
        if num_len == 3:
            if s3[int(c)]:
                result.append(s3[int(c)])
        if num_len == 2:
            if int(c) == 1:
                result.append(s1[int(num[-1])])
                break
            if s2[int(c)]:
                result.append(s2[int(c)])
        if num_len == 1:
            if int(c) == 0:
                if not result and is_last:
                    result.append(s0[int(c)])
            else:
                result.append(s0[int(c)])
        num_len -= 1
    return result


def translation(number):
    result = []
    num = str(int(number))
    if num[-9:-6]:
        items = transform_triplet(num[-9:-6], False)
        if items:
            items.append("million(s)")
            result += items
    if num[-6:-3]:
        items = transform_triplet(num[-6:-3], False)
        if items:
            items.append("thousand(s)")
            result += items
    if num[-3:]:
        items = transform_triplet(num[-3:], is_last=(not result))
        result += items
    return " ".join(result)


if __name__ == "__main__":
    print(translation(10030000))
