# CTF Writeup: Crack Zip

* **Challenge:** Crack Zip
* **Event:** SusCTF 2017
* **Description:** This challenge involves bypassing or cracking an encrypted ZIP archive.

## Vulnerability Analysis & Approach

Before blindly attempting to crack the password, it is essential to understand the common techniques used in archive-based CTF challenges. 

Since the target is a ZIP file, our first step should be to check for **pseudo-encryption** (fake encryption). If the archive is genuinely encrypted, we must then evaluate the feasibility of a brute-force attack. Because we do not have any known plaintext files or specific hints regarding the password's structure, Known Plaintext Attacks (KPA) and Mask Attacks are not viable options.

## Resolution Steps

1. **Initial Inspection:** Attempted to extract the archive using Bandizip. A password prompt appeared, and the archive's directory revealed a single target file named `flag.txt`.
2. **Hex Analysis:** Opened the ZIP file in a hex editor (010 Editor) to inspect its underlying file structure and metadata.

   <img src="./pic1.png" width="500">

3. **Pseudo-Encryption Check:** Analyzed the general-purpose bit flags. Both the local file header flag (`frflag`) and the central directory file header flag (`deflag`) are odd numbers. This confirms that the file is genuinely encrypted, successfully ruling out the pseudo-encryption trick.
4. **Brute-Force Attack:** Loaded the archive into ARCHPR (Advanced Archive Password Recovery). Configured the brute-force parameters to scan a purely numeric range from `0` to `99999999`.
5. **Password Recovery:** The brute-force process successfully recovered the archive password: `20170925`.
6. **Flag Extraction:** Used the recovered password to extract `flag.txt` and retrieve the flag.

## Flag

`Susctf{ec1717de879b19792c77f5edacbb84dc}`
