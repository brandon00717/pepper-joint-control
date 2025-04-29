<?xml version="1.0" encoding="UTF-8" ?>
<Package name="joint-control" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="." xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs />
    <Resources>
        <File name="icon" src="icon.png" />
        <File name="style" src="html/css/style.css" />
        <File name="index" src="html/index.html" />
        <File name="jquery-1.11.0.min" src="html/js/jquery-1.11.0.min.js" />
        <File name="main" src="html/js/main.js" />
        <File name="robotutils" src="html/js/robotutils.js" />
        <File name="joint" src="scripts/joint.py" />
        <File name="__init__" src="scripts/stk/__init__.py" />
        <File name="events" src="scripts/stk/events.py" />
        <File name="logging" src="scripts/stk/logging.py" />
        <File name="runner" src="scripts/stk/runner.py" />
        <File name="services" src="scripts/stk/services.py" />
        <File name="pose1" src="html/images/pose1.png" />
        <File name="README" src="README.md" />
    </Resources>
    <Topics />
    <IgnoredPaths>
        <Path src=".metadata" />
    </IgnoredPaths>
    <Translations auto-fill="en_US">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
    </Translations>
</Package>
