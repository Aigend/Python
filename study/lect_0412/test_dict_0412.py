#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/12 9:35
favite_languages = {
    "jen":"python",
    "sarahc":"java",
    "skafj":"C++",
    "phil":"ruby",
    "jsk":["afkaj","ffn","akjf","lvl"]
}
print(favite_languages.items())
#dict_items([('jen', 'python'), ('sarahc', 'java'), ('skafj', 'C++'), ('phil', 'ruby'), ('jsk', ['afkaj', 5, 'akjf', 3.15])])
for name,languages in favite_languages.items():
    print("\n"+name.title()+"'s favorite languages are:")
    for language in languages:
        print("\t"+language.title())


for name in favite_languages:
    print(name.title())
for name in sorted(favite_languages):
    print(name.upper())
for name in sorted(favite_languages):
    print(name.lower())

favite_languages = "    python   java   "
print(favite_languages)
print(favite_languages.strip())
print(favite_languages.lstrip())
print(favite_languages.rstrip())

for alien_name in range(1,30):
    print(alien_name)

if __name__ == '__main__':
    pass