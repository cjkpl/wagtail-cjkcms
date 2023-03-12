# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "{{ secret_key }}"

# Add your site's domain name(s) here. Disabled by default on localhost.
# ALLOWED_HOSTS = ["{{ domain }}"]

# Default email address used to send messages from the website.
DEFAULT_FROM_EMAIL = "{{ sitename }} <info@{{ domain_nowww }}>"

# A list of people who get error notifications.
ADMINS = [
    ("Administrator", "admin@{{ domain_nowww }}"),
]

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = DEFAULT_FROM_EMAIL
