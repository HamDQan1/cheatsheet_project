import markdown
from django import template
import bleach
from django.template.defaultfilters import stringfilter


ALLOWED_TAGS = [
    'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'em', 'b', 'i', 'u', 's', 'mark',
    'blockquote', 'pre', 'code',
    'ul', 'ol', 'li',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'a', 'details', 'summary'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a': ['href', 'title'],
    'code': ['class'],
}


register = template.Library()

@register.filter
@stringfilter
def markdown_to_html(text):
    html = markdown.markdown(
        text,
        extensions=[
            'fenced_code',
            'tables',
            'attr_list',          # {.class} or {#id}
            'pymdownx.arithmatex',# LaTeX math: $E = mc^2$
            'pymdownx.betterem',  # Smart emphasis
            'pymdownx.caret',     # Superscript: ^2^
            'pymdownx.mark',      # Highlight: ==text==
            'pymdownx.tilde',     # Strikethrough: ~~text~~
            'pymdownx.tasklist',  # - [x] Task
            'pymdownx.superfences',  # Nested code, Mermaid support
            'pymdownx.highlight', # Custom code highlighting (optional)
            'pymdownx.snippets',  # Include other files (advanced)
            'pymdownx.details',
        ],
        extension_configs={
            'pymdownx.superfences': {
                'custom_fences': [
                    {
                        'name': 'mermaid',
                        'class': 'mermaid',
                        'format': lambda src, lang, info, config: f'<pre><code class="mermaid">{src}</code></pre>'
                    }
                ]
            }
        },

        output_format='html5',
    )

    # 2. Sanitize (belt-and-suspenders)
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=False  # ← Important: don't strip, but we won't have bad tags anyway
    )
    
    return clean_html