# Miro MCP Tools Reference

## Board Management

### create_board
Create a new Miro board.
```json
{
  "title": "Board Name",
  "description": "Optional description"
}
```

### get_boards
List all boards in workspace.
```json
{
  "limit": 20,
  "offset": 0
}
```
Returns: Array of `{ id, title, description, createdAt, modifiedAt }`

### get_board
Get specific board details.
```json
{
  "board_id": "uXjVN..."
}
```

## Items — Create

### create_sticky_note
```json
{
  "board_id": "uXjVN...",
  "content": "Note text here",
  "position": { "x": 0, "y": 0 },
  "geometry": { "width": 200, "height": 200 },
  "style": { "fillColor": "yellow" }
}
```
Colors: `yellow`, `blue`, `green`, `orange`, `red`, `gray`, `purple`, `pink`, `cyan`

### create_shape
```json
{
  "board_id": "uXjVN...",
  "type": "rectangle",
  "content": "Shape label",
  "position": { "x": 0, "y": 0 },
  "geometry": { "width": 300, "height": 200 },
  "style": {
    "fillColor": "#4262ff",
    "borderColor": "#000000",
    "borderWidth": 2
  }
}
```
Types: `rectangle`, `circle`, `triangle`, `diamond`, `parallelogram`, `cylinder`, `cloud`, `hexagon`, `star`

### create_connector
```json
{
  "board_id": "uXjVN...",
  "startItem": { "id": "item1_id" },
  "endItem": { "id": "item2_id" },
  "style": {
    "strokeColor": "#000000",
    "strokeWidth": 2,
    "strokeStyle": "normal"
  },
  "captions": [{ "content": "Label" }]
}
```
Stroke styles: `normal`, `dashed`, `dotted`

### create_frame
```json
{
  "board_id": "uXjVN...",
  "title": "Frame Title",
  "position": { "x": 0, "y": 0 },
  "geometry": { "width": 800, "height": 600 }
}
```

### create_card
```json
{
  "board_id": "uXjVN...",
  "title": "Card Title",
  "description": "Card details",
  "position": { "x": 0, "y": 0 },
  "assignee": { "userId": "user_id" },
  "dueDate": "2026-03-01"
}
```

### create_text
```json
{
  "board_id": "uXjVN...",
  "content": "<p>Text content</p>",
  "position": { "x": 0, "y": 0 },
  "style": { "fontSize": 24, "color": "#000000" }
}
```

### create_tag
```json
{
  "board_id": "uXjVN...",
  "title": "Tag Name",
  "fillColor": "red"
}
```
Then apply: `attach_tag({ item_id, tag_id })`

## Items — Read

### get_items
List all items on a board.
```json
{
  "board_id": "uXjVN...",
  "type": "sticky_note",
  "limit": 50
}
```
Filter by type: `sticky_note`, `shape`, `connector`, `frame`, `card`, `text`, `tag`

### get_item
Get specific item details.
```json
{
  "board_id": "uXjVN...",
  "item_id": "item_id"
}
```

## Items — Update

### update_item
Modify an existing item.
```json
{
  "board_id": "uXjVN...",
  "item_id": "item_id",
  "position": { "x": 100, "y": 200 },
  "content": "Updated text"
}
```

### update_item_position
Move an item.
```json
{
  "board_id": "uXjVN...",
  "item_id": "item_id",
  "position": { "x": 500, "y": 300 }
}
```

## Items — Delete

### delete_item
Remove an item from board.
```json
{
  "board_id": "uXjVN...",
  "item_id": "item_id"
}
```

## Common Patterns

### Grid Layout Helper
```
For N items in C columns with S spacing:
  row = floor(index / C)
  col = index % C
  x = col * S
  y = row * S
```

### Batch Create
Create multiple items by looping with incremented positions:
```
items = ["Item 1", "Item 2", "Item 3"]
for i, item in enumerate(items):
    create_sticky_note(content=item, x=0, y=i*250)
```
