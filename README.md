# Alfred Arduino CLI

Python based Workflow to run the Arduino CLI from [Alfred](https://www.alfredapp.com).

![Screenshot with a list of boards](images/screenshot.png)

This project has been written as the companion example for the post https://zmoog.dev/post/alfred-workflow on my [personal website](https://zmoog.dev).

## Development

**Disclaimer**: this is a sample project for a blog post, so probably very few (if any!) people will be interested in it. The ROI in value for the users of me writing a comprehensive documentation, or automate the build, is probably pretty low.

### Requirements

 * [Poetry](https://python-poetry.org/) to handle the project dependencies.
 * Python 2.7 — I know, it's obsolete, but it's what Apple shipped with macOS for years, so now we're hostages.


### Install required libraries

Export the requirements file from Poetry:
```
$ poetry export --output requirements.txt 
```

Install dependencies into the `libs` directory:
```bash

# create a libs directory to host all the dependencies
$ mkdir libs

$ pip install -r requirements.txt --target libs
```

### Fire up a virtualenv

```shell
$ poetry shell
```

### Test it!

```shell
$ export LC_ALL=en_US.UTF-8
$ export LANG=en_US.UTF-8
```

Run a simple command like `version` to see if works:
```shell
$ python arduino-cli.py version
.
<?xml version="1.0" encoding="utf-8"?>
<items>
  <item valid="no">
    <title>0.16.0</title>
    <subtitle>version</subtitle>
  </item>
  <item valid="no">
    <title>c977a2382c2e7770b3eedc43e6a9d41f4a6c3483</title>
    <subtitle>Commit</subtitle>
  </item>
  <item valid="no">
    <title>alpha</title>
    <subtitle>Status</subtitle>
  </item>
</items>

```
