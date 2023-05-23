# Python Backdoor Coding Project

## Description

This project was created by following a tutorial from a course I found on Udemy:
[Complete Ethical Hacking Bootcamp 2023: Zero to Mastery](https://www.udemy.com/course/complete-ethical-hacking-bootcamp-zero-to-mastery/)

The course is a comprehensive overview of ethical hacking and penetration testing concepts.
This backdoor project contains two main programs:

`backdoor.py` - the file that runs on the target machine, the one you want to exploit

`server.py` - the file that runs on your own machine, the one sending the commands

These programs will work together to create a reverse TCP connection that allows you to send commands from your machine that the target machine executes, and the target machine sends back the output.

### Why Code Our Own Backdoor?

There are many reasons why it's useful to code our own backdoor program (as opposed to using premade exploits from a framework such as _Metasploit_):

1. **Customization**

   By developing your own backdoor, you have complete control over its functionality, features, and behavior. You can adapt it to meet your specific needs and objectives, making it easier to integrate into your existing infrastructure or target environment.

2. **Stealth and Evasion**

   Custom backdoors may be harder to detect by antivirus software or intrusion detection systems. By writing your own code, you can implement techniques to evade detection, such as using obfuscation, encryption, or anti-analysis methods. This can increase your chances of successfully infiltrating a target system.

3. **Education and Learning**

   When you create your own backdoor from scratch, it provides an excellent opportunity to learn and understand the intricacies of network protocols, security vulnerabilities, and exploit techniques. It allows you to deepen your knowledge of how these systems work and how they can be exploited, which can be valuable for defensive purposes as well.

4. **Tailored Exploitation**

   Premade exploits like those in _Metasploit_ often target known vulnerabilities in common software. However, if you encounter a unique or undisclosed vulnerability, coding your own backdoor allows you to specifically target and exploit that particular weakness, which gives you an advantage over other exploits.

5. **Adaptability**

   The security landscape is constantly evolving, with new defenses and countermeasures being developed regularly. By coding your own backdoor, you can continuously update and adapt it to bypass emerging security mechanisms. This flexibility can be particularly useful when dealing with hardened or well-protected systems.

### Base Functionality

Once the reverse TCP connection has been created, the attacking machine can send and run any command that the current user on the target machine could run, whether that's on a Windows command prompt or Unix terminal.

The base functionality of this project is relatively rudimentary. Here is the short list of commands that can be run in addition to the commands that you can naturally run on the target machine:

* `cd <path_to_directory>` - changes the current working directory on the target machine
* `download <path_to_file>` - downloads a file from the target machine to the current working directory on the attacking machine
* `upload <path_to_file>` - uploads a file from the attacking machine to the current working directory on the target machine
* `clear` - clears the terminal
* `quit` - closes the connection and exits both programs

### Additional Functionality

There are a handful of possible features I'd like to add on top of the base program.

| Feature             | Status | Description                                        |
|---------------------|--------|----------------------------------------------------|
| Keylogger           | ❌      | Capture and record keystrokes from the target      |
| Privilege Elevation | ❌      | Run commands as root on Unix or System on Windows  |
| Record Microphone   | ❌      | Record voice input from the target (if applicable) |
| Screenshot Desktop  | ❌      | Get screen grabs of the target's screen            |

## Setup and Installation

1. Start by cloning the project's repository onto your attacking machine.
   
   `git clone https://github.com/JaredMHarding/backdoor`

2. In both `server.py` and `backdoor.py`, there are two variables called `SERVER_IP` and `SERVER_PORT`. Their default values are based on my personal Kali Linux machine's IP address and port number. **Make sure to update `SERVER_IP` in both files to whatever your attacking machine's IP is**, otherwise the backdoor will not work. `SERVER_PORT` is arbitrary and can remain the same unless there's already another program/service running on the default port.

3. If you plan to run `backdoor.py` in a Windows environment, then you will need to compile the program on a Windows machine with Python 3 installed to create an executable file. Copy `backdoor.py` onto the Windows machine, and follow these steps...
   1. Open a command prompt and navigate to the directory where you copied `backdoor.py`.
   2. To compile the program, you will need a Pyinstaller library. If you don't already have Pyinstaller on your machine, use the command `pip install pyinstaller` to install it:
   3. Once Pyinstaller is installed, run this command:

      ```cmd
      pyinstaller backdoor.py --onefile --noconsole
      ```
   
      This will compile the program into an executable file called `backdoor.exe` in a folder named `dist`. You are now ready to run the backdoor.
   
   If you plan to run the backdoor on a Unix machine, no extra steps are needed, just copy `backdoor.py` onto the target machine.

4. You should now be ready to use the backdoor program. Run the server file with `python3 server.py` on your attacking machine, then run the backdoor on the target machine in the directory the backdoor file is in:
   - Windows: Run `start backdoor.exe` in the command prompt (or just double-click the file in the file explorer)
   - Unix: Run `python3 backdoor.py` in a terminal
   
   After a short delay, the connection should be created and a shell will appear on your attacking machine's terminal. You should now be able to run any of the commands listed in the functionality sections.

## Credits

The base project was coded by following an online tutorial. I plan to add more functionality to the project over time.

### Links

* [zerotomastery.io](https://zerotomastery.io/)
* Instructors:
  * [Andrei Neagoie](https://github.com/aneagoie) (Owner of Zero To Mastery)
  * Aleksa Tamburkovski (This project's code was based off of his lesson from the course)