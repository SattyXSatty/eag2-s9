# Cortex-R Documentation Index

## 📚 Complete Documentation Set

### 1. **ARCHITECTURE_REPORT.md** (Main Report)
**Location:** Root directory  
**Size:** ~3,500 lines  
**Content:**
- Executive Summary
- System Architecture Overview
- Core Components (Function-Level)
  - Entry Point (agent.py)
  - AgentLoop (core/loop.py)
  - Perception Module
  - Decision Module
  - Strategy Module
  - Action Module
  - Context Management
  - Memory Management
  - Session Management
  - Model Management
  - Tool Utilities
- MCP Server Implementations
  - Math Server (mcp_server_1.py)
  - Document Server (mcp_server_2.py)
  - Web Search Server (mcp_server_3.py)
- Data Models and Configuration
- Prompt Engineering
- Execution Flow Analysis
- Design Patterns and Principles
- SOLID Principles
- Error Handling Strategy
- Performance Optimizations
- Security Considerations
- Testing and Debugging
- Deployment and Operations
- Extension Points
- Best Practices
- **Flow Diagrams (Part 1):**
  - Diagram 32: Complete End-to-End Flow
  - Diagram 33: Perception Module Flow
  - Diagram 34: Decision Module Flow
  - Diagram 35: Action Module Flow
  - Diagram 36: Memory Management Flow
  - Diagram 37: MCP Server Tool Execution

---

### 2. **FLOW_DIAGRAMS_PART2.md** (Extended Diagrams)
**Location:** Root directory  
**Size:** ~1,500 lines  
**Content:**
- **Diagram 38:** Document Processing & FAISS Indexing
- **Diagram 39:** Strategy Selection Flow
- **Diagram 40:** Web Search Flow (DuckDuckGo)
- **Diagram 41:** Configuration Loading
- **Diagram 42:** Error Handling & Retry Logic
- **Diagram 43:** Session Lifecycle
- **Diagram 44:** Complete Data Flow

---

### 3. **VISUAL_FLOWCHARTS.md** (Comprehensive Visual Guide)
**Location:** Root directory  
**Size:** ~2,000 lines  
**Content:**
- **Section 1:** High-Level System Overview
- **Section 2:** Complete End-to-End Flow (Sequence Diagram)
- **Section 3:** Perception Module Flow
- **Section 4:** Decision Module Flow
- **Section 5:** Action Module (Sandbox) Flow
- **Section 6:** Memory Management Flow
- **Section 7:** MCP Server Tool Execution
- **Section 8:** Document Processing Pipeline
- **Section 9:** Strategy Selection Flow
- **Section 10:** Web Search Flow
- **Section 11:** Configuration Loading
- **Section 12:** Error Handling & Retry
- **Section 13:** Session Lifecycle (State Diagram)
- **Section 14:** Data Flow Overview

---

## 🎯 Quick Navigation

### By Topic

#### Architecture & Design
- **System Overview:** ARCHITECTURE_REPORT.md (Lines 1-100)
- **Design Patterns:** ARCHITECTURE_REPORT.md (Section 20)
- **SOLID Principles:** ARCHITECTURE_REPORT.md (Section 21)

#### Core Components
- **AgentLoop:** ARCHITECTURE_REPORT.md (Section 2)
- **Perception:** ARCHITECTURE_REPORT.md (Section 3) + VISUAL_FLOWCHARTS.md (Section 3)
- **Decision:** ARCHITECTURE_REPORT.md (Section 4) + VISUAL_FLOWCHARTS.md (Section 4)
- **Action/Sandbox:** ARCHITECTURE_REPORT.md (Section 6) + VISUAL_FLOWCHARTS.md (Section 5)
- **Memory:** ARCHITECTURE_REPORT.md (Section 8) + VISUAL_FLOWCHARTS.md (Section 6)

#### MCP Servers
- **Math Server:** ARCHITECTURE_REPORT.md (Section 12)
- **Document Server:** ARCHITECTURE_REPORT.md (Section 13)
- **Web Search Server:** ARCHITECTURE_REPORT.md (Section 14)
- **Tool Execution:** VISUAL_FLOWCHARTS.md (Section 7)

#### Advanced Features
- **Document Processing:** FLOW_DIAGRAMS_PART2.md (Diagram 38)
- **Strategy Selection:** FLOW_DIAGRAMS_PART2.md (Diagram 39)
- **Error Handling:** FLOW_DIAGRAMS_PART2.md (Diagram 42) + VISUAL_FLOWCHARTS.md (Section 12)
- **Session Management:** FLOW_DIAGRAMS_PART2.md (Diagram 43) + VISUAL_FLOWCHARTS.md (Section 13)

#### Configuration
- **Config Files:** ARCHITECTURE_REPORT.md (Section 16)
- **Loading Flow:** FLOW_DIAGRAMS_PART2.md (Diagram 41) + VISUAL_FLOWCHARTS.md (Section 11)

#### Prompts
- **Prompt Engineering:** ARCHITECTURE_REPORT.md (Section 17)
- **Perception Prompt:** ARCHITECTURE_REPORT.md (Section 17A)
- **Decision Prompts:** ARCHITECTURE_REPORT.md (Section 17B-C)

---

## 📊 Diagram Types

### Flowcharts (Mermaid)
- **Total:** 14 diagrams
- **Format:** Mermaid flowchart TD/LR
- **Best for:** Understanding function-level execution flow

### Sequence Diagrams
- **Location:** VISUAL_FLOWCHARTS.md (Section 2)
- **Format:** Mermaid sequenceDiagram
- **Best for:** Understanding component interactions over time

### State Diagrams
- **Location:** VISUAL_FLOWCHARTS.md (Section 13)
- **Format:** Mermaid stateDiagram-v2
- **Best for:** Understanding session lifecycle and state transitions

### Architecture Diagrams
- **Location:** VISUAL_FLOWCHARTS.md (Section 1, 14)
- **Format:** Mermaid graph TB/LR
- **Best for:** Understanding system structure and data flow

---

## 🔍 Finding Specific Information

### "How does X work?"

| Question | Document | Section |
|----------|----------|---------|
| How does the agent process a query? | VISUAL_FLOWCHARTS.md | Section 2 |
| How does perception select servers? | VISUAL_FLOWCHARTS.md | Section 3 |
| How does code generation work? | VISUAL_FLOWCHARTS.md | Section 4 |
| How does sandbox execution work? | VISUAL_FLOWCHARTS.md | Section 5 |
| How does memory persistence work? | VISUAL_FLOWCHARTS.md | Section 6 |
| How do tool calls work? | VISUAL_FLOWCHARTS.md | Section 7 |
| How does document indexing work? | VISUAL_FLOWCHARTS.md | Section 8 |
| How does strategy selection work? | VISUAL_FLOWCHARTS.md | Section 9 |
| How does web search work? | VISUAL_FLOWCHARTS.md | Section 10 |
| How does configuration loading work? | VISUAL_FLOWCHARTS.md | Section 11 |
| How does error handling work? | VISUAL_FLOWCHARTS.md | Section 12 |
| How does session management work? | VISUAL_FLOWCHARTS.md | Section 13 |

### "What does function X do?"

| Function | Document | Section |
|----------|----------|---------|
| `agent.py::main()` | ARCHITECTURE_REPORT.md | Section 1 |
| `AgentLoop.run()` | ARCHITECTURE_REPORT.md | Section 2 |
| `extract_perception()` | ARCHITECTURE_REPORT.md | Section 3 |
| `generate_plan()` | ARCHITECTURE_REPORT.md | Section 4 |
| `run_python_sandbox()` | ARCHITECTURE_REPORT.md | Section 6 |
| `MemoryManager.save()` | ARCHITECTURE_REPORT.md | Section 8 |
| `MultiMCP.call_tool()` | ARCHITECTURE_REPORT.md | Section 9 |
| `ModelManager.generate_text()` | ARCHITECTURE_REPORT.md | Section 10 |
| `process_documents()` | ARCHITECTURE_REPORT.md | Section 13 |
| `semantic_merge()` | ARCHITECTURE_REPORT.md | Section 13 |

### "What are the design patterns?"

| Pattern | Document | Section |
|---------|----------|---------|
| Perception-Decision-Action Loop | ARCHITECTURE_REPORT.md | Section 20A |
| Strategy Pattern | ARCHITECTURE_REPORT.md | Section 20B |
| Sandbox Pattern | ARCHITECTURE_REPORT.md | Section 20C |
| Repository Pattern | ARCHITECTURE_REPORT.md | Section 20D |
| Facade Pattern | ARCHITECTURE_REPORT.md | Section 20E |
| Adapter Pattern | ARCHITECTURE_REPORT.md | Section 20F |
| Pipeline Pattern | ARCHITECTURE_REPORT.md | Section 20G |

---

## 📈 Statistics

### Documentation Coverage
- **Total Lines:** ~7,000 lines
- **Total Diagrams:** 14 comprehensive flowcharts
- **Functions Documented:** 100+
- **Classes Documented:** 15+
- **Design Patterns:** 8+
- **Code Examples:** 50+

### File Breakdown
```
ARCHITECTURE_REPORT.md:     3,500 lines (50%)
VISUAL_FLOWCHARTS.md:       2,000 lines (29%)
FLOW_DIAGRAMS_PART2.md:     1,500 lines (21%)
```

### Diagram Distribution
```
ARCHITECTURE_REPORT.md:     6 diagrams (Diagrams 32-37)
FLOW_DIAGRAMS_PART2.md:     7 diagrams (Diagrams 38-44)
VISUAL_FLOWCHARTS.md:       14 diagrams (Sections 1-14)
```

---

## 🚀 Getting Started

### For New Developers
1. Start with **VISUAL_FLOWCHARTS.md Section 1** (System Overview)
2. Read **VISUAL_FLOWCHARTS.md Section 2** (End-to-End Flow)
3. Review **ARCHITECTURE_REPORT.md Sections 1-11** (Core Components)

### For Understanding Specific Features
1. Find your topic in the Quick Navigation table above
2. Go to the recommended document and section
3. Review the corresponding flowchart in VISUAL_FLOWCHARTS.md

### For Debugging
1. Check **VISUAL_FLOWCHARTS.md Section 12** (Error Handling)
2. Review **ARCHITECTURE_REPORT.md Section 22** (Error Handling Strategy)
3. Check **ARCHITECTURE_REPORT.md Section 25** (Testing & Debugging)

### For Extending the System
1. Read **ARCHITECTURE_REPORT.md Section 28** (Extensibility)
2. Review **ARCHITECTURE_REPORT.md Section 30** (Best Practices)
3. Check relevant component documentation for integration points

---

## 💡 Tips

- **All diagrams are in Mermaid format** - Can be rendered in GitHub, VS Code, or any Mermaid viewer
- **Use Ctrl+F to search** - All documents are searchable
- **Cross-references** - Documents reference each other for related topics
- **Code examples** - Most sections include actual code snippets
- **Visual learners** - Start with VISUAL_FLOWCHARTS.md
- **Detail-oriented** - Start with ARCHITECTURE_REPORT.md

---

**Last Updated:** January 2025  
**Version:** 1.0  
**Maintained by:** Architecture Documentation Team

