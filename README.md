# MinerU Parser

**MinerU Parser** 是一个 Python 包，用于调用 [MinerU API](https://mineru.net) 对本地文档（PDF、Word、Excel、PPT、HTML 等）进行解析，支持批量处理和轮询状态。

---

## 安装

```bash
# 克隆仓库
git clone https://your-repo-url/mineru-parser.git
cd mineru-parser

# 创建虚拟环境（可选）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 安装包
pip install -e .
```

## 设置环境变量

在使用 MinerU Parser 之前，需要设置 MinerU 的 API Token。你可以通过两种方式进行设置：

### 1. 通过 Python 运行时输入（推荐）

```python
from mineru_parser.auth import ensure_env

# 如果环境变量不存在，会提示用户输入
ensure_env("MINERU_TOKEN")

# 或者可以直接设置环境变量（仅本次 Python 会话有效）
import os
os.environ["MINERU_TOKEN"] = "your_token_here"
```

## 使用示例

### 1. 解析单个文件

```python
from mineru_parser import parse_local_documents

parse_local_documents(
    inputs=r"C:\Users\22959\Desktop\数据清洗数据\未来乡村\CityDO数字乡村操作系统方案（初稿-0227）.doc",
    output_dir=r"C:\Users\22959\Desktop\mineru_results"
)
```

inputs 可以是单个文件路径，也可以是文件路径列表，或者是文件夹路径列表。

output_dir 是解析结果输出的文件夹，会自动创建。

支持的文件类型：.pdf, .doc, .docx, .ppt, .pptx, .png, .jpg, .jpeg, .html。

---
