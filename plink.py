# version 0.0.3 - "purple cat"
__plinK_version__ = '0.0.3'

import os
import re
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Static, Input
from textual.suggester import SuggestFromList
# from textual import events
# from textual.reactive import reactive
import colorama
from colorama import Fore, Style
from rich.text import Text
from textual.widgets import RichLog
import asyncio
import yaml
import shutil
# from setuptools import copy_tree
import sys
import aiofiles
import time

# import nest_asyncio
# nest_asyncio.apply()
time.sleep(1)
commands = ["profile build", "profile push", "profile src build", "profile sync prefs", "build", "run", "clear cache",
            "rd", "mach", "close"]
# Initialize Colorama for handling colored output
colorama.init(autoreset=True)

startingdir = os.getcwd().replace("\\", "/")
session_id = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

build_dir = f"{startingdir}/obj-x86_64-pc-windows-msvc"  # placeholder
profile_dir = f"{startingdir}\\plinK_data\\profile"

if os.name != 'nt' and not sys.platform.startswith("linux"):
    print(f"{Fore.RED}The plinK build tool is not available on your system({sys.platform})")
    print("im sowwy :c")
    print("Theoretically plinK might just work if you remove this check, that checks the current os, "
          "and edit plinK.buildconfig to have the correct build dir but I cannot"
          "guarantee it.")
    print("If you think this is a mistake, simply remove this check")
    print("If you remove this check make sure to NOT commit with it removed")
    input(f"{Fore.RESET} Press enter to exit")
    quit(1)

try:
    os.makedirs("plinK_data")
    os.makedirs("plinK_data/logs")
except:
    pass


async def write_to_file(filename, data):
    async with aiofiles.open(filename, 'w') as f:
        await f.write(data)


async def read_from_file(filename):
    async with aiofiles.open(filename, 'r') as f:
        contents = await f.read()
        return contents


if os.path.exists(f"{startingdir}/plinK_data/redraw_logs.switch"):
    old_log_session_id = asyncio.run(read_from_file(f"{startingdir}/plinK_data/redraw_logs.switch"))
    if old_log_session_id == "" or old_log_session_id == " " or old_log_session_id == "\n":
        redraw_logs = False
    else:
        redraw_logs = True
        os.remove(f"{startingdir}/plinK_data/redraw_logs.switch")
else:
    redraw_logs = False


class RedrawEventTrigger(Exception):
    def __init__(self, message="Redraw event"):
        super(RedrawEventTrigger, self).__init__(message)


def load_config_file(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)


def remove_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def remove_control_sequences(text: str) -> str:
    # Regex to match both ANSI codes and additional control sequences like '←(B'
    control_seq = re.compile(r'(\x1B[@-_][0-?]*[ -/]*[@-~])|(\x1B\[.*?m)|([^\x20-\x7E])')
    return control_seq.sub('', text)


# Function to extract preferences from a file with user_pref or pref
def extract_prefs(file_content):
    # Regex to match user_pref or pref ("key", value);
    prefs = re.findall(r'(?:user_pref|pref)\("(.+?)",\s*(.+?)\);', file_content)
    return {key: value for key, value in prefs}


# Function to format preferences with "pref("
def format_prefs(prefs):
    return [f'pref("{key}", {value});' for key, value in prefs.items()]


# Function to preserve non-pref lines (e.g., #include, #ifdef)
def merge_prefs_with_directives(file_content, formatted_prefs):
    new_lines = []
    prefs_dict = {pref.split('",')[0]: pref for pref in formatted_prefs}  # For easy lookup of updated prefs

    for line in file_content.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith(("pref(", "user_pref(")):
            # Extract the preference name to replace the line if it exists in prefs_dict
            pref_match = re.match(r'(?:user_pref|pref)\("(.+?)",', stripped_line)
            if pref_match:
                pref_name = pref_match.group(1)
                if pref_name in prefs_dict:
                    new_lines.append(prefs_dict[pref_name])
                    continue
        # Keep the line unchanged if it's not a preference line
        new_lines.append(line)

    return "\n".join(new_lines)


try:
    build_dir = f"{startingdir}/{str(load_config_file(f"{startingdir}/plinK.buildconfig")["build_dir"])}"
except Exception:
    print("Failed to update build dir")


class LogHandler:
    """Handles logging messages with different severity levels."""

    def __init__(self, log_widget, id, build_profile_after_build, copy_js_conf_after_build, profile_builder=None):
        self.start_time = datetime.now()
        self.log_widget = log_widget
        self.build_profile = build_profile_after_build
        self.copy_js_conf = copy_js_conf_after_build
        self.profile_builder = profile_builder
        self.id = id

    def get_id(self):
        return self.id

    def log(self, message, level="i"):
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Define log levels and corresponding Colorama colors
        levels = {
            "i": ("INFO", Fore.CYAN),
            "w": ("WARNING", Fore.YELLOW),
            "e": ("ERROR", Fore.RED),
            "d": ("DEBUG", Fore.GREEN),
            "r": ("RESET", Style.RESET_ALL)
        }

        # Get the level name and color
        level_name, color = levels.get(level, ("INFO", Fore.WHITE))
        lines = str(message).split("\\n")
        with open("plinK.log.temp", "w+", errors="replace") as f:
            f.write("\n".join(lines))
        with open("plinK.log.temp", "r+", errors="replace") as f:
            lines = f.readlines()
        # self.log_widget.write(lines)
        for line in lines:
            line = remove_control_sequences(line).replace("←(", "").replace("←[", "")
            with open(f"plinK_data/plinK_{session_id}_{self.id}.log", "a+", errors="replace") as ff:
                ff.write(f"— [{timestamp}] [{level_name}] {color}{line}{Fore.RESET} —\n")

            if "Your build was successful!" in line:
                log_message = f"— [{timestamp}] [{level_name}] {Fore.WHITE}----------{Fore.RESET} —"
                log_message = Text.from_ansi(log_message)
                self.log_widget.write(log_message)
                log_message = f"— [{timestamp}] [{level_name}] {Fore.GREEN}Your build has finished building :yipeeee:{Fore.RESET} —"
                log_message = Text.from_ansi(log_message)
                self.log_widget.write(log_message)
                log_message = f"— [{timestamp}] [{level_name}] {Fore.WHITE}----------{Fore.RESET} —"
                log_message = Text.from_ansi(log_message)
                self.log_widget.write(log_message)
            elif "Your build was successful!" in line and self.build_profile and self.profile_builder is not None:
                self.profile_builder()
            elif "Your build was successful!" in line and self.copy_js_conf:
                self.log_widget.write(
                    f"— [{timestamp}] [INFO] {Fore.CYAN}Copying prefs.js and user.js from new build to profile{Fore.RESET} —")
                shutil.copy(f"{build_dir}/tmp/profile-default/prefs.js", profile_dir)
                shutil.copy(f"{build_dir}/tmp/profile-default/user.js", profile_dir)

            # Format the log message with Colorama color codes
            log_message = f"— [{timestamp}] [{level_name}] {color}{line}{Fore.RESET} —"
            log_message = Text.from_ansi(log_message)

            # Add the log message to the widget (without ANSI codes)
            self.log_widget.write(log_message)
            with open("plinK.log.temp", "w+", errors="replace") as f:
                f.write("")

    def reload_logs(self, file):
        with open(file, "r") as f:
            lines = f.readlines()
        self.log_widget.write(Text.from_ansi("".join(lines)))


class StartApp(App):
    """A Textual App to display two windows, log messages, and accept user input."""

    CSS = """
    Screen {
        layout: vertical;
    }
    .window {
        border: wide;
        padding: 1;
    }
    #top {
        height: 1fr;
    }
    #bottom {
        height: 1fr;
        overflow-y: auto;
    }
    #input {
        height: 3;
    }
    """
    TITLE = "plinK"
    SUB_TITLE = "plinK"
    AUTO_FOCUS = "*"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.IGNORE_FILES = None
        self.COPY_JS_CONFIG_AFTER_BUILD = None
        self.BUILD_PROFILE_AFTER_BUILD = None
        self.PRESERVE_BOOKMARKS = None
        self.IGNORE_FOLDERS = None
        self.PRESERVE_FOLDERS = None
        self.PRESERVE_EXTENSIONS = None
        self.PRESERVE_PROFILE = None
        self.PRESERVE_FOLDER = None
        self.log_handler_top = None
        self.log_handler = None
        self.input_active = False
        self.user_input_event = asyncio.Event()
        self.user_input_value = None
        self.task_finished_event = asyncio.Event()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="plinK")
        yield Container(
            RichLog(classes="window", id="top"),
            RichLog(classes="window", id="bottom", auto_scroll=True)
        )
        yield Input(placeholder="Enter command for plinK - (press tab to change focused widget)", id="input",
                    disabled=True, suggester=SuggestFromList(commands, case_sensitive=True))
        yield Footer()

    async def _read_stream(self, stream, cb):
        """Asynchronously read the output of a stream line by line in real time."""
        while True:
            line = await stream.readline()
            if line:
                cb(line)  # Log each line immediately as it is read
            else:
                break

    async def _run_subprocess(self, cmd, stdout_cb, stderr_cb, cwd):
        """Runs a subprocess with real-time logging of stdout and stderr."""
        # Set environment variables to disable output buffering in the Python subprocess
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        # Start the subprocess with unbuffered output
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env  # Pass the unbuffered environment to the process
        )

        # Capture output from stdout and stderr asynchronously in real time
        await asyncio.gather(
            self._read_stream(process.stdout, stdout_cb),
            self._read_stream(process.stderr, stderr_cb)
        )

        # Wait for the subprocess to finish
        task_complete_signal = await process.wait()
        return task_complete_signal

    async def run_mach(self, command):
        """Handles running mach through Python and logging output in real time."""
        self.log_handler.log(f"Running command: {command}", "i")
        if command == "build":
            self.log_handler.log(f"Don't run the rd command while building, as it may break output of mach", "w")
        cmd = ["python", f"{startingdir}/mach"] + command.split()

        # Real-time stdout and stderr logging
        # Yes these coroutines aren't awaited for a reason
        asyncio.create_task(
            self._run_subprocess(
                cmd,
                lambda x: self.log_handler_top.log(x.decode().strip(), "i"),  # Real-time logging of stdout
                lambda x: self.log_handler_top.log(x.decode().strip(), "e"),  # Real-time logging of stderr
                cwd=startingdir
            )
        )

    async def run_cmd(self, command):
        self.log_handler.log(f"Running command: {command}", "i")
        cmd = command.split()

        # Real-time stdout and stderr logging
        # Yes these coroutines aren't awaited for a reason
        asyncio.create_task(
            self._run_subprocess(
                cmd,
                lambda x: self.log_handler_top.log(x.decode().strip(), "i"),  # Real-time logging of stdout
                lambda x: self.log_handler_top.log(x.decode().strip(), "e"),  # Real-time logging of stderr
                cwd=startingdir
            )
        )

    def load_config(self):
        config = load_config_file(f"{startingdir}/plinK.buildconfig")
        self.PRESERVE_PROFILE = bool(config["preserve_profile"])
        self.PRESERVE_EXTENSIONS = bool(config["preserve_extensions"])
        self.PRESERVE_FOLDERS = config["preserve_folders"]
        self.IGNORE_FOLDERS = config["ignore_folders"]
        self.IGNORE_FILES = config["ignore_files"]
        self.PRESERVE_BOOKMARKS = bool(config["preserve_bookmarks"])
        self.BUILD_PROFILE_AFTER_BUILD = bool(config["build_profile_after_build"])
        self.COPY_JS_CONFIG_AFTER_BUILD = bool(config["add_userjs_prefsjs_to_profile_after_build"])

    async def on_mount(self):
        """Called when the app is ready to start."""
        # Initialize the log handler with the bottom window (log widget)
        self.bottom_window = self.query_one("#bottom", RichLog)
        self.top_window = self.query_one("#top", RichLog)
        self.log_handler = LogHandler(self.bottom_window, build_profile_after_build=False,
                                      copy_js_conf_after_build=False, id="bottom")
        self.log_handler_top = LogHandler(self.top_window, build_profile_after_build=False,
                                          copy_js_conf_after_build=False, id="top")

        # Log some messages
        self.log_handler.log("plinK", "i")
        self.log_handler.log("Setting up windows", "i")
        await asyncio.sleep(1)  # TODO: Find a better way to get when the window is created/loaded
        if redraw_logs:
            self.log_handler_top.reload_logs(
                f"{startingdir}/plinK_data/plinK_{old_log_session_id}_{self.log_handler_top.get_id()}.log")
            self.log_handler.reload_logs(
                f"{startingdir}/plinK_data/plinK_{old_log_session_id}_{self.log_handler.get_id()}.log")

        # Check if it's the first start
        if os.path.exists(f"{startingdir}/plinK_data/first_start.plink"):
            with open(f"{startingdir}/plinK_data/first_start.plink", "r") as f:
                last_version = f.read().strip()
        else:
            last_version = __plinK_version__
        if not os.path.exists(f"{startingdir}/plinK_data/first_start.plink") or last_version != __plinK_version__:
            if last_version != __plinK_version__:
                self.log_handler.log("!!RECONFIGURING PLINK BECAUSE OF AN UPDATE!!")
                self.log_handler.log("---Your plinK.buildconfig file WILL BE LOST---", "w")
                await asyncio.sleep(2)
                self.log_handler.log(f"Old version: {last_version}")
            self.log_handler.log("First run", "w")
            self.log_handler.log(f"plinK version: {__plinK_version__}")
            # self.log_handler.log("Need to clear cache", "w")
            self.log_handler.log("--------------------------------")
            self.log_handler.log("Run ./mach bootstrap if you don't have mach set-up", "w")
            self.log_handler.log("--------------------------------")
            self.log_handler.log("Starting build...")
            task = asyncio.create_task(self.run_mach("build"))
            await task
            # Activate input after the warning message
            # self.user_input_event.clear()
            # task = asyncio.create_task(self.activate_input())
            # await task
            self.log_handler.log("Creating build config file")
            try:
                with open(f"{startingdir}/plinK.buildconfig", "x"):
                    pass
            except FileExistsError:
                pass
            with open(f"{startingdir}/plinK.buildconfig", "w") as f:
                f.write("""build_dir: obj-x86_64-pc-windows-msvc
preserve_bookmarks: true
preserve_profile: true
preserve_extensions: true
preserve_folders: []
ignore_folders: ["storage/permanent/chrome/idb", "cache2"]
ignore_files: []
build_profile_after_build: false
add_userjs_prefsjs_to_profile_after_build: false""")  # We assume, that user is on windows TODO: Make it change based on sys.platform
            await asyncio.sleep(1)
            self.log_handler.log(f"Done!")
            self.log_handler.log("--------------------------------")
            self.log_handler.log(f"plinK's buildconfig file is in {startingdir}/plinK.buildconfig", "w")
            self.log_handler.log("--------------------------------")
            self.log_handler.log("Finishing up...")
            try:
                with open(f"{startingdir}/plinK_data/first_start.plink", "x"):
                    pass
            except FileExistsError:
                pass
            with open(f"{startingdir}/plinK_data/first_start.plink", "w") as f:
                f.write(__plinK_version__)
            self.log_handler.log("Some features might not work while mach is building", "w")
            self.log_handler.log("Most features will not work until you create a user profile/run your build", "w")
        self.log_handler.log("Loading config...")
        self.load_config()
        self.log_handler = LogHandler(self.bottom_window, build_profile_after_build=self.BUILD_PROFILE_AFTER_BUILD,
                                      copy_js_conf_after_build=self.COPY_JS_CONFIG_AFTER_BUILD,
                                      profile_builder=self.profile_build(), id="bottom")
        self.log_handler_top = LogHandler(self.top_window, build_profile_after_build=self.BUILD_PROFILE_AFTER_BUILD,
                                          copy_js_conf_after_build=self.COPY_JS_CONFIG_AFTER_BUILD,
                                          profile_builder=self.profile_build(), id="top")

        #     os.chdir(startingdir)
        #     self.log_handler_top.log(self.execute(f"test.bat", lambda x: print("STDOUT: %s" % x),
        # lambda x: print("STDERR: %s" % x), cwd=startingdir))
        # self.log_handler_top.log(os.system("test.bat"))
        self.log_handler_top.log("Top window ready!")
        if redraw_logs:
            self.log_handler.log("Redrawing...", "w")
            await asyncio.create_task(self.bottom_window.recompose())
            self.log_handler.log("Bottom window redrawn")
            await asyncio.create_task(self.top_window.recompose())
            self.log_handler_top.log("Top window redrawn")
            await self.deactivate_input()
            input_box = self.query_one(Input)
            input_box.refresh()
            await self.activate_input()
            await asyncio.create_task(input_box.recompose())
            self.log_handler.log("Input redrawn")
        task = asyncio.create_task(self.activate_input())
        await task
        self.log_handler.log("Waiting for command...", "i")
        # await self.run_mach("build")

    # async def run_process(self, command):
    #     self.log_handler_top.log(command)
    #     process = await asyncio.create_subprocess_exec(
    #         *command.split(),
    #         shell=True,# Replace with your command
    #         # stdout=asyncio.subprocess.PIPE,
    #         # stderr=asyncio.subprocess.PIPE,
    #         # bufsize=0
    #     )
    #     # stdout, _ = yield process.communicate()
    #
    #     self.log_handler_top.log("created process")
    #     while True:
    #         try:
    #             output = await asyncio.wait_for(process.stdout.readline(),
    #                                             timeout=5.0)  # Increased timeout to 5 seconds
    #             if output:
    #                 self.call_from_thread(self.log_output, output.decode().strip())
    #             else:
    #                 break
    #         except asyncio.TimeoutError:
    #             self.log_handler_top.log("timeout")
    #             if process.poll() is not None:
    #                 break
    #             continue
    #
    #     # Check the exit code of the process
    #     exit_code = await process.wait()
    #     self.log_handler_top.log(f"Process exited with code {exit_code}")
    #
    # def log_output(self, output: str) -> None:
    #     if output:  # Check if output is not empty
    #         self.log_handler_top.log(output)

    async def get_user_input(self):
        await self.user_input_event.wait()

        return self.user_input_value

    async def activate_input(self, event=None):
        """Activate the input field."""
        self.input_active = True
        input_box = self.query_one(Input)
        input_box.disabled = False  # Enable the input field
        input_box.focus()  # Set focus to the input field
        if event is not None:
            event.input.value = ""
        await asyncio.sleep(0)

    async def deactivate_input(self):
        """Deactivate the input field after user input."""
        self.input_active = False
        input_box = self.query_one(Input)
        input_box.disabled = True  # Disable the input field
        await asyncio.sleep(0)

    async def profile_build(self):  # TODO: Make this ignore files and folders
        def ignore_files_and_dirs(src, names):
            """Custom ignore function to filter files based on config."""
            ignore_files = self.IGNORE_FILES
            ignore_folders = self.IGNORE_FOLDERS
            ignored = set()
            # Ignore specific files
            for file in ignore_files:
                if file in names:
                    ignored.add(file)
            # Ignore specific folders
            for folder in ignore_folders:
                if folder in names:
                    ignored.add(folder)
            return ignored

        try:
            shutil.rmtree(f"{startingdir}/plinK_data/profile_old")
        except Exception:
            pass
        try:
            shutil.rmtree(f"{profile_dir}/cache2")
            os.makedirs(f"{startingdir}/plinK_data/profile_old")
            os.makedirs(f"{startingdir}/plinK_data/profile")
        except Exception:
            pass
        if os.path.exists(f"{profile_dir}"):
            shutil.move(f"{profile_dir}", f"{startingdir}/plinK_data/profile_old")
        self.log_handler.log("Building profile...")
        self.log_handler_top.log("Mach output may interfere with profile building")

        if self.PRESERVE_PROFILE:
            self.log_handler.log("Copying profile")
            # Replace copy_tree with shutil.copytree to allow ignoring files and folders
            shutil.copytree(f"{build_dir}/tmp/profile-default", f"{profile_dir}",
                            ignore=ignore_files_and_dirs)
            self.log_handler.log("Done")
            return await asyncio.sleep(0)

        if self.PRESERVE_EXTENSIONS:
            self.log_handler.log("Preserving extensions")
            try:
                os.makedirs(f"{startingdir}/plinK_data/profile")
            except Exception:
                pass
            shutil.copytree(f"{build_dir}/tmp/profile-default/extension-store", f"{profile_dir}/extension-store",
                            ignore=ignore_files_and_dirs)
            self.log_handler.log("1/8")
            shutil.copytree(f"{build_dir}/tmp/profile-default/extension-store-menus",
                            f"{profile_dir}/extension-store-menus",
                            ignore=ignore_files_and_dirs)
            self.log_handler.log("2/8")
            shutil.copytree(f"{build_dir}/tmp/profile-default/browser-extension-data",
                            f"{profile_dir}/browser-extension-data", ignore=ignore_files_and_dirs)
            self.log_handler.log("3/8")
            shutil.copytree(f"{build_dir}/tmp/profile-default/extension-store", f"{profile_dir}/extension-store",
                            ignore=ignore_files_and_dirs)
            self.log_handler.log("4/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/addons.json", f"{profile_dir}/addons.json")
            self.log_handler.log("5/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/addonStartup.json.lz4",
                            f"{profile_dir}/addonStartup.json.lz4")
            self.log_handler.log("6/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/extension-preferences.json",
                            f"{profile_dir}/extension-preferences.json")
            self.log_handler.log("7/8")
            shutil.copyfile(f"{build_dir}/tmp/profile-default/extensions.json", f"{profile_dir}/extensions.json")
            self.log_handler.log("8/8")
            self.log_handler.log("Done")

        if self.PRESERVE_BOOKMARKS:
            self.log_handler.log("Preserving bookmarks")
            shutil.copytree(f"{build_dir}/tmp/profile-default/bookmarkbackups", f"{profile_dir}/bookmarkbackups",
                            ignore=ignore_files_and_dirs)
            self.log_handler.log("Done")

        if self.PRESERVE_FOLDER:
            self.log_handler.log("Preserving folders")
            for dir in self.PRESERVE_FOLDERS:
                shutil.copytree(dir, f"{profile_dir}", ignore=ignore_files_and_dirs)
            self.log_handler.log("Done")

        self.log_handler.log("Profile building done!")
        return await asyncio.sleep(0)

    async def on_input_submitted(self, event: Input.Submitted):
        """Handle user input when they press Enter."""
        if self.input_active:
            self.load_config()
            self.log_handler = LogHandler(self.bottom_window, build_profile_after_build=self.BUILD_PROFILE_AFTER_BUILD,
                                          copy_js_conf_after_build=self.COPY_JS_CONFIG_AFTER_BUILD,
                                          profile_builder=self.profile_build(), id="bottom")
            self.log_handler_top = LogHandler(self.top_window, build_profile_after_build=self.BUILD_PROFILE_AFTER_BUILD,
                                              copy_js_conf_after_build=self.COPY_JS_CONFIG_AFTER_BUILD,
                                              profile_builder=self.profile_build(), id="top")
            user_input = event.value
            # self.log_handler.log(f"User input: {user_input}", "i")
            self.user_input_value = user_input
            await self.deactivate_input()
            self.user_input_event.set()  # Notify that input has been received
            if user_input == "profile build":
                task = asyncio.create_task(self.profile_build())
                await task

            if user_input == "profile src build":
                self.log_handler_top.log(
                    "Merging prefs.js, user.js and .../bin/browser/defaults/preferences/firefox.js")
                self.log_handler.log("Current preferences in .../browser/app/profile/firefox.js will be replaced")
                self.log_handler.log("Run profile will be deleted", "w")
                # Read the contents of user.js, prefs.js, and firefox.js
                with open(f"{build_dir}/tmp/profile-default/user.js", 'r', errors="ignore") as user_file:
                    user_content = user_file.read()

                with open(f"{build_dir}/tmp/profile-default/prefs.js", 'r', errors="ignore") as prefs_file:
                    prefs_content = prefs_file.read()

                with open(f"{startingdir}/browser/app/profile/firefox.js", "r", errors="ignore") as f:
                    ffjs_def = f.read()

                # Extract preferences from all files (handling user_pref and pref)
                prefs = extract_prefs(prefs_content)  # From prefs.js
                user_prefs = extract_prefs(user_content)  # From user.js
                ffprefs = extract_prefs(ffjs_def)  # From firefox.js

                # Overwrite prefs with user.js values
                prefs.update(user_prefs)

                # Merge firefox.js prefs with the updated prefs from user.js and prefs.js
                ffprefs.update(prefs)

                # Format preferences with "pref("
                formatted_prefs = format_prefs(ffprefs)

                # Merge formatted prefs with original firefox.js, preserving non-pref lines
                merged_content = merge_prefs_with_directives(ffjs_def, formatted_prefs)

                if os.path.exists(f"{startingdir}/browser/app/profile/firefox.js.old"):
                    os.remove(f"{startingdir}/browser/app/profile/firefox.js.old")
                os.rename(f"{startingdir}/browser/app/profile/firefox.js",
                          f"{startingdir}/browser/app/profile/firefox.js.old")
                os.remove(f"{build_dir}/dist/bin/browser/defaults/preferences/firefox.js")
                shutil.rmtree(f"{build_dir}/tmp/profile-default")

                with open(f"{startingdir}/browser/app/profile/firefox.js", 'w', encoding="utf-8",
                          errors="replace") as output_file:
                    output_file.write(f"//file automatically generated by plinK \n{merged_content}")

                self.log_handler.log("Source profile building finished")
                self.log_handler.log("Building app and applying changes...", "w")
                self.log_handler.log("app_build", "d")
                task = asyncio.create_task(self.run_mach("build"))
                await task
            elif user_input == "profile push":
                self.log_handler.log("Pushing profile into rundir...")
                shutil.copytree(profile_dir, f"{build_dir}/tmp/profile-default")
                self.log_handler.log("Done")
            elif user_input == "profile sync prefs":
                shutil.copy(f"{build_dir}/tmp/profile-default/prefs.js", profile_dir)
                shutil.copy(f"{build_dir}/tmp/profile-default/user.js", profile_dir)
            elif user_input.startswith("build"):
                self.log_handler.log(f"app_build", "d")
                self.log_handler.log(f"Building...")
                task = asyncio.create_task(self.run_mach("build"))
                await task
                self.log_handler.log(f"ello")
            elif user_input == "run":
                self.log_handler.log(f"Copying profile...")
                self.log_handler.log(f"Profile in {build_dir}/tmp/profile-default WILL BE LOST", "w")
                shutil.copytree(profile_dir, f"{build_dir}/tmp/profile-default")
                await asyncio.sleep(1)
                # task = asyncio.create_task(self.run_cmd(f"{build_dir}/dist/bin/firefox.exe -profile '{build_dir}/tmp/profile-default'"))
                task = asyncio.create_task(self.run_mach("run"))
                await task
            elif user_input.startswith("logs"):
                await self.deactivate_input()
                await asyncio.sleep(2)
            elif user_input == "clear cache":
                self.log_handler_top.log("Clearing cache...")
                self.log_handler_top.log("This may take some time")
                task = asyncio.create_task(self.run_mach("clobber"))
                await task
            elif user_input == "rd":

                # for _ in range(20):
                #     self.log_handler_top.log(":plinK:", "r")
                await write_to_file(f"{startingdir}/plinK_data/redraw_logs.switch", session_id)
                # raise RedrawEventTrigger
                # Get the current python script and its arguments
                python = sys.executable
                script = sys.argv[0]
                args = sys.argv[1:]

                print("Restarting plinK")

                # Restart the application using execv()
                await self.deactivate_input()

                with self.suspend():
                    os.system("python plink.py")
                    self.exit(0)

                # close app, and open it in the same terminal window
                # TODO: Finish this rn
            elif user_input.startswith("mach"):
                cmd_by_usr_input = user_input.split(" ")[:1]
                task = self.run_mach("".join(cmd_by_usr_input))
                await task
            elif user_input == "close" or user_input == "quit":
                self.exit(0)
            elif user_input == "":
                pass
            elif user_input not in commands:
                self.log_handler.log(f'Unknown command - "{user_input}"', "e")

            await asyncio.sleep(0.001)
            await self.activate_input(event)
            return user_input

    async def wait_for_input(self):
        """Wait until the user has submitted input."""
        # Clear the event before waiting
        await self.user_input_event.wait()  # Wait for the event to be set
        return self.user_input_value


# Run the app
if __name__ == "__main__":
    try:
        StartApp().run()
    except RuntimeError as e:
        print(e)
    # except RedrawEventTrigger:
