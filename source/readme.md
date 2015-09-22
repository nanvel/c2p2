created: 2015-01-01
labels: Public

[TOC]

# MarkdownPages features

## Headers

```markdown
# H1
## H2
### H3
```

## List

```markdown
- item 1
- item 2
```

- item 1
- item 2

## Image

```markdown
![Image title](image.png)
```

![Image example](https://s3-us-west-2.amazonaws.com/fahlo-p0/0cd82267-3158-423f-b5df-c3e72545bb12/0b25030f/6aed/4a78/8896/decbdc2d1c98/50.100.jpg)

## Code

```python
import datetime
```

## TOC - Table of contents

```markdown
[TOC]
```

## Admonition

Danger:

```markdown
!!! danger "Danger ..."
    Danger details ...
```

!!! danger "Danger ..."
    Danger details ...

Error:

```markdown
!!! error "Error ..."
    Error details ...
```

!!! error "Error ..."
    Error details ...

Warning:

```markdown
!!! warning "Some warning ..."
    Warning description ...
```

!!! warning "Some warning ..."
    Warning description ...

Caution:

```markdown
!!! caution "Caution ..."
    Caution details ...
```

!!! caution "Caution ..."
    Caution details ...

Attention:

```markdown
!!! attention "Attention ..."
    Attention details ...
```

!!! attention "Attention ..."
    Attention details ...

Important:

```markdown
!!! important "Important ..."
    Important details ...
```

!!! important "Important ..."
    Important details ...

Note:

```markdown
!!! note "Test notes ..."
    Note ...
```

!!! note "Test notes ..."
    Note ...

Hint:

```markdown
!!! hint "Hint ..."
    Hint details ...
```

!!! hint "Hint ..."
    Hint details ...

Tip:

```markdown
!!! tip "Tip ..."
    Tip details ...
```

!!! tip "Tip ..."
    Tip details ...

## Links

```markdown
inline [text](http://google.com "Link description")
```

inline [text](http://google.com "Link description")

## API

```markdown
!API! POST:/accounts/{n} [accounts:edit, accounts:block]
    "username", "str", "required", "4 chars minimal length"
    "password", "str", "required", ""
```

!API! POST:/accounts/{n} [accounts:edit, accounts:block]
    "username", "str", "required", "4 chars minimal length"
    "password", "str", "required", ""
