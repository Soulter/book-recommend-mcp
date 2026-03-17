import argparse
import csv
import json
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


def get_book_video_link(title: str) -> tuple[bool, str]:
    books = load_books()
    target = title.strip()

    for book in books:
        if book.get("图书名称", "").strip() == target:
            intro_video = book.get("intro-video", "").strip()
            if intro_video:
                return True, intro_video
            break

    return False, ""


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
        return json.dumps(
            {
                "category": normalized_category,
                "has_video": False,
                "books": [],
                "message": (
                    f"未找到分类\u201c{normalized_category}\u201d的图书。可用分类：{', '.join(categories)}"
                ),
            },
            ensure_ascii=False,
        )

    selected_books = random.sample(matched_books, k=min(5, len(matched_books)))
    recommend_books = []
    for index, book in enumerate(selected_books, start=1):
        title = book.get("图书名称", "未知书名").strip()
        author = book.get("作者", "未知作者").strip()
        level = book.get("推荐学段", "未知学段").strip()
        summary = book.get("故事梗概", "无简介").strip()
        has_video, video = get_book_video_link(title)
        recommend_books.append(
            {
                "rank": index,
                "title": title,
                "author": author,
                "level": level,
                "summary": summary,
                "has_video": has_video,
                "video": video,
            }
        )

    return json.dumps(
        {
            "category": normalized_category,
            "has_video": any(item["has_video"] for item in recommend_books),
            "books": recommend_books,
        },
        ensure_ascii=False,
    )


@mcp.tool(name="get_book_recommend_video")
def get_book_recommend_video(title: str) -> str:
    """Return intro video link for a specific book title."""
    has_video, video = get_book_video_link(title)
    if not has_video:
        return json.dumps(
            {
                "title": title.strip(),
                "has_video": False,
                "video": "",
                "message": "未找到该书对应视频",
            },
            ensure_ascii=False,
        )

    return json.dumps(
        {"title": title.strip(), "has_video": True, "video": video},
        ensure_ascii=False,
    )


def main():
    parser = argparse.ArgumentParser(description="Book recommend MCP server")
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Use stdio transport instead of streamable-http",
    )
    args = parser.parse_args()

    transport = "stdio" if args.stdio else "streamable-http"
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
