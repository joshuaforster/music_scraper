def parse_price(price_text):
    import re

    nums = re.findall(r"\d+", price_text)
    nums = [int(n) for n in nums]

    if len(nums) == 0:
        return 0, 0
    elif len(nums) == 1:
        return nums[0], nums[0]
    else:
        return nums[0], nums[1]
