def to_xpath(compoundClass):
    '''Packs compound class name into xpath usable by Selenium'''
    return f"//*[@class='{compoundClass}']"