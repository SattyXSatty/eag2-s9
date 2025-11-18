# Available Tools Reference Card

## Quick Reference: What Tools Actually Exist

### 🔢 Math Server (mcp_server_1.py)

| Tool Name | Purpose | Example |
|-----------|---------|---------|
| `add` | Add two numbers | `add({"input": {"a": 5, "b": 3}})` |
| `subtract` | Subtract numbers | `subtract({"input": {"a": 10, "b": 3}})` |
| `multiply` | Multiply numbers | `multiply({"input": {"a": 6, "b": 7}})` |
| `divide` | Divide numbers | `divide({"input": {"a": 20, "b": 4}})` |
| `power` | Exponentiation | `power({"input": {"a": 2, "b": 10}})` |
| `cbrt` | Cube root | `cbrt({"input": {"a": 27}})` |
| `factorial` | Factorial | `factorial({"input": {"a": 5}})` |
| `remainder` | Modulo | `remainder({"input": {"a": 17, "b": 4}})` |
| `sin` | Sine (radians) | `sin({"input": {"a": 1}})` |
| `cos` | Cosine (radians) | `cos({"input": {"a": 1}})` |
| `tan` | Tangent (radians) | `tan({"input": {"a": 1}})` |
| `mine` | Special operation | `mine({"input": {"a": 5, "b": 2}})` |
| `strings_to_chars_to_int` | String to ASCII | `strings_to_chars_to_int({"input": {"string": "INDIA"}})` |
| `int_list_to_exponential_sum` | Sum of exponentials | `int_list_to_exponential_sum({"input": {"numbers": [1,2,3]}})` |
| `fibonacci_numbers` | Fibonacci sequence | `fibonacci_numbers({"input": {"n": 10}})` |
| `create_thumbnail` | Image thumbnail | `create_thumbnail({"input": {"image_path": "img.jpg"}})` |

---

### 📄 Document Server (mcp_server_2.py)

| Tool Name | Purpose | Example |
|-----------|---------|---------|
| `search_stored_documents` | Search indexed docs | `search_stored_documents({"input": {"query": "AI"}})` |
| `convert_webpage_url_into_markdown` | Fetch & convert webpage | `convert_webpage_url_into_markdown({"input": {"url": "https://example.com"}})` |
| `extract_pdf` | Extract PDF content | `extract_pdf({"input": {"file_path": "doc.pdf"}})` |

---

### 🌐 Web Search Server (mcp_server_3.py)

| Tool Name | Purpose | Example |
|-----------|---------|---------|
| `duckduckgo_search_results` | Web search | `duckduckgo_search_results({"input": {"query": "AI", "max_results": 5}})` |
| `download_raw_html_from_url` | Fetch raw HTML | `download_raw_html_from_url({"input": {"url": "https://example.com"}})` |

---

## ❌ Common Hallucinations (DO NOT USE)

| Hallucinated Tool | Why It Fails | Use This Instead |
|-------------------|--------------|------------------|
| `extract_webpage` | Does not exist | `convert_webpage_url_into_markdown` |
| `search_api` | Does not exist | `duckduckgo_search_results` |
| `fetch_and_summarize_webpage` | Does not exist | `convert_webpage_url_into_markdown` |
| `search_knowledge_graph` | Does not exist | Use search + synthesis |
| `get_webpage` | Does not exist | `convert_webpage_url_into_markdown` |
| `web_search` | Does not exist | `duckduckgo_search_results` |
| `search_web` | Does not exist | `duckduckgo_search_results` |
| `fetch_url` | Does not exist | `download_raw_html_from_url` |

---

## 📋 Usage Patterns

### Pattern 1: Web Search

```python
# ✅ CORRECT
input = {"input": {"query": "Gensol Go-Auto", "max_results": 5}}
result = await mcp.call_tool('duckduckgo_search_results', input)

# ❌ WRONG
result = await mcp.call_tool('search_api', input)  # Does not exist!
```

### Pattern 2: Webpage Extraction

```python
# ✅ CORRECT
input = {"input": {"url": "https://example.com"}}
result = await mcp.call_tool('convert_webpage_url_into_markdown', input)

# ❌ WRONG
result = await mcp.call_tool('extract_webpage', input)  # Does not exist!
```

### Pattern 3: Document Search

```python
# ✅ CORRECT
input = {"input": {"query": "DLF apartments"}}
result = await mcp.call_tool('search_stored_documents', input)

# ❌ WRONG
result = await mcp.call_tool('search_knowledge_graph', input)  # Does not exist!
```

### Pattern 4: Math Operations

```python
# ✅ CORRECT
input = {"input": {"a": 5, "b": 3}}
result = await mcp.call_tool('add', input)

# ❌ WRONG
result = await mcp.call_tool('calculate', input)  # Does not exist!
```

---

## 🎯 Decision Tree: Which Tool to Use?

```
Need to search the web?
  → Use: duckduckgo_search_results

Need to fetch webpage content?
  → Use: convert_webpage_url_into_markdown

Need to search local documents?
  → Use: search_stored_documents

Need to extract PDF?
  → Use: extract_pdf

Need to do math?
  → Use: add, subtract, multiply, divide, etc.

Need to process strings?
  → Use: strings_to_chars_to_int

Need something else?
  → Check the Tool Catalog in the prompt!
```

---

## 🔍 How to Verify a Tool Exists

### Method 1: Check the Tool Catalog

The prompt always includes a "Tool Catalog" section. Only use tools listed there.

### Method 2: Look for Usage Examples

Every tool has a usage example in its docstring:
```
Usage: input={"input": {"query": "..."}} result = await mcp.call_tool('tool_name', input)
```

### Method 3: Runtime Error

If you use a wrong tool, you'll get:
```
ValueError: Tool 'wrong_tool' not found on any server.
Available tools include: add, subtract, multiply, ...
```

---

## 💡 Pro Tips

1. **Always copy the tool name exactly** from the Tool Catalog
2. **Check the Usage docstring** for correct input format
3. **Don't invent tool names** based on what "should" exist
4. **If unsure, re-read the Tool Catalog** in the prompt
5. **Use FURTHER_PROCESSING_REQUIRED** if you need to synthesize results

---

## 📊 Tool Statistics

| Server | Number of Tools | Most Used |
|--------|----------------|-----------|
| Math | 16 tools | `add`, `multiply`, `strings_to_chars_to_int` |
| Documents | 3 tools | `search_stored_documents`, `convert_webpage_url_into_markdown` |
| Web Search | 2 tools | `duckduckgo_search_results` |
| **Total** | **21 tools** | - |

---

## 🚨 Emergency Checklist

Before calling a tool, verify:

- [ ] Tool name appears in Tool Catalog
- [ ] Tool name is spelled exactly as shown
- [ ] Input format matches Usage docstring
- [ ] Tool is called with string name: `'tool_name'`
- [ ] Not using a hallucinated tool from the forbidden list

---

**Last Updated:** January 2025  
**Status:** Current ✅

