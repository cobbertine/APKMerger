# About

This Python3 tool automates the process required to convert a split APK into a single APK.

# Pre-requisites

It is expected that the user is familiar with ADB and decompiling APKs.

# Instructions


1. You must first determine the package name of the APK you wish to pull, running the command "```adb shell pm list packages```" is one method.
2. With the package name known, you must get the filepath of the Base APK and its components. For example:

```
> adb shell pm path com.example.someapp

package:/data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/base.apk
package:/data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/split_config.arm64_v8a.apk
package:/data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/split_config.en.apk
package:/data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/split_config.xxhdpi.apk
```

3. Create a new folder to hold these APKs and then pull each one into it:

```
adb pull /data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/base.apk
adb pull /data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/split_config.arm64_v8a.apk
adb pull /data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/split_config.en.apk
adb pull /data/app/com.company.app-rDbi7upLpZlKZLaJkge0jw==/split_config.xxhdpi.apk
```

4. Decompile each APK. The folders should look similar to below:
(If you use APK Studio, the folders will be named as below automatically)

```
base.apk-decompiled
split_config.arm64_v8a.apk-decompiled
split_config.en.apk-decompiled
split_config.xxhdpi.apk-decompiled
```

**NOTE**: The tool looks for one folder with the substring "base.apk" and any folders with the substring "split_config".

5. Copy this script into the same directory where the folders above are listed, such that running an "ls" command would look like:

```
APKMerger.py
base.apk-decompiled
split_config.arm64_v8a.apk-decompiled
split_config.en.apk-decompiled
split_config.xxhdpi.apk-decompiled
```

6. Run this tool. ```python3 APKMerger.py```.

7. Finally, you can now safely delete all of the "split_config" folders and build the "base.apk-decompiled" folder.