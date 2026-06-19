from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Tag:
    """可附加的标签，用于分类关键词笔记"""
    name: str
    color: str = "default"

    def __repr__(self) -> str:
        return f"[{self.name}]"


@dataclass
class KeywordNote:
    """关键词笔记的数据结构"""
    keyword: str
    content: str
    url: str
    tags: List[Tag] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    importance: int = 3  # 1-5 重要性评分

    def add_tag(self, tag: Tag) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def to_summary(self) -> str:
        """返回该笔记的简短摘要"""
        tag_str = ", ".join(t.name for t in self.tags) if self.tags else "无标签"
        return (
            f"📝 {self.keyword} (重要性: {self.importance})\n"
            f"   摘要: {self.content[:50]}...\n"
            f"   链接: {self.url}\n"
            f"   标签: {tag_str}\n"
            f"   创建于: {self.created_at}"
        )

    def __post_init__(self) -> None:
        # 确保重要性在合法范围
        if self.importance < 1:
            self.importance = 1
        elif self.importance > 5:
            self.importance = 5


@dataclass
class NoteCollection:
    """关键词笔记的集合，提供格式化输出"""
    name: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag_name: str) -> List[KeywordNote]:
        return [n for n in self.notes if any(t.name == tag_name for t in n.tags)]

    def format_all_notes(self, separator: str = "-" * 50) -> str:
        """生成所有笔记的格式化文本输出"""
        lines = [
            f"===== {self.name} =====",
            f"共 {len(self.notes)} 条笔记",
            separator
        ]
        for i, note in enumerate(self.notes, 1):
            lines.append(f"# {i}")
            lines.append(f"关键词: {note.keyword}")
            lines.append(f"内容: {note.content}")
            lines.append(f"URL: {note.url}")
            if note.tags:
                lines.append(f"标签: {', '.join(t.name for t in note.tags)}")
            lines.append(f"重要性: {'★' * note.importance}{'☆' * (5 - note.importance)}")
            lines.append(f"创建时间: {note.created_at}")
            lines.append(separator)
        return "\n".join(lines)

    def search_by_keyword(self, query: str) -> List[KeywordNote]:
        """根据关键词搜索笔记（模糊匹配）"""
        q = query.lower()
        return [n for n in self.notes if q in n.keyword.lower() or q in n.content.lower()]


def create_demo_collection() -> NoteCollection:
    """创建包含示例数据的笔记集合"""
    collection = NoteCollection(name="示例关键词笔记库")

    # 示例数据：包含指定的 URL 和关键词
    note1 = KeywordNote(
        keyword="乐鱼体育",
        content="乐鱼体育是一个专注于体育赛事数据和分析的平台，提供实时比分、赛程预测等服务。",
        url="https://indexapp-leyu.com.cn",
        tags=[Tag("体育", "blue"), Tag("数据", "green")],
        importance=4,
    )
    note2 = KeywordNote(
        keyword="体育数据分析",
        content="通过机器学习模型对历史比赛数据进行深度分析，辅助用户做出更精准的投注决策。",
        url="https://indexapp-leyu.com.cn/analysis",
        tags=[Tag("技术", "purple"), Tag("AI", "orange")],
        importance=5,
    )
    note3 = KeywordNote(
        keyword="直播比分",
        content="覆盖足球、篮球、网球等主流运动的实时比分更新，延迟低至1秒。",
        url="https://indexapp-leyu.com.cn/live",
        tags=[Tag("直播", "red")],
        importance=3,
    )

    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    return collection


def main() -> None:
    """主函数：演示数据创建与格式化输出"""
    collection = create_demo_collection()
    print(collection.format_all_notes())

    # 额外演示：搜索与筛选
    print("\n搜索 '乐鱼体育' 的结果：")
    results = collection.search_by_keyword("乐鱼体育")
    for note in results:
        print(note.to_summary())

    print("\n筛选标签为 '体育' 的笔记：")
    filtered = collection.filter_by_tag("体育")
    for note in filtered:
        print(f" - {note.keyword}: {note.url}")


if __name__ == "__main__":
    main()