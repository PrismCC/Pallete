import json
import os

from openai import OpenAI


def llm_call(color, hex_code, client):
    prompt1 = f"关于中国传统颜色{color} {hex_code}，用一段话介绍该颜色的起源、发展历程与相关轶事。文风典雅简洁，不多于200字，无换行符。"
    completion1 = client.chat.completions.create(
        model="deepseek-v3-1-250821",
        messages=[
            {
                "role": "user",
                "content": prompt1,
            },
        ],
    )
    prompt2 = f"关于中国传统颜色{color} {hex_code}，写下你联想到的或自行创作的一句诗词。不用写标题作者出处，在一行内输出。"
    completion2 = client.chat.completions.create(
        model="deepseek-v3-1-250821",
        messages=[
            {
                "role": "user",
                "content": prompt2,
            },
        ],
    )
    return (
        completion1.choices[0].message.content.strip(),
        completion2.choices[0].message.content.strip(),
    )


def add_tags():
    with open("../public/colors.json", encoding="utf-8") as file:
        colors = json.load(file)
    for color, info in colors.items():
        tags = input(f"tags for {color}: ").strip().split()
        info["tags"] = tags
    with open("../public/colors.json", "w", encoding="utf-8") as file:
        json.dump(colors, file, ensure_ascii=False, indent=4)


def main():
    color_file = "colors.txt"
    colors = {}
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3/",
        api_key=os.environ.get("ARK_API_KEY"),
    )
    with open(color_file, encoding="utf-8") as file:
        for line in file:
            name, hex_code = line.strip().split()
            r = int(hex_code[1:3], 16)
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
            introduction, poetry = llm_call(name, hex_code, client)
            colors[name] = {
                "name": name,
                "hex": hex_code,
                "r": r,
                "g": g,
                "b": b,
                "introduction": introduction,
                "poetry": poetry,
            }
            print(colors[name])
    with open("../public/colors.json", "w", encoding="utf-8") as file:
        json.dump(colors, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # main()
    add_tags()
