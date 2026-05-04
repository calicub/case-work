---
icon: simple/markdown
---

# Markdown in 5min

## Headers
```
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header
```

## Text formatting
```
**bold text**
*italic text*
***bold and italic***
~~strikethrough~~
`inline code`
```

## Links and images
```
[Link text](https://example.com)
[Link with title](https://example.com "Hover title")
![Alt text](image.jpg)
![Image with title](image.jpg "Image title")
```

## Lists
```
Unordered:
- Item 1
- Item 2
  - Nested item

Ordered:
1. First item
2. Second item
3. Third item
```

## Blockquotes
```
> This is a blockquote
> Multiple lines
>> Nested quote
```

## Code blocks

Basic fenced block with language:

````
```python
print("Hello, world!")
```
````

With a title bar (use the `codeblock` snippet):

````
```python title="example.py"
print("Hello, world!")
```
````

For log files use `log` or `text` to skip syntax highlighting:

`````markdown
```log title="error.log"
2026-05-03 14:32:01 ERROR Connection timed out
```
`````

## Tables
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Data     | Data     |
| Row 2    | Data     | Data     |
```

## Horizontal rule
```
---
or
***
or
___
```

## Task lists
```
- [x] Completed task
- [ ] Incomplete task
- [ ] Another task
```

## Escaping characters

```text
Use backslash to escape: \* \_ \# \`
```

## Line breaks

```text
End a line with two spaces  
to create a line break.

Or use a blank line for a new paragraph.
```

---

## Admonitions

Admonitions are colored callout boxes rendered by Zensical. The type controls the color and icon.

```markdown
!!! note "Optional custom title"
    Indented content goes here.
    All lines must be indented 4 spaces.
```

| Type | Color | Use for |
| ---- | ----- | ------- |
| `note` | Blue | General info |
| `tip` | Green | Helpful hints |
| `warning` | Orange | Caution / watch out |
| `danger` | Red | Destructive or irreversible actions |
| `info` | Teal | Context or background |
| `abstract` | Light blue | Summaries, remote support notes |

Collapsible admonition (closed by default):

```markdown
??? warning "Click to expand"
    Hidden content here.
```

Collapsible but open by default:

```markdown
???+ tip "Expanded by default"
    Visible content here.
```

---

## Icons & Emojis

Zensical supports icons from Lucide, FontAwesome, and Material icon sets using `:set/name:` syntax.

**Emojis** (shortcode format):

```markdown
:smile:   :warning:   :white_check_mark:   :x:
```

**Lucide icons:**

```markdown
:lucide-circle-check:   :lucide-alert-triangle:   :lucide-file-text:
```

**FontAwesome icons:**

```markdown
:fontawesome-solid-star:   :fontawesome-regular-file-pdf:   :fontawesome-brands-github:
```

**Material Design icons:**

```markdown
:material-check:   :material-close:   :material-alert:
```

!!! tip "Finding icons"
    Browse available icons at [lucide.dev](https://lucide.dev) for Lucide, or search [fontawesome.com/icons](https://fontawesome.com/icons) for FontAwesome. Replace spaces with hyphens in the icon name.
