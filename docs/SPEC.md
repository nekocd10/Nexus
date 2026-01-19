# Nexus Programming Language Specification

## Philosophy: Completely Original Language Design

Nexus is a fundamentally different language with unique syntax, paradigms, and concepts that don't exist in mainstream languages.

## Core Unique Features

### 1. CONTEXT-BASED PROGRAMMING (Not functions, not objects)
Instead of functions/methods, Nexus uses **Contexts** - named execution scopes with inputs and outputs:

```nexus
~context add_numbers
  @in: a, b
  @out: result
  result => a + b
```

### 2. FLOW ARROWS (Explicit data flow)
Data flows through `=>` (forward), `<=` (backward), `<>` (bidirectional):

```nexus
data => transform => output
value <= previous_context
```

### 3. POOLS (Unique data structures - not arrays or objects)
**Pools** are ordered, indexed collections with implicit iteration:

```nexus
[| 1, 2, 3, 4, 5 |]  # pool of numbers
[: name="Alice", age=30, city="NYC" :]  # keyed pool (like a map but different)
```

### 4. MUTATIONS (State management)
Use `@` symbol to mark values that change:

```nexus
@counter = 0
@counter ++> 1  # increment, result flows forward
```

### 5. CONDITION GATES (Unique control flow)
Instead of if/else, use condition gates with `?`:

```nexus
value ? > 10
  => "large"
| < 10
  => "small"
| else
  => "medium"
```

### 6. REACTION CHAINS (Unique loops)
Instead of while/for, use reactions that trigger on conditions:

```nexus
~reaction process_items
  @items
  ? @items.length > 0
    => process @items[0]
    @items => @items.tail
```

### 7. CHANNEL OPERATORS (Unique piping)
Pass data through channels with `@>`, `<@`, `@<>`:

```nexus
data @> transform @> output
input <@ previous <@ start
```

### 8. ASPECT SYSTEM (Cross-cutting concerns)
Mark behaviors that apply across contexts:

```nexus
#[aspect: logging]
#[aspect: security]
~context protected_operation
  @in: data
  @out: result
```

### 9. QUANTUM OPERATORS (Multiple possibilities)
Handle alternatives elegantly:

```nexus
value ?: a | b | c  # try a, if fails try b, if fails try c
```

### 10. RESONANCE BLOCKS (Grouped operations)
Named blocks that resonate together:

```nexus
{~ resonance process_payment
  validate => charge => confirm
~}
```

## Syntax Components

### Variable Declaration
```nexus
#var x = 10           # immutable binding
@var counter = 0      # mutable state
```

### Contexts (Execution Blocks)
```nexus
~context name
  @in: param1, param2
  @out: result
  # body
```

### Flow Control
```nexus
~gate condition
  ? condition1 => action1
  | condition2 => action2
  | else => default_action
```

### Pools (Collections)
```nexus
[| 1, 2, 3 |]         # ordered pool
[: x=1, y=2 :]        # keyed pool
```

### Reactions (Loops)
```nexus
~reaction keep_going
  @state
  ? @state != done
    => process @state
    @state => update @state
```

### Data Flow
```nexus
input => step1 => step2 => output
@value ++> next_value
result <= source_context
```

## Example Programs

### Hello World
```nexus
~context main
  @out: message
  message => "Hello, Nexus!"
```

### Variables and Operations
```nexus
#var x = 10
#var y = 20
#var sum = x + y
sum => output
```

### Simple Context
```nexus
~context multiply
  @in: a, b
  @out: result
  result => a * b
```

### Conditional Gates
```nexus
~context classify
  @in: number
  @out: type
  
  number ? > 100
    => type = "large"
  | > 10
    => type = "medium"
  | else
    => type = "small"
```

### Pool Operations
```nexus
~context sum_pool
  @in: numbers [| |]
  @out: total
  
  @total = 0
  
  ~reaction add_items
    [| numbers |]
    ? @total => @total + item
```

### Reaction (Loop) with State
```nexus
~context countdown
  @in: start
  @out: sequence
  
  @current = start
  @sequence = [| |]
  
  ~reaction count_down
    ? @current >= 0
      @sequence => @sequence + @current
      @current ++> @current - 1
```

## Built-in Contexts

```nexus
~context output          # send to output
~context input           # receive input
~context type_of         # get type
~context length          # get length
~context reverse         # reverse pool
~context transform       # apply transformation
~context filter          # filter pool
~context accumulate      # reduce operation
```

## Unique Syntax Rules

1. **`~`** - Marks context/reaction definitions
2. **`@`** - Marks mutable state
3. **`#`** - Marks immutable bindings
4. **`=>`** - Forward flow
5. **`<=`** - Backward flow
6. **`?`** - Gate/condition marker
7. **`|`** - Alternative branch
8. **`[| |]`** - Ordered pool
9. **`[: :]`** - Keyed pool
10. **`@>`** - Channel operator
11. **`++>`** - Increment and flow
12. **`?:`** - Quantum operator

## Why It's Completely Different

- **No functions** - Uses contexts instead
- **No if/else** - Uses condition gates with `?`
- **No loops** - Uses reactions that trigger on state
- **No arrays/objects** - Uses pools (unique data structure)
- **No methods** - Data flows through channels
- **No return statements** - Results flow forward with `=>`
- **Aspect system** - Built-in cross-cutting concerns
- **Quantum operators** - Try multiple alternatives
- **Explicit data flow** - All movement marked with arrows
- **Mutable state marked** - `@` prefix shows what can change

This language is fundamentally different from every mainstream language and creates a new paradigm for thinking about programs.
