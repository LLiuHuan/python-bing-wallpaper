from datetime import datetime, timedelta
from glob import glob


def writeToReadme():
    readme_path = 'README.md'

    # 把最近30天的图片链接写入README.md
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('# Bing Wallpaper\n\n')

        f.write('```\n')
        f.write('Python 每日爬取Bing壁纸，保存到本地，同时将最近30天的图片链接写入README.md\n')
        f.write('从2009年开始至今的图片大部分都有，有几个实在是找不到了\n')
        f.write('```\n\n')

        image_path = datetime.now().strftime("%Y/%m/%d")
        paths = glob(f'./images/{image_path}/*.jpg')
        if paths:
            f.write('\n\n## 今日图片\n')
            f.write('\n\n![]({}){} [download]({})'.format(paths[0], image_path, paths[0]))

        f.write('\n\n## 最近30天的图片链接\n')
        f.write('\n\n|      |      |      |\n')
        f.write('| :----: | :----: | :----: |\n')
        index = 1
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            image_path = date.strftime("%Y/%m/%d")
            paths = glob(f'./images/{image_path}/*.jpg')
            if paths:
                file = "![]({}){} [download]({})".format(paths[0], image_path, paths[0])
                f.write('|' + file)
                if index % 3 == 0:
                    f.write('|\n')
                index += 1

        if index % 3 != 1:
            f.write('|')

        f.write('\n\n')


if __name__ == '__main__':
    writeToReadme()
