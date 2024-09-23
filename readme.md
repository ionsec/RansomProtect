# RansomProtect
Developed by [IONSec](https://github.com/ionsec)

## About

`RansomProtect` is an open-source tool which identifies and blocks ransomware attacks early in the infection chain.

## Usage

### Option 1: Use Pre-built Executable (Recommended for Quick Setup)

1. Clone the repository:

    ```bash
    git clone https://github.com/ionsec/RansomProtect.git
    ```

2. Navigate to project's bin directory:

    ```bash
    cd RansomProtect\bin
    ```

3. Execute the pre-built `ransom-protect.exe`

### Option 2: Build from Source (For Developers or Customization)

To install `RansomProtect`, follow the steps below:

1. Clone the repository:

    ```bash
    git clone https://github.com/ionsec/RansomProtect.git
    ```

2. Navigate to the project directory:

    ```bash
    cd RansomProtect
    ```

3. Install project's dependencies:

    ```bash
    python3 -m venv venv
    venv\Scripts\activate.bat
    pip install -r requirements.txt
    ```

4. Install project'smodules (use -e to install in `dev` mode):

    ```bash
    pip install -e .
    ```
5. Build `RansomProtect` using pyinstaller:

    ```bash
    pyinstaller --onefile --console src/main.py
    ```
## Configurations


This section explains the configuration parameters used by the application. The config file is divided into three sections: `GENERAL`, `SPLUNK`, and `NETWORK`.

> **NOTE:** Make sure to modify the configuration values according to your environment before running the application.

```ini
[GENERAL]
TrapSensitivity = Low
TimeSensitivity = 10
Prefix          = 0_ios_
Extensions      = [".csv",".data",".docx",".mdb",".pem",".sql",".sqlite",".txt",".vmdk",".xlsx",".ini"]
Paths           = ["C:/ProgramData", "Desktop","Documents"]

[SPLUNK]
Token           = <TOKEN>
URL             = https://localhost:8088/services/collector/event
Source          = ransom_protect

[NETWORK]
Drop            = True
```

### General

- `TrapSensitivity`: Defines the sensitivity level for trapping suspicious activity. Possible values are `Low`, `Medium`, or `High`.
- `TimeSensitivity`: Sets the time window (in seconds) for detection. The default value here is `10`.
- `Prefix`: Aunique string that will be added as a prefix to all decoy files (e.g., `0_ios_`).
- `Extensions`: A list of file extensions to use for decoy files.
- `Paths`: Specifies the decoy directories.

### Splunk

- `Token`: Authentication token for the Splunk service. Replace `<TOKEN>` with your actual Splunk token.
- `URL`: The URL for sending events to Splunk’s HTTP Event Collector (HEC).
- `Source`: A custom source identifier for the Splunk logs, set as `ransom_protect`.

### Network

- `Drop`: Boolean flag (`True` or `False`) indicating whether network traffic should be dropped in case of suspicious activities. The default value is `True`.


