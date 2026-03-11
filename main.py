import csv
import random
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("book-recommend", port=6267)

BOOKLIST_PATH = Path(__file__).parent / "booklist.csv"


def load_books() -> list[dict[str, str]]:
    with BOOKLIST_PATH.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


@mcp.tool(name="book-recommend")
def book_recommend(category: str) -> str:
    """Recommend 5 random books by category.

    Args:
        category: Book category, e.g. 文学 / 人文社科 / 自然科学 / 艺术
    """
    normalized_category = category.strip()
    books = load_books()
    matched_books = [
        book for book in books if book.get("分类", "").strip() == normalized_category
    ]

    if not matched_books:
        categories = sorted(
            {book.get("分类", "").strip() for book in books if book.get("分类")}
        )
        return (
            f"未找到分类“{normalized_category}”的图书。"
            f"可用分类：{', '.join(categories)}"
        )

    selected_books = random.sample(matched_books, k=min(5, len(matched_books)))
    lines = [f"分类“{normalized_category}”推荐书单："]
    for index, book in enumerate(selected_books, start=1):
        title = book.get("图书名称", "未知书名").strip()
        author = book.get("作者", "未知作者").strip()
        level = book.get("推荐学段", "未知学段").strip()
        summary = book.get("故事梗概", "无简介").strip()
        lines.append(f"{index}. {title} | 作者：{author} | 学段：{level} | 简介：{summary}")
    return "\n".join(lines)


def main():
    # Initialize and run the server
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
