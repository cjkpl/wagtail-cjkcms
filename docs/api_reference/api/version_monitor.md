# Version monitor

## Purpose

The purpose of this feature is to enable easy monitoring of setups with multiple websites, where it is easy to get 
forget about keeping all websites up to date with software components. 

Administrator can easily implement a dashboard for simultaneous monitoring of multiple websites, making sure that 
software components are up to date everywhere.

## Description

In order to enable remote monitoring of versions of basic software components (django, wagtail, cms), a new api route 
has been added:
/api/versions/<TOKEN_MIN_12_CHARACTERS>/

This returns a JSON response with versions of key software components.

For security, it has been disabled by default. Two settings entries control access to the feature.
Set them in your local settings, to enable monitoring:

```
CJKCMS_VERSION_MONITOR_TOKEN = "123456789ABCDEF" # token - min 12 chars
CJKCMS_VERSION_MONITOR_ALLOWED_DOMAINS = ["*"] # allowed domains - by default blank
```

## Output

If an api call does not pass security checks, 403 is returned. If security checks are ok, the following type of JSON response is returned:

```json
{
    "python": "3.12.3 (main, May 27 2024, 19:00:21) [GCC 11.4.0]",
    "django": "5.0.6",
    "wagtail": "6.1.2",
    "cjkcms": "24.6.1"
}
```