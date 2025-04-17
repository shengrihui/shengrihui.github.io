import os
import yaml

all_tags = set()
all_categories = set()


def fix_front_matter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(file_path)
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = yaml.safe_load(parts[1])
            # print(front_matter)
            categories = front_matter.get('categories')
            tags = front_matter.get('tags')
            print("原先", categories, tags)
            if isinstance(categories, str):
                categories = [categories]
            if isinstance(tags, str):
                tags = [tags]

            # 换名字
            for old, new in [("蓝桥", "蓝桥杯"), ('二分法', '二分'),
                             ('广度优先搜索（BFS）', 'BFS'), ('深度优先搜索（DFS）', 'DFS'), ('动态规划DP', '动态规划')]:
                if old in categories:
                    categories.remove(old)
                    categories.append(new)
                if old in tags:
                    tags.remove(old)
                    tags.append(new)

            # 整理分类
            for old, new in [('Leetcode', '算法'), ('蓝桥杯', '算法'), ('二分', '算法'),
                             ('Python', 'Python'), ('大数据', '学校课程'),
                             ('操作系统', '学校课程'), ('数据库', '学校课程'), ]:
                if old in categories:
                    tags = list(set(tags) | set(categories))
                    categories = [new]
                    tags = list(set(tags) | set(categories))

            print("改后", categories, tags)

            all_tags.update(tags)
            all_categories.update(categories)

            front_matter['categories'] = categories
            front_matter['tags'] = tags

            # 修改并写入
            new_front = yaml.dump(front_matter, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{new_front}---{parts[2]}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 修复: {file_path}")
        else:
            print(f"🟢 无需更改: {file_path}")


def walk_md_files(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                fix_front_matter(os.path.join(root, file))


# 修改这里为你的博客路径
blog_path = '_posts'
walk_md_files(blog_path)
print(all_tags)
print(all_categories)
