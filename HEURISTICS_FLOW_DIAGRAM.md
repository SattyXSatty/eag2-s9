# Heuristics Flow Diagram

## Complete Flow with All 10 Heuristics

```mermaid
flowchart TD
    Start([User Input]) --> Q1[Heuristic 1:<br/>Remove Sensitive Data]
    
    Q1 --> Q1Check{Contains PII?}
    Q1Check -->|Yes| Q1Mask[Mask with [REDACTED]]
    Q1Check -->|No| Q2
    Q1Mask --> Q2[Heuristic 2:<br/>Stop Prompt Injection]
    
    Q2 --> Q2Check{Injection Pattern?}
    Q2Check -->|Yes| Reject1[❌ REJECT<br/>Show Error]
    Q2Check -->|No| Q3[Heuristic 3:<br/>Trim & Normalize]
    
    Q3 --> Q3Process[Remove extra spaces<br/>Fix punctuation]
    Q3Process --> Q4[Heuristic 4:<br/>Limit Query Length]
    
    Q4 --> Q4Check{Length > 2000?}
    Q4Check -->|Yes| Q4Truncate[Truncate + Warning]
    Q4Check -->|No| Q5
    Q4Truncate --> Q5[Heuristic 5:<br/>Detect Meaningless]
    
    Q5 --> Q5Check{Meaningful?}
    Q5Check -->|No| Reject2[❌ REJECT<br/>Ask for details]
    Q5Check -->|Yes| Process[✅ Query Validated<br/>Send to Agent]
    
    Process --> Agent[Agent Processing<br/>Perception → Decision → Action]
    
    Agent --> R6[Heuristic 6:<br/>Safety Check]
    
    R6 --> R6Check{Contains PII/Profanity?}
    R6Check -->|Yes| R6Mask[Mask with [REDACTED]]
    R6Check -->|No| R7
    R6Mask --> R7[Heuristic 7:<br/>System Leakage Check]
    
    R7 --> R7Check{System Info?}
    R7Check -->|Yes| R7Remove[Remove leaking sentences]
    R7Check -->|No| R8
    R7Remove --> R8[Heuristic 8:<br/>Relevance Check]
    
    R8 --> R8Check{Relevant to Query?}
    R8Check -->|No| Reject3[❌ REJECT<br/>Off-topic]
    R8Check -->|Yes| R9[Heuristic 9:<br/>Hallucination Guard]
    
    R9 --> R9Check{Suspicious Content?}
    R9Check -->|Yes| R9Warn[⚠️ Add Warning]
    R9Check -->|No| R10
    R9Warn --> R10[Heuristic 10:<br/>Clean Formatting]
    
    R10 --> R10Process[Remove HTML<br/>Fix spacing<br/>Clean output]
    R10Process --> Output[✅ Response Validated<br/>Return to User]
    
    Reject1 --> End([End])
    Reject2 --> End
    Reject3 --> End
    Output --> End
    
    style Q1 fill:#e1f5ff
    style Q2 fill:#fff4e1
    style Q3 fill:#ffe1e1
    style Q4 fill:#ffebe1
    style Q5 fill:#e1ffe1
    style R6 fill:#f0e1ff
    style R7 fill:#ffe1f0
    style R8 fill:#e1fff0
    style R9 fill:#fff0e1
    style R10 fill:#f0ffe1
    style Reject1 fill:#ffcccc
    style Reject2 fill:#ffcccc
    style Reject3 fill:#ffcccc
    style Output fill:#ccffcc
```

## Detailed Heuristic Pipeline

### Query Heuristics (Pre-Processing)

```mermaid
sequenceDiagram
    participant User
    participant H1 as Heuristic 1<br/>Sensitive Data
    participant H2 as Heuristic 2<br/>Injection
    participant H3 as Heuristic 3<br/>Normalize
    participant H4 as Heuristic 4<br/>Length
    participant H5 as Heuristic 5<br/>Meaningful
    participant Agent
    
    User->>H1: "My email is john@example.com, what is AI?"
    H1->>H1: Detect email pattern
    H1->>H2: "My email is [REDACTED_EMAIL], what is AI?"
    Note over H1: ⚠️ Warning: Redacted email
    
    H2->>H2: Check injection patterns
    H2->>H3: No injection detected ✓
    
    H3->>H3: Normalize whitespace
    H3->>H4: Cleaned text
    
    H4->>H4: Check length (< 2000)
    H4->>H5: Length OK ✓
    
    H5->>H5: Check if meaningful
    H5->>Agent: ✅ Valid query
    Note over H5: Query validated
```

### Response Heuristics (Post-Processing)

```mermaid
sequenceDiagram
    participant Agent
    participant H6 as Heuristic 6<br/>Safety
    participant H7 as Heuristic 7<br/>Leakage
    participant H8 as Heuristic 8<br/>Relevance
    participant H9 as Heuristic 9<br/>Hallucination
    participant H10 as Heuristic 10<br/>Formatting
    participant User
    
    Agent->>H6: "As an AI model, AI is machine learning..."
    H6->>H6: Check for PII/profanity
    H6->>H7: No issues ✓
    
    H7->>H7: Detect "As an AI model"
    H7->>H8: "AI is machine learning..."
    Note over H7: ⚠️ Removed system leakage
    
    H8->>H8: Calculate keyword overlap
    H8->>H8: Query: "what is AI"<br/>Response: "AI is machine learning"
    H8->>H9: Overlap: 50% ✓
    
    H9->>H9: Check for suspicious URLs
    H9->>H9: Check for fake citations
    H9->>H10: No hallucinations ✓
    
    H10->>H10: Remove extra spaces
    H10->>H10: Strip HTML tags
    H10->>User: ✅ "AI is machine learning..."
    Note over H10: Response validated
```

## Decision Tree

```mermaid
graph TD
    Start([User Input]) --> Q1{Contains<br/>Sensitive Data?}
    
    Q1 -->|Yes| Mask1[Mask & Continue]
    Q1 -->|No| Q2{Prompt<br/>Injection?}
    
    Mask1 --> Q2
    Q2 -->|Yes| Reject1[❌ REJECT]
    Q2 -->|No| Q3{Needs<br/>Normalization?}
    
    Q3 -->|Yes| Norm[Normalize & Continue]
    Q3 -->|No| Q4{Length<br/>> 2000?}
    
    Norm --> Q4
    Q4 -->|Yes| Trunc[Truncate & Continue]
    Q4 -->|No| Q5{Meaningful?}
    
    Trunc --> Q5
    Q5 -->|No| Reject2[❌ REJECT]
    Q5 -->|Yes| Process[Process Query]
    
    Process --> R6{Response<br/>Safe?}
    
    R6 -->|No| Mask2[Mask & Continue]
    R6 -->|Yes| R7{System<br/>Leakage?}
    
    Mask2 --> R7
    R7 -->|Yes| Remove[Remove & Continue]
    R7 -->|No| R8{Relevant?}
    
    Remove --> R8
    R8 -->|No| Reject3[❌ REJECT]
    R8 -->|Yes| R9{Hallucination?}
    
    R9 -->|Yes| Warn[⚠️ Warn & Continue]
    R9 -->|No| R10{Needs<br/>Formatting?}
    
    Warn --> R10
    R10 -->|Yes| Format[Format & Continue]
    R10 -->|No| Output[✅ OUTPUT]
    
    Format --> Output
    
    style Reject1 fill:#ffcccc
    style Reject2 fill:#ffcccc
    style Reject3 fill:#ffcccc
    style Output fill:#ccffcc
```

## Statistics Flow

```mermaid
graph LR
    Input[1000 Queries] --> H1[Heuristic 1]
    H1 -->|50 masked| H2[Heuristic 2]
    H1 -->|950 clean| H2
    
    H2 -->|10 rejected| Reject1[❌ 10]
    H2 -->|990 passed| H3[Heuristic 3]
    
    H3 -->|200 normalized| H4[Heuristic 4]
    H3 -->|790 clean| H4
    
    H4 -->|5 truncated| H5[Heuristic 5]
    H4 -->|985 ok| H5
    
    H5 -->|20 rejected| Reject2[❌ 20]
    H5 -->|970 passed| Process[Agent Processing]
    
    Process --> R6[Heuristic 6]
    R6 -->|30 masked| R7[Heuristic 7]
    R6 -->|940 clean| R7
    
    R7 -->|100 cleaned| R8[Heuristic 8]
    R7 -->|870 clean| R8
    
    R8 -->|15 rejected| Reject3[❌ 15]
    R8 -->|955 passed| R9[Heuristic 9]
    
    R9 -->|50 warnings| R10[Heuristic 10]
    R9 -->|905 clean| R10
    
    R10 -->|150 formatted| Output[✅ 955 Output]
    R10 -->|805 clean| Output
    
    Reject1 --> Total[Total Rejected: 45]
    Reject2 --> Total
    Reject3 --> Total
    
    style Reject1 fill:#ffcccc
    style Reject2 fill:#ffcccc
    style Reject3 fill:#ffcccc
    style Output fill:#ccffcc
    style Total fill:#ffcccc
```

**Success Rate:** 95.5% (955/1000 queries successfully processed)
**Rejection Rate:** 4.5% (45/1000 queries rejected for safety/quality)

