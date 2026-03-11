# book-recommend-mcp

一个基于 MCP 的图书推荐服务。

- Tool 名称：`book-recommend`
- 参数：`category`（图书分类）
- 行为：从 `booklist.csv` 中筛选对应分类，随机返回 5 本书（不足 5 本则返回全部）

## 目录结构

- `main.py`：MCP 服务入口
- `booklist.csv`：图书数据源

## 环境要求

- Python `>=3.12`

## 安装依赖

如果你使用虚拟环境（如 `.venv`）：

```bash
source .venv/bin/activate
pip install -e .
```

## 启动服务 - 普通 MCP Server

```bash
python main.py
```

## 启动服务 - 小智

```bash
export MCP_ENDPOINT=<your_mcp_endpoint>
python xiaozhi_mcp_pipe.py main.py
```

服务通过 `stdio` 传输，可被 MCP Host（如支持 MCP 的客户端）直接调用。

## Tool 说明

### `book-recommend`

按分类随机推荐图书。

**参数**

- `category` (`string`)：分类名称，例如：`文学`、`人文社科`、`自然科学`、`艺术`

**返回**

- 成功：返回该分类下随机 5 本图书，包含书名、作者、推荐学段
- 失败：当分类不存在时，返回提示并列出可用分类

## 调用示例

请求参数：

```json
{
	"category": "文学"
}
```

返回示例（随机）：

```text
分类“文学”推荐书单：
1. 芝麻开门 | 作者：祁智 著 | 学段：小学 5-6
2. 你是我的妹 | 作者：彭学军 著 | 学段：小学 5-6
3. 三毛流浪记 | 作者：张乐平 著 | 学段：小学 3-4
4. 成语故事 | 作者：—— | 学段：小学 3-4
5. 大林和小林 | 作者：张天翼 著 | 学段：小学 5-6
```
