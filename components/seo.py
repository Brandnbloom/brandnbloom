import streamlit.components.v1 as components

def inject_all(
    # SEO
    title: str = "BloomScore Pro – AI Brand Intelligence",
    description: str = "BloomScore Pro gives creators and businesses AI-powered branding audits, competitor analysis, and growth insights.",
    url: str = "https://www.bloomscorepro.com",
    image_url: str = "https://www.bloomscorepro.com/assets/cover.png",
    keywords: str = "branding audit, instagram analytics, ai marketing, competitor analysis, growth tools, creator tools",

    # Branding
    favicon_url: str = "https://www.bloomscorepro.com/assets/favicon.png",

    # Analytics
    google_analytics_id: str = "G-XXXXXXXXXX",   # Replace
    facebook_pixel_id: str = "XXXXXXXXXXXXXXX",  # Replace

    # Chats
    intercom_app_id: str = "your_intercom_app_id",  # Replace
    tawk_property_id: str = "your_tawk_property_id", # Replace
    tawk_widget_id: str = "your_tawk_widget_id",     # Replace

    enable_intercom: bool = False,
    enable_tawk: bool = False,
):
    """
    Injects SEO tags, favicon, Google Analytics, Facebook Pixel,
    and optional chat widgets into Streamlit via invisible HTML.
    """
    html = f"""
    <head>
      <!-- Basic SEO -->
      <title>{title}</title>
      <meta name="description" content="{description}">
      <meta name="keywords" content="{keywords}">
      <meta name="viewport" content="width=device-width, initial-scale=1">

      <!-- Canonical -->
      <link rel="canonical" href="{url}" />

      <!-- Favicon -->
      <link rel="icon" href="{favicon_url}" type="image/png">

      <!-- Open Graph -->
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{description}">
      <meta property="og:image" content="{image_url}">
      <meta property="og:url" content="{url}">
      <meta property="og:type" content="website">

      <!-- Twitter -->
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{title}">
      <meta name="twitter:description" content="{description}">
      <meta name="twitter:image" content="{image_url}">

      <!-- Schema JSON-LD -->
      <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "{title}",
        "url": "{url}",
        "description": "{description}",
        "image": "{image_url}"
      }}
      </script>

      <!-- Google Analytics -->
      <script async src="https://www.googletagmanager.com/gtag/js?id={google_analytics_id}"></script>
      <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{google_analytics_id}');
      </script>

      <!-- Facebook Pixel -->
      <script>
        !function(f,b,e,v,n,t,s)
        {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '{facebook_pixel_id}');
        fbq('track', 'PageView');
      </script>
      <noscript><img height="1" width="1" 
        src="https://www.facebook.com/tr?id={facebook_pixel_id}&ev=PageView&noscript=1"
      /></noscript>
    </head>
    """

    # Optional Intercom Chat
    if enable_intercom:
        html += f"""
        <script>
          window.intercomSettings = {{
            app_id: "{intercom_app_id}"
          }};
        </script>
        <script>
          (function(){{
            var w = window;
            var ic = w.Intercom;
            if (typeof ic === "function") {{
              ic("reattach_activator");
              ic("update", w.intercomSettings);
            }} else {{
              var d = document;
              var i = function(){{ i.c(arguments) }};
              i.q = [];
              i.c = function(args){{ i.q.push(args) }};
              w.Intercom = i;
              function l() {{
                var s = d.createElement("script");
                s.type = "text/javascript";
                s.async = true;
                s.src = "https://widget.intercom.io/widget/{intercom_app_id}";
                var x = d.getElementsByTagName("script")[0];
                x.parentNode.insertBefore(s, x);
              }}
              if (document.readyState === "complete") {{
                l();
              }} else {{
                w.attachEvent ?
                  w.attachEvent("onload", l) :
                  w.addEventListener("load", l, false);
              }}
            }}
          }})();
        </script>
        """

    # Optional Tawk.to Chat
    if enable_tawk:
        html += f"""
        <script async data-cfasync="false" src="https://embed.tawk.to/{tawk_property_id}/{tawk_widget_id}"></script>
        """

    components.html(html, height=0)
