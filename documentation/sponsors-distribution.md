# Sponsors guidance distribution integration

[日本語](sponsors-distribution_ja.md)

Source changes for a future release; no published package is updated by this change.
Linux retains its existing behavior. FreeBSD, NetBSD and OpenBSD use the same dialog.
Windows requires the activated, unpackaged, unfrozen uv profile. Ordinary Windows
source launches and MSIX processes do not show this guidance. Native Windows ARM64
uv remains a separate, unfinished dependency/acceptance task.

Homebrew must install `launch_homebrew.py` alongside `main.py` and the application
files, and change its `bin/folimeld` wrapper to invoke `launch_homebrew.py` using
the formula's private Python. This calls `run(distribution="homebrew")`; ordinary
`main.py` and frozen macOS applications do not enable the dialog. The explicit
label is a presentation switch, not proof of installation provenance.

For the next Homebrew source release, update its source URL/version/SHA-256 and:

```ruby
app.install "main.py", "launch_homebrew.py", "folimeld", "assets", "locales", "licenses", "LICENSE"
# In the existing wrapper, retaining the formula's private Python:
exec "#{libexec}/bin/python" "#{app}/launch_homebrew.py" "$@"
```

The wrapper line belongs inside the existing shell heredoc, not Ruby code.
Do not apply it to the old 0.3.3 archive: that archive lacks the new launcher.
The external tap formula and published source archives are unchanged in this task.

Acceptance on each target: open the dialog without opening a browser, click the
button and verify the exact HTTPS URL in the browser, verify failure guidance
when the desktop cannot open a URL, close/reopen the dialog, check translations,
and confirm excluded distributions have no Sponsors menu. A successful openUrl
return only confirms dispatch, not successful loading of the web page.
