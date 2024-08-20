# Instructions for Windows

Here is a full tutorial on how to get started with the Heexy browser

System Requirements
-------------------

-  **Memory:** 4GB RAM minimum, 8GB+ recommended.
-  **Disk Space:** At least 40GB of free disk space.
-  **Operating System:** Windows 10 or 11.

Recommended (For Windows 11 Users)
----------------------------------
[Setup a Dev Drive instructions](https://learn.microsoft.com/en-us/windows/dev-drive/#how-to-set-up-a-dev-drive)
-  A Dev Drive has been shown to make Firefox builds and VCS operations 5-10% faster.
-  This guide assumes no Dev Drive, so all instructions of ``C:\mozilla-source`` should be to your Dev Drive letter instead (eg: ``D:\mozilla-source``), as your ``C:\`` drive can never be a Dev Drive.

## 1. Required files

- [Download Mozilla Build Tools](https://ftp.mozilla.org/pub/mozilla/libraries/win32/MozillaBuildSetup-Latest.exe) **(MUST BE ON THE SAME DISK AS THE SOURCE CODE!)**
- You need to download the [source code of Heexy browser](https://github.com/Heexy/heexy-browser/) *(we recommend Dev Drive for the place where you want it)*
- Make sure you have the source code and build tools on the same disk!
- **Download Visual Studio 2022**
- **You must have Python 3.11 or higher**

## 2. Prepare the source code

Then open the **heexy-browser** folder and start the terminal in it and insert a command:
```bash
./mach bootstrap
```
Terminal will Answer something like this:
```
Please choose the version of Firefox you want to build (see note above):
  1. Firefox for Desktop Artifact Mode [default]
  2. Firefox for Desktop
  3. GeckoView/Firefox for Android Artifact Mode
  4. GeckoView/Firefox for Android
  5. SpiderMonkey JavaScript engine
Your choice:
```
**Choose first mode Firefox for Desktop Artifact Mode [default]** and enter, then wait when the terminal finish everything.


## 3. Building source code
After successful completion, run this command which builds and prepares the source code to run.
```bash
./mach build
```
**Note: This may take a few minutes the terminal may type strange things and act like it is in a smiley, please wait the process may take 10 minutes or more!**

When finished, you can run the code:
```bash
./mach run
```

# Important notes!
After a change in the code, you must always run this command,
**./mach build** without this, the changes will not take effect.

**Are you unclear about anything?** you can try reading the official documentation of the Firefox source code for windows [here](https://firefox-source-docs.mozilla.org/setup/windows_build.html)