# Bug Fix Visualization

## The Bug: Infinite Loop

```mermaid
sequenceDiagram
    participant User
    participant Loop as AgentLoop
    participant Decision as generate_plan
    participant Sandbox
    
    User->>Loop: "What is relationship between Gensol and Go-Auto?"
    
    Note over Loop: Step 1
    Loop->>Decision: user_input = "What is relationship..."
    Decision->>Decision: Generate search plan
    Decision-->>Loop: solve() with search call
    Loop->>Sandbox: Execute search
    Sandbox-->>Loop: Search results (5 articles)
    Loop->>Loop: Set user_input_override with results
    
    Note over Loop: Step 2 (BUG HERE!)
    Loop->>Decision: user_input = "What is relationship..." ❌
    Note over Decision: LLM never sees the search results!<br/>It only sees the original query
    Decision->>Decision: Generate search plan AGAIN
    Decision-->>Loop: solve() with search call AGAIN
    Loop->>Sandbox: Execute search AGAIN
    Sandbox-->>Loop: Same search results
    Loop->>Loop: Set user_input_override AGAIN
    
    Note over Loop: Step 3
    Loop->>Decision: user_input = "What is relationship..." ❌
    Decision->>Decision: Generate search plan AGAIN
    Decision-->>Loop: solve() with search call AGAIN
    Loop->>Loop: Max steps reached
    Loop-->>User: "Max steps reached" 😞
```

## The Fix: Proper Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Loop as AgentLoop
    participant Decision as generate_plan
    participant Sandbox
    
    User->>Loop: "What is relationship between Gensol and Go-Auto?"
    
    Note over Loop: Step 1
    Loop->>Decision: user_input = "What is relationship..."
    Decision->>Decision: Generate search plan
    Decision-->>Loop: solve() with search call
    Loop->>Sandbox: Execute search
    Sandbox-->>Loop: Search results (5 articles)
    Loop->>Loop: Set user_input_override with results
    
    Note over Loop: Step 2 (FIXED!)
    Loop->>Decision: user_input = user_input_override ✅
    Note over Decision: LLM sees:<br/>"Your last tool produced this result:<br/>[5 search results about Gensol-Go-Auto fraud]"
    Decision->>Decision: Synthesize answer from results
    Decision-->>Loop: solve() with FINAL_ANSWER (no tool calls)
    Loop->>Sandbox: Execute synthesis
    Sandbox-->>Loop: FINAL_ANSWER: "Go-Auto was an auto dealership..."
    Loop-->>User: Comprehensive answer 🎉
```

## Code Comparison

### Before (Bug):

```python
# core/loop.py - Line 56
plan = await generate_plan(
    user_input=self.context.user_input,  # ❌ Always original query
    perception=perception,
    memory_items=self.context.memory.get_session_items(),
    tool_descriptions=tool_descriptions,
    prompt_path=prompt_path,
    step_num=step + 1,
    max_steps=max_steps,
)
```

**Problem:** Even though `user_input_override` was set with search results, the `generate_plan()` function never received it. The LLM kept seeing the original query and generating the same search plan repeatedly.

### After (Fixed):

```python
# core/loop.py - Line 56
plan = await generate_plan(
    user_input=user_input_override or self.context.user_input,  # ✅ Uses override
    perception=perception,
    memory_items=self.context.memory.get_session_items(),
    tool_descriptions=tool_descriptions,
    prompt_path=prompt_path,
    step_num=step + 1,
    max_steps=max_steps,
)
```

**Solution:** Now when `user_input_override` is set (after FURTHER_PROCESSING_REQUIRED), the LLM receives the search results and can synthesize the final answer.

## Execution Flow Comparison

### Before Fix:

```
Step 1:
  Input: "What is relationship between Gensol and Go-Auto?"
  Plan: Search for "Gensol Go-Auto relationship"
  Result: [5 search results]
  Output: FURTHER_PROCESSING_REQUIRED
  
Step 2:
  Input: "What is relationship between Gensol and Go-Auto?" ❌ (same)
  Plan: Search for "Gensol Go-Auto relationship" ❌ (same)
  Result: [5 search results] ❌ (same)
  Output: FURTHER_PROCESSING_REQUIRED ❌ (same)
  
Step 3:
  Input: "What is relationship between Gensol and Go-Auto?" ❌ (same)
  Plan: Search for "Gensol Go-Auto relationship" ❌ (same)
  Output: Max steps reached 😞
```

### After Fix:

```
Step 1:
  Input: "What is relationship between Gensol and Go-Auto?"
  Plan: Search for "Gensol Go-Auto relationship"
  Result: [5 search results]
  Output: FURTHER_PROCESSING_REQUIRED
  
Step 2:
  Input: "Your last tool produced: [5 search results]" ✅ (different)
  Plan: Synthesize answer from provided results ✅ (no tool calls)
  Result: Comprehensive answer about fraud scheme ✅
  Output: FINAL_ANSWER: "Go-Auto was an auto dealership..." 🎉
```

## Key Insight

The bug was a **data flow issue**, not a prompt engineering issue. The LLM was making the correct decision based on the input it received - it just wasn't receiving the right input!

**Lesson:** When debugging agent loops, always verify that data is flowing correctly between components before assuming the LLM is making bad decisions.

