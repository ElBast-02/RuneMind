# RuneMind — Screen Design Index

These are **pre-implementation visual mockups** for the midterm feature flow. Commit the design images before writing the corresponding screen implementation. Images are design references, not evidence of functional features.

| Screen | Image | GitHub issue | Intended user flow |
|---|---|---|---|
| Dashboard (previously committed) | `dashboard-design.png` | Assign dedicated dashboard issue | Landing page for authenticated users |
| Login | `login-design.png` | **Assign newly created UI issue number** | Enter email and password → submit → view error or open dashboard |
| Registration | `register-design.png` | **Assign newly created UI issue number** | Enter username, email, password → submit → view validation or success |
| Character attributes | `character-design.png` | **Assign newly created character issue number** | Edit name and attributes → save via Flask API → persist to SQLite → reload saved values |

## Design decisions

- Forms use explicit labels and a prominent primary action to make the flow understandable.
- Both authentication screens include an error-message region for validation and failed requests.
- Registration asks only for the username, email, and password currently accepted by the API.
- Character editing includes an explicit Save action and success feedback; the example character values are illustrative, not real stored data.
- Dark backgrounds, gold borders, and crimson primary actions provide visual continuity with the existing RuneMind dashboard mockup.
- The designs show intended states, not simultaneous required states: error banners appear on failed submissions; success banners appear after successful saves.
- The character mockup shows three example stats (Strength, Vigor, Dexterity); final field selection should be documented in its issue before implementation.

## GitHub linking checklist

1. Create numbered UI/character issues with acceptance criteria and add them to the Kanban board.
2. Replace each **Assign** placeholder above with the real issue number.
3. Commit these images and this index to `docs/screens/` **before** writing corresponding HTML/JS.
4. Add Markdown image references to the corresponding issue descriptions, for example `![Login design](https://github.com/ElBast-02/RuneMind/blob/main/docs/screens/login-design.png)`.
5. If implementation changes the layout or user flow, update the mockups and record the design change.

**Note:** This package intentionally excludes `dashboard-design.png` because that file already exists in the repository. Keep the original file unchanged.
