from src.charts import PALETTE

FONT_FAMILY = "'IBM Plex Sans', 'Inter', system-ui, -apple-system, sans-serif"

LUCIDE_ICONS = {
    "target": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><circle cx='12' cy='12' r='6'/><circle cx='12' cy='12' r='2'/></svg>",
    "spark": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M5 3v4'/><path d='M19 17v4'/><path d='M3 5h4'/><path d='M17 19h4'/><path d='m6.5 6.5 3 3'/><path d='m14.5 14.5 3 3'/><path d='M10 2h4'/><path d='M10 22h4'/><path d='m7 7 2-2'/><path d='m15 15 2-2'/></svg>",
    "notes": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M19 21H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l6 6v10a2 2 0 0 1-2 2Z'/><path d='M14 3v4a2 2 0 0 0 2 2h4'/><path d='M9 15h6'/><path d='M9 19h6'/></svg>",
    "chart": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 3v18h18'/><path d='M7 13l3-3 4 4 5-5'/></svg>",
    "building": "<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 21h18'/><path d='M6 21V7l6-4 6 4v14'/><path d='M9 21v-6h6v6'/></svg>",
}

def get_global_styles():
    return f"""
        <style>
        :root {{
            --primary: {PALETTE["primary"]};
            --primary-dark: {PALETTE["primary_dark"]};
            --accent: {PALETTE["accent"]};
            --soft: {PALETTE["soft"]};
            --muted: {PALETTE["muted"]};
        }}
        html, body, [class*="css"]  {{
            font-family: {FONT_FAMILY};
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700;
            color: var(--primary-dark);
        }}
        /* Tag chips */
        div[data-baseweb="tag"], span[data-baseweb="tag"] {{
            background-color: var(--soft) !important;
            color: var(--primary-dark) !important;
            border: 1px solid #9bc7b3 !important;
        }}
        .stMultiSelect [data-baseweb="tag"] svg {{
            color: var(--primary-dark) !important;
        }}
        /* Top banner */
        .aire-banner {{
            background: var(--primary-dark);
            color: #f2fbff;
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 10px;
        }}
        .aire-banner strong {{ color: #f2fbff; }}
        .metric-card-title {{
            display: flex; gap: 6px; align-items: center;
            font-weight: 600;
            color: var(--primary-dark);
        }}
        .stTabs [role="tablist"] button {{
            background: transparent;
            border: none;
            color: var(--primary-dark);
            padding: 8px 12px;
            border-radius: 0;
            margin-right: 6px;
            box-shadow: none;
        }}
        .stTabs [role="tablist"] button[aria-selected="true"] {{
            background: transparent;
            border: none;
            color: var(--primary);
            box-shadow: inset 0 -2px 0 0 var(--primary);
        }}
        .stTabs [role="tablist"] button:hover {{
            background: transparent;
            border: none;
            color: var(--primary);
            box-shadow: inset 0 -2px 0 0 #b7dbe8;
        }}
        .stMetric > div {{
            background: #ffffff;
            border: 1px solid #e2ebf0;
            border-radius: 10px;
            padding: 8px 10px;
        }}
        .executive-card {{
            background:#f7fbfd;
            border:1px solid #dbe9f1;
            border-radius:10px;
            padding:14px 16px;
        }}
        .lucide {{ display:inline-flex; vertical-align:middle; }}
        .chip {{
            display:inline-flex;
            align-items:center;
            gap:6px;
            background:#eef6fa;
            color: var(--primary-dark);
            padding:6px 10px;
            border-radius:20px;
            border:1px solid #d2e5ee;
            font-size:12px;
            font-weight:600;
        }}
        .primary-btn {{
            background: {PALETTE["primary"]};
            color:#fff !important;
            padding:8px 14px;
            border-radius:8px;
            border:none;
        }}
        </style>
        """
