"""
c25k_utils/accessibility.py
Handles accessibility features for high-contrast and large-font options.
"""


def apply_accessibility_options(
    export_data: str, high_contrast: bool = False, large_font: bool = False
) -> str:
    """
    Apply accessibility modifications to export data.

    Args:
        export_data: The export data (e.g., HTML, Markdown, etc.)
        high_contrast: Whether to apply high contrast styling
        large_font: Whether to apply large font styling

    Returns:
        Modified export data with accessibility enhancements
    """
    if not (high_contrast or large_font):
        return export_data

    # For HTML content, add CSS styling
    if "<html>" in export_data.lower() or "<body>" in export_data.lower():
        return _apply_html_accessibility(export_data, high_contrast, large_font)

    # For Markdown content, add accessibility annotations
    if export_data.startswith("#") or "##" in export_data:
        return _apply_markdown_accessibility(export_data, high_contrast, large_font)

    # For plain text, just return as-is (no styling possible)
    return export_data


def _apply_html_accessibility(html_content: str, high_contrast: bool, large_font: bool) -> str:
    """Apply accessibility styling to HTML content."""
    styles = []

    if high_contrast:
        styles.append(
            """
        body { 
            background-color: #000000 !important; 
            color: #ffffff !important; 
        }
        .workout { 
            background-color: #000080 !important; 
            color: #ffffff !important; 
            border: 2px solid #ffffff !important;
        }
        .rest-day { 
            background-color: #800000 !important; 
            color: #ffffff !important; 
        }
        """
        )

    if large_font:
        styles.append(
            """
        body { 
            font-size: 18px !important; 
            line-height: 1.6 !important; 
        }
        h1 { 
            font-size: 32px !important; 
        }
        h2 { 
            font-size: 28px !important; 
        }
        h3 { 
            font-size: 24px !important; 
        }
        """
        )

    if styles:
        style_block = f"<style>{''.join(styles)}</style>"
        # Insert before closing head tag or at beginning of body
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{style_block}</head>")
        elif "<body>" in html_content:
            html_content = html_content.replace("<body>", f"<body>{style_block}")
        else:
            html_content = f"{style_block}\n{html_content}"

    return html_content


def _apply_markdown_accessibility(
    markdown_content: str, high_contrast: bool, large_font: bool
) -> str:
    """Apply accessibility annotations to Markdown content."""
    if high_contrast or large_font:
        # Add accessibility note at the top
        accessibility_note = "\n**Accessibility Options Applied:**"
        if high_contrast:
            accessibility_note += " High Contrast"
        if large_font:
            accessibility_note += " Large Font"
        accessibility_note += "\n\n---\n\n"

        # Find the first header and insert after it
        lines = markdown_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("#"):
                lines.insert(i + 1, accessibility_note)
                break
        else:
            # No header found, add at beginning
            lines.insert(0, accessibility_note)

        markdown_content = "\n".join(lines)

    return markdown_content
