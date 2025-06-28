import streamlit.components.v1 as components

def inject_seo():
    components.html("""
        <head>
          <title>Brand n Bloom – Restaurant AI Tools</title>
          <meta name="description" content="AI tools for restaurant branding, consumer behavior analysis, and competitor benchmarking.">
          <meta name="keywords" content="restaurant marketing, AI tools, branding audit, consumer behavior, digital menu">
          <meta property="og:title" content="Brand n Bloom – AI Tools for Restaurants" />
          <meta property="og:description" content="Use AI to audit, analyze, and optimize your restaurant's brand and reach." />
          <meta property="og:image" content="https://www.brand-n-bloom.com/assets/banner.png" />
          <meta property="og:url" content="https://www.brand-n-bloom.com" />
          <meta name="twitter:card" content="summary_large_image">
          <meta name="twitter:title" content="Brand n Bloom">
          <meta name="twitter:description" content="Grow your restaurant with AI-powered branding insights.">
          <meta name="twitter:image" content="https://www.brand-n-bloom.com/assets/banner.png">
          <link rel="canonical" href="https://www.brand-n-bloom.com" />
        </head>
    """, height=0)
